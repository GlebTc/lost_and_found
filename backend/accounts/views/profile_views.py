from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from jose import jwt
from accounts.models import Profile
from accounts.serializers import ProfileSerializer
from database.supabase_client import supabase, supabase_admin
from utils.auth_helpers import verify_and_decode_jwt

class classProfileDetailView(APIView):
    # Extracts auth_id from a verified JWT token.
    def get_auth_id(self, request):
        decoded_token, error = verify_and_decode_jwt(request)
        if error:
            return None, Response({
                'error': 'JWT verification failed',
                'details': error
            }, status=status.HTTP_401_UNAUTHORIZED)
        return decoded_token.get('sub'), None
    
    def get(self, request):
        # Use the class (self) get_auth_id method to obtain auth_id from the decoded JWT.
        auth_id, error_response = self.get_auth_id(request)
        if error_response:
            return error_response
        
        try:
            profile = Profile.objects.get(id=auth_id)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({
                'error': f"Could not fine profile with {auth_id}",
            }, status=status.HTTP_404_NOT_FOUND)
        except Eception as e:
            return Response({
                'error': 'Unable to process request',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self, request):
        auth_id, error_response = self.get_auth_id(request)
        if error_response:
            return error_response
        
        try:
            profile = Profile.objects.get(id=auth_id)
            current_password = request.data.get('current_password')
            new_password = request.data.get('new_password')

            # If patch request is for password, change password
            if new_password:
                if not current_password:
                    return Response({
                        'status': 'errror',
                        'message': 'Current password required to change password'
                    }, status=status.HTTP_400_BAD_REQUEST)

                auth_check = supabase.auth.sign_in_with_password({
                    "email": profile.email,
                    "password": current_password
                })

                if not auth_check.user:
                    return Response({
                        'status': 'error',
                        'message': 'Current password is incorrect'
                    }, status=status.HTTP_403_FORBIDDEN)
                
                supabase_admin.auth.admin.update_user_by_id(auth_id, {
                    'password': new_password
                })

                return Response({
                    'status': 'success',
                    'message': 'Password updatd successfully'
                })
            
            # If patch request is not for password
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Profile updated successfully',
                    'updated_profile': serializer.data
                })
            
            return Response({
                'status': 'error',
                'message': 'Failed to update profile',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Server error',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request):
        auth_id, error_response = self.get_auth_id(request)
        if error_response:
            return error_response
        
        try:
            profile = Profile.objects.get(id=auth_id)
            profile.delete()
            supabase_admin.auth.admin.delete_user(auth_id)
            return Response({'message': "Profile deleted successfully"})
        
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
