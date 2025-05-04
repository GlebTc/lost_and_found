from rest_framework.response import Response
from rest_framework import status
import jwt
from database.supabase_client import supabase
from accounts.models import Profile
from accounts.serializers import ProfileSerializer

def get_profile_details(request):
    jwt_from_header = request.headers.get("Authorization")
    if not jwt_from_header:
        return None, Response({
            'status': 'error',
            'message': 'Authorization header missing.'
        }, status=status.HTTP_401_UNAUTHORIZED)
    jwt_token = jwt_from_header.split(" ")[1] if " " in jwt_from_header else jwt_from_header
    
    try:
        decoded = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["HS256"])
        auth_id = decoded.get("sub")
        profile_details = Profile.objects.get(id=auth_id)
        serialized_profile_details = ProfileSerializer(profile_details)

    except jwt.InvalidTokenError:
        return None, Response({
            'status': 'error',
            'message': 'Invalid token.'
        }, status=status.HTTP_401_UNAUTHORIZED)
        
    return serialized_profile_details, None
        
    

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
