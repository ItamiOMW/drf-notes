from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .exceptions import *
from .models import User
from .validators import validate_verification_code, validate_password, validate_email_custom


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[validate_email_custom, ])
    password = serializers.CharField(validators=[validate_password, ])

    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()

        if user is not None:
            raise UserAlreadyExistException

        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        password = make_password(validated_data['password'])
        user = User.objects.create_user(email=email, password=password)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[validate_email_custom, ])
    password = serializers.CharField(validators=[])

    def validate(self, attrs):
        email = attrs['email']

        user = User.objects.filter(email=email).first()

        if user is not None and not user.is_active:
            raise EmailNotVerifiedException

        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[validate_email_custom, ])
    verification_code = serializers.CharField(validators=[validate_verification_code, ])

    def validate(self, attrs):
        email = attrs['email']
        verification_code = attrs['verification_code']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise UserDoesNotExistException

        if user.is_active:
            raise EmailAlreadyVerifiedException

        if user.verification_code != verification_code:
            raise InvalidVerificationCodeException

        return attrs





class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[validate_email_custom, ])
    new_password = serializers.CharField(validators=[validate_password, ])
    password_reset_code = serializers.CharField(validators=[validate_verification_code, ])

    def validate(self, attrs):
        email = attrs['email']
        password_reset_code = attrs['password_reset_code']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise UserDoesNotExistException

        if user.password_reset_code != password_reset_code:
            raise InvalidPasswordResetCodeException

        return attrs


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[validate_email_custom, ])

    def validate(self, attrs):
        email = attrs['email']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise UserDoesNotExistException

        return attrs


class ResendEmailVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[validate_email_custom, ])

    def validate(self, attrs):
        email = attrs['email']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise UserDoesNotExistException

        if user.is_active:
            raise EmailAlreadyVerifiedException

        return attrs
