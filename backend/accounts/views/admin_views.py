from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.models import Profile
from accounts.serializers import ProfileSerializer
from utils.auth_helpers import get_requestor_role
from database.supabase_client import supabase_admin

class CreateListAllProfilesView(APIView):
        
    def post(self, request):
        role, error_response = get_requestor_role(request)
        if error_response:
            return error_response
        if role != "admin":
            return Response({
                'status': 'error',
                'message': 'Permission denied, failed to create profile, admin access required'
            }, status=status.HTTP_403_FORBIDDEN)
        
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in request.data:
                return Response({
                    'status': 'error',
                    'message': f'Missing required field {field}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            auth_response = supabase_admin.auth.admin.create_user({
                'email': request.data['email'],
                'password': request.data['password'],
                # 'email_confirm': True           Add this when frontend has email confirmation in form
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

            serializer = ProfileSerializer(data=profile_data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'User successfully created',
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

    def get(self, request):
        role, error_response = get_requestor_role(request)
        if error_response:
            return error_response
        if role != "admin":
            return Response({
                'status': 'error',
                'message': 'Permission denied, failed to get list of profiles, admin access required'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            profiles = Profile.objects.all()
            serializer = ProfileSerializer(profiles, many=True)
            return Response({
                'status': 'success',
                'profiles': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Server error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProfileAdminDetailView(APIView):
    def get(self, request, user_id):
        role, error_response = get_requestor_role(request)
        if error_response:
            return error_response
        if role != "admin":
            return Response({
                "status": "error",
                "message": "Permission denied. Admin access required."
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            profile = Profile.objects.get(id=user_id)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, user_id):
        role, error_response = get_requestor_role(request)
        if error_response:
            return error_response
        if role != "admin":
            return Response({
                "status": "error",
                "message": "Permission denied. Admin access required."
            }, status=status.HTTP_403_FORBIDDEN)

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

    def delete(self, request, user_id):
        role, error_response = get_requestor_role(request)
        if error_response:
            return error_response
        if role != "admin":
            return Response({
                "status": "error",
                "message": "Permission denied. Admin access required."
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            profile = Profile.objects.get(id=user_id)
            profile.delete()
            supabase_admin.auth.admin.delete_user(user_id)
            return Response({
                'message': "Profile deleted successfully",
            }, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

