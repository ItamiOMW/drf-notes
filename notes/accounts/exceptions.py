from rest_framework.exceptions import APIException


class InvalidTokenException(APIException):
    status_code = 400
    default_code = '4001'
    default_detail = {'code': 4001, 'message': 'Invalid Token'}


class InvalidEmailOrPasswordException(APIException):
    status_code = 400
    default_code = '4002'
    default_detail = {'code': 4002, 'message': 'Invalid email or password'}


class InvalidEmailException(APIException):
    status_code = 400
    default_code = '4003'
    default_detail = {'code': 4003, 'message': 'Invalid email'}


class EmailAlreadyVerifiedException(APIException):
    status_code = 400
    default_code = '4004'
    default_detail = {'code': 4004, 'message': 'Email already verified'}


class EmailNotVerifiedException(APIException):
    status_code = 400
    default_code = '4005'
    default_detail = {'code': 4005, 'message': 'Email not verified'}


class UserDoesNotExistException(APIException):
    status_code = 400
    default_code = '4006'
    default_detail = {'code': 4006, 'message': 'User does not exist'}


class UserAlreadyExistException(APIException):
    status_code = 400
    default_code = '4007'
    default_detail = {'code': 4007, 'message': 'User already exists'}


class InvalidVerificationCodeException(APIException):
    status_code = 400
    default_code = '4008'
    default_detail = {'code': 4008, 'message': 'Invalid verification code'}


class InvalidPasswordResetCodeException(APIException):
    status_code = 400
    default_code = '4009'
    default_detail = {'code': 4009, 'message': 'Invalid password reset code'}


class InvalidCredentialsException(APIException):
    status_code = 400
    default_code = '4010'
    default_detail = {'code': 4010, 'message': 'Invalid credentials'}


class ShortPasswordException(APIException):
    status_code = 400
    default_code = '4010'
    default_detail = {'code': 4010, 'message': 'Password must be more than 8 symbols'}


