import base64
import logging
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

from app.config.settings import get_settings


settings = get_settings()


SPECIAL_CHARACTERS = ['@','#','$','%','=',':','?','.','/','|','~','>']
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def is_password_strong_enough(password: str) -> bool:
    if len(password) < 8:
        return False
    
    if not any(char.isupper() for char in password):
        return False
    
    if not any(char.islower() for char in password):
        return False
    
    if not any(char.isdigit() for char in password):
        return False
    
    if not any(char in SPECIAL_CHARACTERS for char in password):
        return False
    
    return True


def str_encode(string: str) -> str:
    return base64.b85encode(string.encode('ascii')).decode('ascii')


def str_decode(string: str) -> str:
    return base64.b85decode(string.encode('ascii')).decode('ascii')


def get_token_payload(token: str, secret: str, algo: str):
    try:
        payload = jwt.decode(token, secret, algorithms=algo)
    except Exception as jwt_exec:
        logging.debug(f'JWT Error: {str(jwt_exec)}')
        payload = None
    return payload


def generate_token(payload: dict, secret: str, algo: str, expiry: timedelta):
    expire = datetime.utcnow() + expiry
    payload.update({'exp': expire})
    return jwt.encode(payload, secret, algorithm=algo)


async def get_token_user(token: str, db):
    payload = get_token_payload(token, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    if payload:
        user = await load_user(str_decode(payload.get('username')), db)
        if user and user.id == int(payload.get('sub')):
            return user
    return None


async def load_user(email: str, db):
    from app.models.user import User
    try:
        user = db.query(User).filter(User.email == email).first()
    except Exception as user_exec:
        logging.info(f'User Not Found, Email: {email}')
        user = None
    return user

