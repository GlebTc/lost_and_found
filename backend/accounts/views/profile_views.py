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

# Serializers
from accounts.serializers import ProfileSerializer

# Custom Modules
from database.supabase_client import supabase, supabase_admin

@api_view(['GET', 'PATCH', 'DELETE'])
def get_patch_delete_profile_and_user(request):
    # Check JWT
    access_token = request.COOKIES.get('jwt')
    if not access_token:
        return Response({'error': 'JWT token missing from cookies.'}, status=status.HTTP_401_UNAUTHORIZED)
    token = access_token.split(' ')[1] if ' ' in access_token else access_token
    # Decode JWT to obtain auth_id
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    auth_id = decoded_token.get('sub')
    # Get profile information using auth_id
    profile = Profile.objects.get(id=auth_id)
    if not profile:
        return Response({
            "error": f"No profile found associated with this {auth_id}"
        })

    
    if request.method == "GET":
        try:
            serialized_profile_data = ProfileSerializer(profile)
            return Response(serialized_profile_data.data)
        except Exception as e:
            return Response({
                "error": "Unable to process request",
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if request.method == "PATCH":
        try:
            # Obtain current and updated password from request body
            current_password = request.data.get("current_password")
            new_password = request.data.get("new_password")

            # Check if new password has been provided
            if new_password:
                # Check if current password i sbeing provided
                if not current_password:
                    return Response({
                        "status": "error",
                        "message": "Current password is required to change your password."
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Send a request to supabase auth to verify current login credentials
                auth_check = supabase.auth.sign_in_with_password({
                    "email": profile.email,
                    "password": current_password
                })

                if None or not auth_check.user:
                    return Response({
                        "status": "error",
                        "message": "Current password is incorrect."
                    }, status=status.HTTP_403_FORBIDDEN)

                # Step 2: Update password using Supabase admin
                response = supabase_admin.auth.admin.update_user_by_id(auth_id, {
                    "password": new_password
                })
                return Response({
                    "status": "success",
                    "message": "Password updated successfully"
                }, status=status.HTTP_200_OK)

            # If not updating password, update other profile fields
            serialized_updated_data = ProfileSerializer(profile, data=request.data, partial=True)
            if serialized_updated_data.is_valid():
                serialized_updated_data.save()
                return Response({
                    "status": "success",
                    "message": "Profile updated successfully",
                    "updated_profile": serialized_updated_data.data
                }, status=status.HTTP_200_OK)

            return Response({
                "status": "error",
                "message": "Profile update failed",
                "errors": serialized_updated_data.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "status": "error",
                "message": "Server error during update",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    if request.method == "DELETE":
        try:
            profile = Profile.objects.get(id=auth_id)
            profile.delete()
            
            supabase_admin.auth.admin.delete_user(auth_id)
            return Response({
                'message': f"Profile deleted successfully",
            }, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
