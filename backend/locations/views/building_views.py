from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from locations.models import Building
from locations.serializers import BuildingSerializer
from utils.auth_helpers import get_requestor_role

@api_view (['POST', 'GET'])
def create_list_all_building(request):
    
    if request.method == 'POST':
        # Check if the role is admin:
        role, error_response = get_requestor_role(request)
        if error_response:
            return error_response
        if role != "admin":
            return Response({
            "status": "error",
            "message": "Permission denied. Admin access required."
        }, status=status.HTTP_403_FORBIDDEN)
    
        # Validate incoming data with serializer and save to db
        serializer = BuildingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save ()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        buildings = Building.objects.all()
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view (['GET', 'PATCH', 'DELETE'])
def delete_patch_view_building(request, building_id):
    if request.method == "GET":
        try:
            building = Building.objects.get(id=building_id)
            print(building)
            serializer = BuildingSerializer(building)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Building not found'}, status=status.HTTP_404_NOT_FOUND)
        
    elif request.method == "PATCH":
    # Check if the role is admin
        role, error_response = get_requestor_role(request)
        if error_response:
            return error_response
        if role != "admin":
            return Response({
                "status": "error",
                "message": "Permission denied. Admin access required."
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            # Retrieve the building instance
            building = Building.objects.get(id=building_id)
        except Building.DoesNotExist:
            return Response({'error': 'Building not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Initialize the serializer with partial=True for partial updates
        serializer = BuildingSerializer(building, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Building updated successfully.',
                'building': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    elif request.method == "DELETE":
        # Check user role
        role, error_response = get_requestor_role(request)
        if error_response:
            return error_response
        if role != "admin":
            return Response({
                "status": "error",
                "message": "Permission Denied, admin access required"
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            building = Building.objects.get(id=building_id)
            building.delete()
  
            return Response({
                'message': f"Building '{building.name}' removed successfully"
            }, status=status.HTTP_204_NO_CONTENT)
        
        except Building.DoesNotExist:
            return Response({'error': 'Building not found'}, status=status.HTTP_404_NOT_FOUND)
        