# Built-in modules
import os  # Used to access environment variables like your Supabase URL and API key
import requests  # Third-party library to make HTTP requests (we use this to contact Supabase)
import jwt


# Django imports
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

# USER PATCH OWN PROFILE VIEW
@csrf_exempt
@api_view(['PATCH'])
def own_update_profile(request):
    access_token = request.headers.get('Authorization')
    
    if not access_token:
        return Response({'error': 'Authorization header missing.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    token = access_token.split(' ')[1] if ' ' in access_token else access_token

    try:
        # Decode the token to extract user_id
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        user_id = decoded_token.get('sub')  # "sub" = subject = user_id in Supabase
        
        print(f"User Id - {user_id}")

        if not user_id:
            return Response({'error': 'User ID not found in token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fields available to be changed
        allowed_fields = ['email', 'role', 'first_name', 'last_name', 'avatar_url']
        update_data = {field: request.data[field] for field in allowed_fields if field in request.data}

        if not update_data:
            return Response({'error': 'No valid fields provided to update.'}, status=status.HTTP_400_BAD_REQUEST)

        response = (
            supabase
            .table('accounts_profile')
            .update(update_data)
            .eq('id', user_id)
            .execute()
        )

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
def own_delete_profile (request):
    access_token_w_bearer = request.headers.get('Authorization')
    
    access_token = access_token_w_bearer.split(' ')[1]
    
    if not access_token:
        return Response({'error': 'Authorization header missing - could not retrieve access token from header.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
    # Decode the access token
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        user_id_from_token = decoded_token.get('sub')
        
    
    # Delete User Profile
        supabase_response = (
            supabase
            .table('accounts_profile')
            .delete()
            .eq('id', user_id_from_token)
            .execute()
        )
    
        print(f"Supabase Delete Response {supabase_response}")
    
    # Delete Auth Profile    
        supabase_admin.auth.admin.delete_user(user_id_from_token)
    
        return Response({
            'status': 'success',
            'message': 'User deleted successfully.',
            'profile_delete_result': supabase_response,   
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'status': 'error',
            'message': 'Server error during user deletion.',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

