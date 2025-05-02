from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from locations.models import Site
from locations.serializers import SiteSerializer
from utils.auth_helpers import get_requestor_role

@api_view(['POST'])
def create_site(request):
    # Check if role is admin
    role, error_response = get_requestor_role(request)
    if error_response:
        return error_response
    if role != "admin":
        return Response({
            "status": "error",
            "message": "Permission denied. Admin access required."
        }, status=status.HTTP_403_FORBIDDEN)
        
    # Pass incoming request data into the serializer for validation
    serializer = SiteSerializer(data=request.data)

    # If data is valid, serializer.save() will:
    # 1. Create a Site instance (using Django ORM)
    # 2. Save it to the database (Postgres via Supabase in your setup)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # If validation fails, return detailed errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_site(request, site_id):
    role, error_response = get_requestor_role(request)
    if error_response:
        return error_response
    if role != "admin":
        return Response({
            "status": "error",
            "message": "Permission denied. Admin access required."
        }, status=status.HTTP_403_FORBIDDEN)
        
    try:
        site = Site.objects.get(id=site_id)
        site.delete()
        return Response({'message': 'Site deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Site.DoesNotExist:
        return Response({'error': 'Site not found.'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PATCH'])
def edit_site(request, site_id):
    role, error_response = get_requestor_role(request)
    if error_response:
        return error_response
    if role != "admin":
        return Response({
            "status": "error",
            "message": "Permission denied. Admin access required."
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Extract new site name
        new_name = request.data.get("name")
        
        # Get site information from database
        site = Site.objects.get(id=site_id)
        
        # Update site name and save
        site.name = new_name
        site.save()

        # Serialize updated site
        serializer = SiteSerializer(site)

        return Response({
            'message': 'Site updated successfully.',
            'site': serializer.data
        }, status=status.HTTP_200_OK)

    except Site.DoesNotExist:
        return Response({'error': 'Site not found.'}, status=status.HTTP_404_NOT_FOUND)
