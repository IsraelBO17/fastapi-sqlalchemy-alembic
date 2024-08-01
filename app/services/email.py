from fastapi import BackgroundTasks
from app.config.settings import get_settings
from app.models.user import User
from app.config.email import send_email
from app.utils.email_context import USER_VERIFY_ACCOUNT

settings = get_settings()

async def send_account_verification_email(user: User, background_tasks: BackgroundTasks):
    from app.config.security import hash_password
    string_context = user.get_context_string(context=USER_VERIFY_ACCOUNT)
    token = hash_password(string_context)
    activate_url = f'{settings.FRONTEND_HOST}/auth/account-verify?token={token}&email={user.email}'
    data = {
        'app_name': settings.APP_NAME,
        'name': user.name,
        'activate_url': activate_url
    }
    subject = f'Account Verification - {settings.APP_NAME}'
    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name='user/account-verification.html',
        context=data,
        background_tasks=background_tasks
    )