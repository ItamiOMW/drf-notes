from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .emails import send_verification_code_to_email, send_password_reset_code_to_email
from .models import User
from .serializers import UserSerializer, VerifyEmailSerializer, EmailSerializer, PasswordResetConfirmSerializer
from django.contrib.auth.hashers import make_password


class RegisterAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_verification_code_to_email(serializer.data['email'])

                data = {'message': 'We sent verification code to your email', 'data': serializer.data}
                return Response(data=data, status=status.HTTP_200_OK)

            data = {'message': 'something went wrong', 'data': serializer.errors}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)


class ResendVerificationCodeAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = EmailSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data['email']
                user = User.objects.filter(email=email).first()

                if user is None:
                    data = {'message': 'Account with such an email does not exist', 'data': {}}
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

                if user.is_active:
                    data = {'message': 'Email already verified', 'data': {}}
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

                send_verification_code_to_email(email)

                data = {'message': 'We sent verification code to your email', 'data': serializer.data}
                return Response(data=data, status=status.HTTP_200_OK)

            data = {'message': 'Something went wrong', 'data': {serializer.errors}}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)


class VerifyEmailAPI(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = VerifyEmailSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data['email']
                verification_code = serializer.data['verification_code']

                user = User.objects.filter(email=email).first()

                if user is None:
                    data = {'message': 'Account with such an email does not exist', 'data': {}}
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

                if user.verification_code != verification_code:
                    data = {'message': 'Invalid verification code', 'data': {}}
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

                user.is_active = True
                user.verification_code = None
                user.save()

                data = {'message': 'Email verified', 'data': {}}
                return Response(data=data, status=status.HTTP_200_OK)

            data = {'message': 'Something went wrong', 'data': serializer.errors}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)


class LoginAPI(APIView):
    permission_classes = []

    def post(self, request):
        try:
            email = request.data.get('email', default=None)
            password = request.data.get('password', default=None)

            if not email or not password:
                data = {'message': 'No credentials provided', 'data': {}}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(email=email, password=password)

            if user is not None:

                if user.is_active:
                    token = Token.objects.filter(user=user).first()

                    if token is None:
                        token = Token.objects.create(user=user)

                    data = {'message': 'Login successful', 'data': {'token': token.key, 'email': email}}
                    return Response(data=data, status=status.HTTP_200_OK)
                else:
                    data = {'message': 'Email is not verified', 'data': {}}
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

            else:
                data = {'message': 'Invalid email or password', 'data': {}}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)

    def get(self, request):
        data = {'message': 'Get User successful', 'data': {'user': str(request.user), 'auth': str(request.auth)}}
        return Response(data=data, status=status.HTTP_200_OK)


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        try:
            user_token = Token.objects.filter(key=request.auth.key).first()

            if user_token is not None:
                user_token.delete()
                data = {'message': 'Logout successful', 'data': {}}
                return Response(data=data, status=status.HTTP_200_OK)

            data = {'message': 'User already logged out', 'data': {}}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)


class PasswordResetAPI(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = EmailSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data['email']

                user = User.objects.filter(email=email).first()

                if user is None:
                    data = {'message': 'Account with such an email does not exist', 'data': {}}
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

                send_password_reset_code_to_email(email)

                data = {'message': 'We sent password reset code to your email', 'data': {}}
                return Response(data=data, status=status.HTTP_200_OK)

            data = {'message': 'Something went wrong', 'data': serializer.errors}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)


class PasswordResetConfirmAPI(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = PasswordResetConfirmSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data['email']
                password_reset_code = serializer.data['password_reset_code']
                new_password = serializer.data['new_password']

                user = User.objects.filter(email=email).first()

                if user is None:
                    data = {'message': 'Account with such an email does not exist', 'data': {}}
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

                if user.password_reset_code != password_reset_code:
                    data = {'message': 'Invalid password reset code', 'data': {}}
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

                user.password = make_password(new_password)
                user.password_reset_code = None
                user.save()

                data = {'message': 'Password reset successful', 'data': {}}
                return Response(data=data, status=status.HTTP_200_OK)

            data = {'message': 'Something went wrong', 'data': serializer.errors}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
