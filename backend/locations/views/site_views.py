from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from locations.models import Site
from locations.serializers import SiteSerializer
from utils.auth_helpers import get_requestor_role

@api_view(['GET', 'POST'])
def create_list_all_site(request):
    if request.method == "POST":
        # Check if role is admin
        role, error_response = get_requestor_role(request)
        if error_response:
            return error_response
        if role != "admin":
            return Response({
            "status": "error",
            "message": "Permission denied. Admin access required."
        }, status=status.HTTP_403_FORBIDDEN)
        
        
        serializer = SiteSerializer(data=request.data)

        # If data is valid, serializer.save() will:
        # 1. Create a Site instance (using Django ORM)
        # 2. Save it to the database (Postgres via Supabase in your setup)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If validation fails, return detailed errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "GET":
        sites = Site.objects.all() #Get all the sites from db
        serializer = SiteSerializer(sites, many=True) # Serialize data
        return Response(serializer.data, status=status.HTTP_200_OK) # Return Data

@api_view(['GET', 'PATCH', 'DELETE'])
def get_patch_delete_site(request, site_id):
    if request.method == "GET":
        try:
            site = Site.objects.get(id=site_id)
            serializer = SiteSerializer(site)
            return Response(serializer.data, status.HTTP_200_OK)
        except Site.DoesNotExist:
            return Response({'error': 'Site not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == "PATCH":
        # Check if role is admin
        role, error_response = get_requestor_role(request)
        if error_response:
            return error_response
        if role != "admin":
            return Response({
            "status": "error",
            "message": "Permission denied. Admin access required."
        }, status=status.HTTP_403_FORBIDDEN)
        
        # Patch site information
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
    elif request.method == "DELETE":
        # Check if role is admin
        role, error_response = get_requestor_role(request)
        if error_response:
            return error_response
        if role != "admin":
            return Response({
            "status": "error",
            "message": "Permission denied. Admin access required."
        }, status=status.HTTP_403_FORBIDDEN)

        try:
            site = Site.objects.get(id=site_id)  # Get id first
            site.delete()  # Then delete
            return Response({
                'message': f"Site '{site.name}' removed successfully"
            }, status=status.HTTP_204_NO_CONTENT)

        except Site.DoesNotExist:
            return Response({'error': 'Site not found.'}, status=status.HTTP_404_NOT_FOUND)
