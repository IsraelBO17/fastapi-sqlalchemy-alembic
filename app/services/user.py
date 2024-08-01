from fastapi import HTTPException
from app.models.user import User
from app.config.security import hash_password, is_password_strong_enough

async def create_user_account(data, session):

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
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
    