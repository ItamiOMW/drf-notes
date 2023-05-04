from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers

from .exceptions import InvalidEmailException, UserAlreadyExistException, ShortPasswordException, \
    InvalidVerificationCodeException, InvalidPasswordResetCodeException
from .models import User


# class CreateUserSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = ['email', 'password', 'is_active']
#
# def validate(self, attrs):
#
#     user = User.objects.filter(email=attrs['email']).first()
#     if user is not None:
#         raise UserAlreadyExistException
#
#     try:
#         validate_email(attrs['email'])
#     except ValidationError:
#         raise InvalidEmailException
#
#     if len(attrs['password']) < 8:
#         raise ShortPasswordException
#
#     return attrs
#
#     def create(self, validated_data):
#         validated_data['password'] = make_password(validated_data['password'])
#         return super(CreateUserSerializer, self).create(validated_data)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        email = validated_data['email']
        password = make_password(validated_data['password'])
        user = User.objects.filter(email=email).first()

        if user is not None and user.is_active == False:
            user.delete()

        user = User.objects.create_user(email=email, password=password)
        return user

    def validate(self, attrs):

        user = User.objects.filter(email=attrs['email']).first()
        if user is not None and user.is_active == True:
            raise UserAlreadyExistException

        try:
            validate_email(attrs['email'])
        except ValidationError:
            raise InvalidEmailException

        if len(attrs['password']) < 8:
            raise ShortPasswordException

        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField()

    def validate(self, attrs):
        try:
            validate_email(attrs['email'])
        except ValidationError:
            raise InvalidEmailException

        if len(attrs['verification_code']) != 6:
            raise InvalidVerificationCodeException


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()
    password_reset_code = serializers.CharField()

    def validate(self, attrs):
        try:
            validate_email(attrs['email'])
        except ValidationError:
            raise InvalidEmailException

        if len(attrs['verification_code']) != 6:
            raise InvalidPasswordResetCodeException

        if len(attrs['password']) < 8:
            raise ShortPasswordException


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        try:
            validate_email(attrs['email'])
        except ValidationError:
            raise InvalidEmailException
