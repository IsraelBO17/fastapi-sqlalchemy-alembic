from datetime import datetime
import logging
from fastapi import HTTPException
from app.models.user import User
from app.config.security import hash_password, is_password_strong_enough, verify_password
from app.services.email import send_account_activation_email, send_account_verification_email
from app.utils.email_context import USER_VERIFY_ACCOUNT

async def create_user_account(data, session, background_tasks):

    user_exist = session.query(User).filter(User.email == data.email).first()
    if user_exist:
        raise HTTPException(status_code=400, detail='Email already exists.')
    
    if not is_password_strong_enough(data.password):
        raise HTTPException(status_code=400, detail='Please provide a strong password.')

    user = User()
    user.name = data.name
    user.email = data.email
    user.password = hash_password(data.password)
    user.is_active = False
    user.updated_at = datetime.utcnow()
    
    session.add(user)
    session.commit()
    session.refresh(user)

    # Account Verification Email
    await send_account_verification_email(user, background_tasks=background_tasks)

    return user


async def activate_user_account(data, session, background_tasks):
    user = session.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail='This is not valid.')
    
    user_token = user.get_context_string(context=USER_VERIFY_ACCOUNT)

    try:
        token_valid = verify_password(user_token, data.token)
    except Exception as verify_exec:
        logging.exception(verify_exec)
        token_valid = False
    
    if not token_valid:
        raise HTTPException(status_code=400, detail='The link is either expired or not valid.')
    
    user.is_active = True
    user.updated_at = datetime.utcnow()
    user.verified_at = datetime.utcnow()
    session.add(user)
    session.commit()
    session.refresh(user)

    # Activation confirmation email
    await send_account_activation_email(user, background_tasks=background_tasks)

    return user

    