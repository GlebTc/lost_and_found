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

# GET ALL USERS VIEW
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