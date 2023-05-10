from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .emails import send_verification_code_to_email, send_password_reset_code_to_email
from .serializers import *


class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            send_verification_code_to_email(serializer.data['email'])

            data = {'message': 'We sent verification code to your email', 'data': serializer.data}
            return Response(data=data, status=status.HTTP_200_OK)


class ResendVerificationCodeAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = ResendEmailVerificationCodeSerializer(data=data)

        if serializer.is_valid():
            email = serializer.data['email']

            send_verification_code_to_email(email)

            data = {'message': 'We sent verification code to your email', 'data': serializer.data}
            return Response(data=data, status=status.HTTP_200_OK)


class VerifyEmailAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = VerifyEmailSerializer(data=data)

        if serializer.is_valid():
            email = serializer.data['email']

            user = User.objects.filter(email=email).first()

            user.is_active = True
            user.verification_code = None
            user.save()

            data = {'message': 'Email verified', 'data': {}}
            return Response(data=data, status=status.HTTP_200_OK)


class LoginAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if serializer.is_valid():

            email = serializer.data['email']
            password = serializer.data['password']

            user = authenticate(email=email, password=password)

            if user is not None:

                if user.is_active:
                    token = Token.objects.filter(user=user).first()

                    if token is None:
                        token = Token.objects.create(user=user)

                    data = {'message': 'Login successful', 'data': {'token': token.key, 'email': email}}
                    return Response(data=data, status=status.HTTP_200_OK)
                else:
                    raise EmailNotVerifiedException

            else:
                raise InvalidEmailOrPasswordException
        else:
            raise InvalidEmailOrPasswordException


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        user_token = Token.objects.filter(key=request.auth.key).first()

        if user_token is not None:
            user_token.delete()

        data = {'message': 'Logout successful', 'data': {}}
        return Response(data=data, status=status.HTTP_200_OK)


class PasswordResetAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = PasswordResetSerializer(data=data)

        if serializer.is_valid():
            email = serializer.data['email']

            send_password_reset_code_to_email(email)

            data = {'message': 'We sent password reset code to your email', 'data': {}}
            return Response(data=data, status=status.HTTP_200_OK)


class PasswordResetConfirmAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = PasswordResetConfirmSerializer(data=data)

        if serializer.is_valid():
            email = serializer.data['email']
            new_password = serializer.data['new_password']

            user = User.objects.filter(email=email).first()

            user.password = make_password(new_password)
            user.password_reset_code = None
            user.save()

            data = {'message': 'Password reset successful', 'data': {}}
            return Response(data=data, status=status.HTTP_200_OK)


class IsUserTokenValidAPI(APIView):

    def post(self, request):
        token = request.data
        token = Token.objects.filter(key=token).first()

        if token is not None:
            user = User.objects.filter(id=token.user_id).first()
            data = {'message': 'Token is valid', 'data': {'user': user.email, 'auth': token.key}}
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise InvalidTokenException
