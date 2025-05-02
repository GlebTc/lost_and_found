from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from locations.models import Site, Building
from locations.serializers import BuildingSerializer
from utils.auth_helpers import get_requestor_role

@api_view (['POST'])
def create_building(request):
    # Check if role is admin
    role, error_response = get_requestor_role(request)
    if error_response:
        return error_response
    if role != "admin":
        return Response({
            "status": "error",
            "message": "Permission denied. Admin access required."
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = BuildingSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)