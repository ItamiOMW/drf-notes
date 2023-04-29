from rest_framework.response import Response
from rest_framework.views import APIView

from .emails import send_verification_code_to_email
from .models import User
from .serializers import UserSerializer, VerifyEmailSerializer, EmailSerializer


class RegisterAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_verification_code_to_email(serializer.data['email'])
                return Response({
                    'status': 200,
                    'message': 'We sent verification code to your email',
                    'data': serializer.data
                })
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)


class ResendVerificationCode(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = EmailSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data['email']
                user = User.objects.filter(email=email)

                if not user.exists():
                    return Response({
                        'status': 400,
                        'message': 'something went wrong',
                        'data': 'Account with such an email does not exist'
                    })

                if user[0].is_email_verified:
                    return Response({
                        'status': 400,
                        'message': 'something went wrong',
                        'data': 'Email already verified'
                    })

                send_verification_code_to_email(email)
                return Response({
                    'status': 200,
                    'message': 'We sent verification code to your email',
                    'data': serializer.data
                })
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })

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

                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response({
                        'status': 400,
                        'message': 'something went wrong',
                        'data': 'Account with such an email does not exist'
                    })

                if user[0].email_verification_code != verification_code:
                    return Response({
                        'status': 400,
                        'message': 'something went wrong',
                        'data': 'Wrong verification code'
                    })

                user = user[0]
                user.is_email_verified = True
                user.save()

                return Response({
                    'status': 200,
                    'message': 'Email verified',
                    'data': {}
                })
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })

        except Exception as e:
            print(e)
