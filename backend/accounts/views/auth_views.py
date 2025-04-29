# Auth Views
# Built-in modules
import os  # Used to access environment variables like your Supabase URL and API key
import requests  # Third-party library to make HTTP requests (we use this to contact Supabase)

# Django imports
from django.http import JsonResponse  # Helper to return JSON responses to the client
from rest_framework.decorators import api_view  # Allows you to create views that respond to HTTP methods like POST
from rest_framework.response import Response  # To return API responses
from rest_framework import status  # For HTTP status codes
from django.views.decorators.csrf import csrf_exempt

# Debugging
import pdb

# Third Party
from supabase import create_client, Client

# Models
from accounts.models import Profile

# Supabase Variables
SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_ANON_API_KEY")

# Initializing Supabase Client
supabase: Client = create_client(SUPABASE_PROJECT_URL, SUPABASE_API_KEY)

# USER REGISTRATION VIEW
@api_view(['POST'])
def register_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Registration Error: Email or password missing'}, status=status.HTTP_400_BAD_REQUEST)

    # Create new user in auth table and get results
    try:
        result = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        print(f"Registration Results {result}")
    # Assign id and email from results to a variable
        user_id = result.user.id
        user_email = result.user.email
        
    # Create a user profile in profile table with reference to the auth table and give the profile a role
    
        profile = Profile.objects.create(
            id=user_id,
            email=user_email,
        )
        
        print(f"Profile Information {profile}")

        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# USER LOGIN VIEW
@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Login Error: Email or password missing'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # 1. Sign in user with Supabase
        result = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )

        # 2. Obtain user id from authentication
        user_id = result.user.id 
        # print(f"Login Results: {result}")

        # 3. Obtain profile information
        profile = (
            supabase.table("accounts_profile")
            .select("id, email, role")  
            .eq("id", user_id)          
            .single()                   
            .execute()
        )

        # print(f"User Information: {profile}")

        # 4. Return successful response
        return Response({
            "message": "User logged in successfully",
            "access_token": result.session.access_token,
            "profile": profile.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# USER LOGOUT VIEW
@api_view(['POST'])
def logout_user(request):
    access_token = request.data.get('access_token')
    
    if not access_token:
        return Response({'error': 'Logout Error: Missing Access Token'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        url = f"{SUPABASE_PROJECT_URL}/auth/v1/logout"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "apikey": SUPABASE_API_KEY,
            "Content-Type": "application/json"
        }
        
        logoutResponse = requests.post(url, headers=headers)
        print("Logout Response:", logoutResponse.status_code, logoutResponse.text)
        
        if logoutResponse.status_code == 204:
            return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': logoutResponse.text}, status=logoutResponse.status_code)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)