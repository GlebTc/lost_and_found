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

# GET ALL USERS VIEW AS ADMIN
@api_view(['GET'])
def get_all_users(request):

    jwt_from_header = request.headers.get('Authorization')
    if not jwt_from_header:
        return Response({"error": "Authorization header missing."}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        jwt_token = jwt_from_header.split(" ")[1] if " " in jwt_from_header else jwt_from_header

        # Use token to fetch user id from Supabase Auth
        headers = {
            "Authorization": f"Bearer {jwt_token}",
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

        # Use user id to check role from Supabase `accounts_profile` table
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

        # Fetch all users
        supabase_response = (
            supabase
            .table("accounts_profile")
            .select("*")
            .execute()
        )
        
        supabase_auth_response = supabase_admin.auth.admin.list_users()

        return Response({
            "profiles": supabase_response.data,
            "auth_users": supabase_auth_response
        }, status=status.HTTP_200_OK)


    except Exception as e:
        return Response(
            {"error": f"Server error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
# GET INDIVIDUAL USER INFO AS ADMIN
@api_view(['GET'])
def get_individual_user_info(request, user_id):
    # Get user_id from params
    info_user_id = user_id
    if not info_user_id:
        return Response({"error": "Error - No User ID found in query params"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get JWT from header, "Authorization"
    jwt_from_header = request.headers.get("Authorization")
    if not jwt_from_header:
        return Response({"error": "Error - Could not obtain JWT from header"}, status=status.HTTP_401_UNAUTHORIZED)
    jwt_token = jwt_from_header.split(' ')[1] if " " in jwt_from_header else jwt_from_header

    # Decode JWT to check requestor role is "admin"
    try:
        decoded_jwt = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["HS256"])
        requestor_id = decoded_jwt.get("sub")  # Supabase stores user ID in the "sub" field
    except jwt.ExpiredSignatureError:
        return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    requestor_profile_response = (
        supabase
        .table("accounts_profile")
        .select("role")
        .eq("id", requestor_id)
        .single()
        .execute()
    )

    user_role = requestor_profile_response.data.get("role", "user")
    if user_role != "admin":
        return Response({"error": "Role Authorization Error - Not an Admin Role"}, status=status.HTTP_401_UNAUTHORIZED)

    # Query Supabase to get the individual user's profile
    try:
        user_profile = (
            supabase_admin
            .table("accounts_profile")
            .select("*")
            .eq("id", info_user_id)
            .single()
            .execute()
        )
        return Response(user_profile.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# EDIT/PATCH USER INFORMATION AS ADMIN
@api_view(['PATCH'])
def update_user(request, user_id):
    # 1. Validate user_id param
    if not user_id:
        return Response({
            'status': 'error',
            'message': 'Error - Unable to obtain user ID'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 2. Get and parse JWT from Authorization header
    jwt_from_header = request.headers.get('Authorization')
    if not jwt_from_header:
        return Response({
            'status': 'error',
            'message': 'Error - Unable to obtain JWT from header'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    jwt_token = jwt_from_header.split(" ")[1] if " " in jwt_from_header else jwt_from_header

    # 3. Decode JWT and get requestor ID
    try:
        decoded_jwt = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["HS256"])
        requestor_id = decoded_jwt.get("sub")
    except jwt.ExpiredSignatureError:
        return Response({
            'status': 'error',
            'message': 'Token has expired.'
        }, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return Response({
            'status': 'error',
            'message': 'Invalid token.'
        }, status=status.HTTP_401_UNAUTHORIZED)

    # 4. Confirm admin privileges
    requestor_profile_response = (
        supabase
        .table("accounts_profile")
        .select("role")
        .eq("id", requestor_id)
        .single()
        .execute()
    )

    requestor_role = requestor_profile_response.data.get("role", "user")
    if requestor_role != "admin":
        return Response({
            'status': 'error',
            'message': 'Role Authorization Error - Not an Admin Role'
        }, status=status.HTTP_403_FORBIDDEN)

    # 5. Extract update data
    allowed_fields = ['email', 'role', 'first_name', 'last_name', 'avatar_url']
    update_data = {field: request.data[field] for field in allowed_fields if field in request.data}

    if not update_data:
        return Response({
            'status': 'error',
            'message': 'No valid fields provided to update.'
        }, status=status.HTTP_400_BAD_REQUEST)

    # 6. Send update to Supabase
    try:
        response = (
            supabase_admin
            .table("accounts_profile")
            .update(update_data)
            .eq("id", user_id)
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

