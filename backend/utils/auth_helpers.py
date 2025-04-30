from rest_framework.response import Response
from rest_framework import status
import jwt
from supabase import create_client
import os

# Load config for direct access
SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_ANON_API_KEY")
supabase = create_client(SUPABASE_PROJECT_URL, SUPABASE_API_KEY)

def get_requestor_role(request):
    jwt_from_header = request.headers.get('Authorization')
    if not jwt_from_header:
        return None, Response({
            'status': 'error',
            'message': 'Authorization header missing.'
        }, status=status.HTTP_401_UNAUTHORIZED)

    jwt_token = jwt_from_header.split(" ")[1] if " " in jwt_from_header else jwt_from_header

    try:
        decoded = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["HS256"])
        user_id = decoded.get("sub")
    except jwt.InvalidTokenError:
        return None, Response({
            'status': 'error',
            'message': 'Invalid token.'
        }, status=status.HTTP_401_UNAUTHORIZED)

    role_check = (
        supabase
        .table("accounts_profile")
        .select("role")
        .eq("id", user_id)
        .single()
        .execute()
    )

    return role_check.data.get("role", "user"), None
