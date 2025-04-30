# Built-in modules
import jwt

# Django imports
from rest_framework.decorators import api_view  # Allows you to create views that respond to HTTP methods like POST
from rest_framework.response import Response  # To return API responses
from rest_framework import status  # For HTTP status codes
from django.views.decorators.csrf import csrf_exempt

# Debugging
import pdb

# Models
from accounts.models import Profile

# Custom Modules
from database.supabase_client import supabase, supabase_admin

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
        
@csrf_exempt
@api_view(['GET'])
def own_view_profile(request):
    # Obtain JWT from headers "Authorization"
    jwt_from_header = request.headers.get('Authorization')
    if not jwt_from_header:
        return Response ({'error': 'Error - Unable to get JWT from header "Authorization'}, status=status.HTTP_401_UNATHORIZED)
    jwt_token = jwt_from_header.split(' ')[1] if " " in jwt_from_header else jwt_from_header

    
    # Decode jwt to obtain user_id
    
    try:
        decoded_jwt = jwt.decode(jwt_token, options={"verify_signature": False}, algorithms=["HS256"])

        user_id = decoded_jwt.get('sub')
    except jwt.ExpiredSignatureError:
        return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Use user_id to obtain profile information
    try:
        user_profile = (
            supabase
            .table("accounts_profile")
            .select("*")
            .eq("id", user_id)
            .single()
            .execute()
        )
        return Response(user_profile.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

