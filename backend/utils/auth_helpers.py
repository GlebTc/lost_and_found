from rest_framework.response import Response
from rest_framework import status
import jwt
from database.supabase_client import supabase
from accounts.models import Profile
from accounts.serializers import ProfileSerializer


from jose import jwt
from jose.constants import ALGORITHMS
import requests
import os

SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")
JWKS_URL = f"{SUPABASE_PROJECT_URL}/auth/v1/keys"

import os
import requests
from jose import jwt
from jose.exceptions import JWTError

SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")
JWKS_URL = f"{SUPABASE_PROJECT_URL}/auth/v1/keys"

# Fetch JWKS (JSON Web Key Set).  The response will contain a list of dictionaries that have kid in them
def get_supabase_jwks():
    response = requests.get(JWKS_URL)
    response.raise_for_status()
    return response.json()

def verify_and_decode_jwt(request):
    # 1. Obtain the JWT from the cookie
    jwt_cookie = request.COOKIES.get("jwt")
    if not jwt_cookie:
        return None, "JWT cookie is missing."

    # 2. Parse the token out of cookie string. (From "Bearer <token>" to "<token>")
    jwt_token = jwt_cookie.split(" ")[1] if " " in jwt_cookie else jwt_cookie


    try:
    # 3. Verify JWT signature using Supabase JWKS and JWT kid (Key ID).
        jwks = get_supabase_jwks()
        unverified_header = jwt.get_unverified_header(jwt_token)
        rsa_key = next(
            (
                {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                for key in jwks["keys"]
                if key["kid"] == unverified_header["kid"]
            ),
            None,
        )
        if rsa_key is None:
            raise ValueError("Matching key not found in JWKS")
        
    # 4. If valid, return the decoded payload.
        decoded = jwt.decode(
            jwt_token,
            rsa_key,
            algorithms=[unverified_header["alg"]],
            issuer=f"{SUPABASE_PROJECT_URL}/auth/v1"
        )
        return decoded, None

    except JWTError as e:
        return None, str(e)
    except Exception as e:
        return None, f"JWT verification failed: {e}"

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

    if role_check.error:
        return None, Response({
            'status': 'error',
            'message': 'Failed to retrieve user role.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return role_check.data.get("role", "user"), None

