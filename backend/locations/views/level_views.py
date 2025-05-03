from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from locations.models import Level
from locations.serializers import LevelSerializer
from utils.auth_helpers import get_requestor_role

@api_view (['POST', 'GET'])
def create_list_all_levels(request):
    
    if request.method == 'POST':
        # Check if role is admin
        role, error_response = get_requestor_role(request)
        if error_response:
            return error_response
        if role != "admin":
            return Response ({
                "status": "error",
                "message": "Permission denied.  Admin access required."
            }, status = status.HTTP_403_FORBIDDEN)
            
        # Validate incoming data and save to db with serializer
        serializer = LevelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "GET":
        try:
            levels = Level.objects.all()
            serializer = LevelSerializer(levels, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Could not fetch level",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
@api_view(['GET', 'PATCH', 'DELETE'])
def get_patch_delete_level(request, level_id):
    if request.method == "GET":
        try:
            level=Level.objects.get(id=level_id)
            serializer=LevelSerializer(level)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': "Level not found"}, status=status.HTTP_404_NOT_FOUND)
            
    if request.method == "PATCH":
        # Check role
        role, error = get_requestor_role(request)
        if error:
            return error
        if role != "admin":
            return Response({
                "status": "error",
                "message": "Unauthorized User"
            }, status=status.HTTP_403_FORBIDDEN)
        try:
            level = Level.objects.get(id=level_id)
        except:
            return Response({
                "error": 'Level not found'
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = LevelSerializer(level, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Level update complete",
                "level": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        role, error = get_requestor_role(request)
        if error:
            return error
        if role != "admin":
            return Response({
                "status": "error",
                "message": "403 - Unauthorized - Admin access requied"
            }, status=status.HTTP_403_UNAUTHORIZED)
        
        try:
            level = Level.objects.get(id=level_id)
            level.delete()
            
            return Response({
                'message': f"200 - OK - Level '{level.name}' removed successfully"
            }, status=status.HTTP_200_OK)
        
        except Level.DoesNotExist:
            return Response({'error': 'Level not found'}, status=status.HTTP_404_NOT_FOUND)