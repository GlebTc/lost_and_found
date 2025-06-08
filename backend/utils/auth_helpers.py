from rest_framework.response import Response
from rest_framework import status
from jose import jwt, JWTError
from database.supabase_client import supabase
from accounts.models import Profile
from accounts.serializers import ProfileSerializer
import os

SUPABASE_SECRET = os.getenv("SUPABASE_JWT_SECRET")  # This is your JWT secret for HS256
SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")


def verify_and_decode_jwt(request):
    # 1. Get the JWT from the cookie
    jwt_cookie = request.COOKIES.get("jwt")
    if not jwt_cookie:
        return None, "JWT cookie is missing."

    # 2. Extract raw token from "Bearer <token>" format
    jwt_token = jwt_cookie.split(" ")[1] if " " in jwt_cookie else jwt_cookie

    try:
        # 3. Decode the token using HS256 and your service key
        decoded = jwt.decode(
            jwt_token,
            key=SUPABASE_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False},
            issuer=f"{SUPABASE_PROJECT_URL}/auth/v1"
        )
        return decoded, None

    except JWTError as e:
        return None, f"JWT verification failed: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error during JWT verification: {e}"


def get_profile_details(request):
    decoded_jwt, error = verify_and_decode_jwt(request)
    if error:
        return None, Response({
            'status': 'error',
            'message': error
        }, status=status.HTTP_401_UNAUTHORIZED)

    auth_id = decoded_jwt.get("sub")
    if not auth_id:
        return None, Response({
            'status': 'error',
            'message': 'User ID (sub) not found in token.'
        }, status=status.HTTP_401_UNAUTHORIZED)

    try:
        profile = Profile.objects.get(id=auth_id)
        serialized = ProfileSerializer(profile)
        return serialized, None
    except Profile.DoesNotExist:
        return None, Response({
            'status': 'error',
            'message': 'User profile not found.'
        }, status=status.HTTP_404_NOT_FOUND)


def get_requestor_role(request):
    decoded_jwt, error = verify_and_decode_jwt(request)
    if error:
        return None, Response({
            'status': 'error',
            'message': error
        }, status=status.HTTP_401_UNAUTHORIZED)

    user_id = decoded_jwt.get("sub")
    if not user_id:
        return None, Response({
            'status': 'error',
            'message': 'User ID (sub) not found in token.'
        }, status=status.HTTP_401_UNAUTHORIZED)

    role_check = (
        supabase
        .table("accounts_profile")
        .select("role")
        .eq("id", user_id)
        .single()
        .execute()
    )
    
    if not role_check.data:
        return None, Response({
            'status': 'error',
            'message': 'Failed to retrieve user role.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return role_check.data.get("role", "user"), None
