# Django imports
from rest_framework.decorators import api_view  # Allows you to create views that respond to HTTP methods like POST
from rest_framework.response import Response  # To return API responses
from rest_framework import status  # For HTTP status codes

# Debugging
import pdb

# Models
from accounts.models import Profile

# Serializers
from accounts.serializers import ProfileSerializer

# Custom Modules
from utils.auth_helpers import get_requestor_role
from database.supabase_client import supabase_admin


@api_view(['GET', 'POST'])
def create_list_all_profiles(request):
    role, error_response = get_requestor_role(request)
    if error_response:
        return error_response
    if role != "admin":
        return Response({
            "status": "error",
            "message": "Permission denied. Admin access required."
        }, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        try:
            # Fetch all profiles using Django ORM
            profiles = Profile.objects.all()
            serializer = ProfileSerializer(profiles, many=True)
            # Fetch all users from supabase auth table
            auth_users = supabase_admin.auth.admin.list_users()

            # Response containing Profiles, no need to return user data.
            return Response({
                "status": "success",
                "profiles": serializer.data,
                # "auth_users": auth_users
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Server error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if request.method == "POST":
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
            
            # Prepare data for Profile
            profile_data = {
                "id": user_id,
                "email": request.data['email'],
                "role": request.data.get('role', 'user'),
                "first_name": request.data.get('first_name'),
                "last_name": request.data.get('last_name'),
                "avatar_url": request.data.get('avatar_url')
            }
            
            serializer = ProfileSerializer(data=profile_data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'User successfully created.',
                    'profile': serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'status': 'error',
                    'message': 'Profile validation failed.',
                    'details': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Server error during user creation.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# I do not neeed to get auth data for either get or patch request as the information used will be only coming from Profile table.  I only need user table to delete a profile/user.
@api_view(['GET', 'PATCH', 'DELETE'])
def get_patch_delete_profile_and_user (request, user_id):
    role, error_response = get_requestor_role(request)
    if error_response:
        return error_response
    if role != "admin":
        return Response({
            "status": "error",
            "message": "Permission denied. Admin access required."
        }, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == "GET":
        profile = Profile.objects.get(id=user_id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == "PATCH":
        try:
            profile = Profile.objects.get(id=user_id)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully",
                "updated_profile": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "DELETE":
        try:
            profile = Profile.objects.get(id=user_id)
            profile.delete()
            
            supabase_admin.auth.admin.delete_user(user_id)
            return Response({
                'message': f"Profile deleted successfully",
            }, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)