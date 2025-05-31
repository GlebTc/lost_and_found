# Built-in
import os
import requests
import pdb

# Django
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Models & Serializers
from accounts.models import Profile
from accounts.serializers import ProfileSerializer

#Third party modules
from gotrue.errors import AuthApiError

# Supabase client
from database.supabase_client import supabase

# ENV
SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_ANON_API_KEY")

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CsrfTokenView(APIView):
    def get(self, request):
        return Response({'message': 'CSRF cookie set'}, status=status.HTTP_200_OK)

@method_decorator(csrf_protect, name='dispatch')
class RegisterUserView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Registration Error: Email or password missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            user_id = result.user.id
            user_email = result.user.email

            Profile.objects.create(
                id=user_id,
                email=user_email,
            )

            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_protect, name='dispatch')
class LoginUserView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        print(f"🟢 Login attempt: email={email}, password={'*' * len(password) if password else 'None'}")

        if not email or not password:
            print("🔴 Missing credentials")
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Attempt login via Supabase
            result = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if not result.user:
                print("🔴 Supabase login returned no user")
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = result.user.id

            try:
                profile = Profile.objects.get(id=user_id)
            except Profile.DoesNotExist:
                print(f"🔴 Profile not found for user_id={user_id}")
                return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

            serialized_profile = ProfileSerializer(profile)

            response = Response({
                "message": "User logged in successfully",
                "profile": serialized_profile.data
            }, status=status.HTTP_200_OK)

            if result.session:
                response.set_cookie(
                    key='jwt',
                    value=result.session.access_token,
                    httponly=True,
                    secure=False,  # Use True with HTTPS in production
                    samesite='Lax',
                    max_age=86400,
                    path='/'
                )
                print("✅ JWT cookie set")
            else:
                print("⚠️ Warning: No session returned from Supabase")

            return response

        except AuthApiError as auth_err:
            print(f"🔒 Supabase Auth Error: {auth_err}")
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(f"🔥 Unhandled exception: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({'error': 'Server error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@method_decorator(csrf_protect, name='dispatch')
class LogoutUserView(APIView):
    def post(self, request):
        jwt_token = request.COOKIES.get('jwt')

        if not jwt_token:
            return Response({"error": "JWT cookie missing."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            url = f"{SUPABASE_PROJECT_URL}/auth/v1/logout"
            headers = {
                "Authorization": f"Bearer {jwt_token}",
                "apikey": SUPABASE_API_KEY,
                "Content-Type": "application/json"
            }

            logout_response = requests.post(url, headers=headers)
            print("Logout Response:", logout_response.status_code, logout_response.text)

            response = Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
            response.delete_cookie('jwt')

            return response

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
