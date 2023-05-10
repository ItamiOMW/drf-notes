from django.core.validators import validate_email
from rest_framework.exceptions import ValidationError

from .exceptions import InvalidVerificationCodeException, ShortPasswordException, InvalidEmailException


def validate_verification_code(code):
    if len(code) != 6:
        raise InvalidVerificationCodeException

    if not code.isnumeric():
        raise InvalidVerificationCodeException


def validate_password(value):
    if len(value) < 8:
        raise ShortPasswordException


def validate_email_custom(value):
    try:
        validate_email(value)
    except ValidationError:
        raise InvalidEmailException
    except Exception:
        raise InvalidEmailException

