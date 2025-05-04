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
    access_token = request.headers.get('Authorization')
    if not access_token:
        return Response({'error': 'Authorization header missing.'}, status=status.HTTP_401_UNAUTHORIZED)
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
            serialized_updated_data = ProfileSerializer(profile, data=request.data, partial=True)
            if serialized_updated_data.is_calid():
                serialized_updated_data.save()
                return Response({
                    "message": "Profile updated successfully",
                    "updated_profile": serialized_updated_data.data
                }, status=status.HTTP_200_OK)
            return Response(serialized_updated_data.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "error": "Unable to process request",
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == "DELETE":
        print("Delete Activated")
        try:
            profile = Profile.objects.get(id=auth_id)
            profile.delete()
            
            supabase_admin.auth.admin.delete_user(auth_id)
            return Response({
                'message': f"Profile deleted successfully",
            }, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
