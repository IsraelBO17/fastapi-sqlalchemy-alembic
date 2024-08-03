from fastapi import APIRouter, BackgroundTasks, Depends, Header, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config.database import get_session
from app.responses.user import LoginResponse, UserResponse
from app.schemas.user import EmailRequest, RegisterUserRequest, ResetPasswordRequest, VerifyUserRequest
from app.services import user

user_router = APIRouter(
    prefix='/users',
    tags=['Users'],
    responses={404: {'description': 'Not found'}},
)

guest_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
    responses={404: {'description': 'Not found'}},
)

@user_router.post('', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(data: RegisterUserRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    return await user.create_user_account(data, session, background_tasks)

@user_router.post('/verify', status_code=status.HTTP_200_OK)
async def verify_user_account(data: VerifyUserRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    await user.activate_user_account(data, session, background_tasks)
    return JSONResponse({'message': 'Account is activated successfully.'})

@guest_router.post('/login', status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def login_user(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    return await user.get_login_token(data, session)

@guest_router.post('/refresh', status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def refresh_token(refresh_token = Header(), session: Session = Depends(get_session)):
    return await user.get_refresh_token(refresh_token, session)

@guest_router.post('/forgot-password', status_code=status.HTTP_200_OK)
async def forgot_password(data: EmailRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    await user.email_forgot_password_link(data, background_tasks, session)
    return JSONResponse({'message': 'An email with the password link has been sent to your email address.'})

@guest_router.post('/reset-password', status_code=status.HTTP_200_OK)
async def reset_password(data: ResetPasswordRequest, session: Session = Depends(get_session)):
    await user.reset_user_password(data, session)
    return JSONResponse({'message': 'Your password has been updated.'})


