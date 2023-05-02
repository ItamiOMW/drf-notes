from django.core.mail import send_mail
from django.conf import settings

import random

from .models import User


def send_verification_code_to_email(email):
    subject = 'Verification Code'
    verification_code = random.randint(100000, 999999)
    message = f'Your verification code is {verification_code}'
    user_obj = User.objects.get(email=email)
    user_obj.verification_code = verification_code
    user_obj.save()
    send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST, recipient_list=[email])


def send_password_reset_code_to_email(email):
    subject = 'Password Reset Code'
    reset_code = random.randint(100000, 999999)
    message = f'Your password reset code code is {reset_code}'
    user_obj = User.objects.get(email=email)
    user_obj.password_reset_code = reset_code
    user_obj.save()
    send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST, recipient_list=[email])
