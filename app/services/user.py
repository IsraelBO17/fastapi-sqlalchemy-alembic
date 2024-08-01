from datetime import datetime
from fastapi import HTTPException
from app.models.user import User
from app.config.security import hash_password, is_password_strong_enough
from app.services.email import send_account_verification_email

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
    user.updated_at = datetime.now(datetime.timezone.utc)
    
    session.add(user)
    session.commit()
    session.refresh(user)

    # Account Verification Email
    await send_account_verification_email(user, background_tasks=background_tasks)

    return user
    