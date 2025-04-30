# Django imports
from rest_framework.decorators import api_view  # Allows you to create views that respond to HTTP methods like POST
from rest_framework.response import Response  # To return API responses
from rest_framework import status  # For HTTP status codes

# Debugging
import pdb

# Custom Modules
from utils.auth_helpers import get_requestor_role
from database.supabase_client import supabase_admin
from database.user_service import get_all_profiles, get_profile_by_id, update_profile, delete_profile, create_profile

@api_view(['GET'])
def get_all_users(request):
    role, error_response = get_requestor_role(request)
    if error_response:
        return error_response
    if role != "admin":
        return Response({
            "status": "error",
            "message": "Permission denied. Admin access required."
        }, status=status.HTTP_403_FORBIDDEN)

    try:
        profiles = get_all_profiles()
        auth_users = supabase_admin.auth.admin.list_users()

        return Response({
            "status": "success",
            "profiles": profiles.data,
            "auth_users": auth_users
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_individual_user_info(request, user_id):
    if not user_id:
        return Response({"error": "Missing user ID."}, status=status.HTTP_400_BAD_REQUEST)

    role, error_response = get_requestor_role(request)
    if error_response:
        return error_response
    if role != "admin":
        return Response({"error": "Not an admin."}, status=status.HTTP_403_FORBIDDEN)

    try:
        user_profile = get_profile_by_id(user_id)
        return Response(user_profile.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
def update_user(request, user_id):
    if not user_id:
        return Response({"error": "Missing user ID."}, status=status.HTTP_400_BAD_REQUEST)

    role, error_response = get_requestor_role(request)
    if error_response:
        return error_response
    if role != "admin":
        return Response({"error": "Not an admin."}, status=status.HTTP_403_FORBIDDEN)

    allowed_fields = ['email', 'role', 'first_name', 'last_name', 'avatar_url']
    update_data = {field: request.data[field] for field in allowed_fields if field in request.data}

    if not update_data:
        return Response({"error": "No valid fields provided."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        response = update_profile(user_id, update_data)

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

@api_view(['DELETE'])
def delete_user(request, user_id):
    role, error_response = get_requestor_role(request)
    if error_response:
        return error_response
    if role != "admin":
        return Response({
            'status': 'error',
            'message': 'Permission denied. Admin access required.'
        }, status=status.HTTP_403_FORBIDDEN)

    try:
        # 1. Delete from accounts_profile
        delete_profile(user_id)

        # 2. Delete from Supabase Auth
        supabase_admin.auth.admin.delete_user(user_id)

        return Response({
            'status': 'success',
            'message': 'User successfully deleted from profile and auth.',
            'deleted_user_id': user_id
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'status': 'error',
            'message': 'Server error during user deletion.',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_user(request):
    role, error_response = get_requestor_role(request)
    if error_response:
        return error_response
    if role != "admin":
        return Response({
            'status': 'error',
            'message': 'Permission denied. Admin access required.'
        }, status=status.HTTP_403_FORBIDDEN)

    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in request.data:
            return Response({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }, status=status.HTTP_400_BAD_REQUEST)

    try:
        auth_response = supabase_admin.auth.admin.create_user({
            "email": request.data['email'],
            "password": request.data['password'],
            "email_confirm": True
        })

        user_id = auth_response.user.id

        profile_data = {
            "id": user_id,
            "email": request.data['email'],
            "role": request.data.get('role', 'user'),
            "first_name": request.data.get('first_name'),
            "last_name": request.data.get('last_name'),
            "avatar_url": request.data.get('avatar_url')
        }

        profile_response = create_profile(profile_data)

        return Response({
            'status': 'success',
            'message': 'User successfully created.',
            'user_id': user_id,
            'profile': profile_response.data
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'status': 'error',
            'message': 'Server error during user creation.',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
