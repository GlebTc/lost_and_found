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