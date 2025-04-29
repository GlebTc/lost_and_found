# Built-in modules
import os  # Used to access environment variables like your Supabase URL and API key
import requests  # Third-party library to make HTTP requests (we use this to contact Supabase)
import json
import jwt


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

# Load your Supabase config from environment variables
SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_ANON_API_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Initializing Supabase Client
supabase: Client = create_client(SUPABASE_PROJECT_URL, SUPABASE_API_KEY)
supabase_admin: Client = create_client(SUPABASE_PROJECT_URL, SUPABASE_SERVICE_ROLE_KEY)

# GET ALL USERS VIEW
@api_view(['GET'])
def get_all_users(request):
    print("Get All Users View Activated")

    access_token = request.headers.get('Authorization')
    if not access_token:
        return Response({"error": "Authorization header missing."}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # ✅ Cleanly extract the bearer token
        token = access_token.split(" ")[1] if " " in access_token else access_token
        print("Token:", token)

        # ✅ Use token to fetch user info from Supabase Auth
        headers = {
            "Authorization": f"Bearer {token}",
            "apikey": SUPABASE_API_KEY,
        }

        supabase_auth_response = requests.get(
            f"{SUPABASE_PROJECT_URL}/auth/v1/user",
            headers=headers
        )

        if supabase_auth_response.status_code != 200:
            return Response(
                {"error": "Get All Users Error: Invalid token or Supabase auth failed."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user_data = supabase_auth_response.json()
        user_id = user_data.get("id")

        # ✅ Check role from Supabase `accounts_profile` table
        profile_response = (
            supabase
            .table("accounts_profile")
            .select("role")
            .eq("id", user_id)
            .single()
            .execute()
        )

        user_role = profile_response.data.get("role", "user")

        if user_role != "admin":
            return Response(
                {"error": "Permission denied. Admin access required."},
                status=status.HTTP_403_FORBIDDEN
            )

        # ✅ Fetch all users
        supabase_response = (
            supabase
            .table("accounts_profile")
            .select("*")
            .execute()
        )

        return Response({"users": supabase_response.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": f"Server error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# USER OWN PATCH PROFILE VIEW
@csrf_exempt
@api_view(['PATCH'])
def own_update_profile(request, user_id):
    access_token = request.data.get('access_token')
    
    if not access_token:
        return Response({'error': 'Patch Error: Missing Access Token'}, status=status.HTTP_400_BAD_REQUEST)

    allowed_fields = ['email', 'role', 'first_name', 'last_name', 'avatar_url']
    update_data = {field: request.data[field] for field in allowed_fields if field in request.data}

    if not update_data:
        return Response({'error': 'No valid fields provided to update.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        response = (
            supabase
            .table('accounts_profile')
            .update(update_data)
            .eq('id', user_id)
            .execute()
        )

        # print("Supabase Update Response:", response)
        # print("DATA:", response.data)

        if response.data:
            return Response({
                'status': 'success',
                'message': 'Profile updated successfully.',
                'updated_profile': response.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'message': 'Profile update failed. No data returned.'
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            'status': 'error',
            'message': 'Server error during profile update.',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# USER OWN DELETE PROFILE VIEW
@csrf_exempt
@api_view (['DELETE'])
def own_delete_profile (request, user_id):
    access_token = request.data.get('access_token')
    
    if not access_token:
        return Response({'error': 'Delete Error: Access Token Missing - Not Logged In'}, status=status.HTTP_400_BAD_REQUEST)

    try:
    # Decode the access token
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        user_id_from_token = decoded_token.get('sub')  # sub = user_id
        user_role_from_token = decoded_token.get('role', 'user')  # default to user if not found

        # print("Decoded token user_id:", user_id_from_token)
        # print("Decoded token role:", user_role_from_token)
    
    # Check if request user_id matches decoded user_id or if the role is admin.
        if user_id != user_id_from_token and user_role_from_token != 'admin':
            return Response({'error': 'You are not authorized to delete this user.'}, status=status.HTTP_403_FORBIDDEN)
        
    
    # Delete User Profile
    
        supabase_response = (
            supabase
            .table('accounts_profile')
            .delete()
            .eq('id', user_id)
            .execute()
        )
    
        print(f"Supabase Delete Response {supabase_response}")
    
    # Delete Auth Profile
    
        auth_response = supabase_admin.auth.admin.delete_user(user_id)
    
        print(f"Auth Delete Response {auth_response}")
    
        return Response({
            'status': 'success',
            'message': 'User deleted successfully.',
            'profile_delete_result': supabase_response,  # you can log it if needed
            'auth_delete_result': str(auth_response)  # auth delete returns None or response
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'status': 'error',
            'message': 'Server error during user deletion.',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

