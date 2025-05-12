import os
from django.conf import settings
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Items
from .serializers import ItemsSerializer
from utils.auth_helpers import get_profile_details

SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_ANON_API_KEY")

@api_view(['POST', 'GET'])
def create_get_all_items(request):
    if request.method == "POST":
    # Check if user exists
        profile_details_response, error = get_profile_details(request)
        if error:
            return Response({
                "status": "failed",
                "message": "401 - UNAUTHORIZED - Must be logged in to create items"
            }, status=status.HTTP_401_UNAUTHORIZED)
        profile_details_response_data = profile_details_response.data
    
        # Build item data in one go
        item_data = {
            key: request.data.get(key)
            for key in [
                "title",
                "description",
                "item_img_url",
                "status",
                "owner_identified",
                "owner_name",
                "owner_contact",
                "turned_in_by_name",
                "turned_in_by_phone",
                "claimed_by_id_verified",
                "claimed_by",
                "site",
                "building",
                "level",
                "department"
            ]
        }

        # Add fields from profile
        item_data["accepted_by"] = profile_details_response_data["id"]
        item_data["accepted_by_email"] = profile_details_response_data["email"]
            
        serialized_item = ItemsSerializer(data=item_data)
        if serialized_item.is_valid():
            serialized_item.save()
            return Response(
                serialized_item.data, status=status.HTTP_201_CREATED 
            )
        return Response(serialized_item.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "GET":
        # Check if user exists
        profile_details_response, error = get_profile_details(request)
        if error:
            return Response({
                "status": "failed",
                "message": "401 - UNAUTHORIZED - Must be logged in to create items"
            }, status=status.HTTP_401_UNAUTHORIZED)
        # # Extract query parameters from URL
        # query = request.query_params.get('q', '')
        
        # if query:
        #     items = Items.objects.filter(
        #         Q(title__icontains=query) |
        #         Q(description__icontains=query) |
        #         Q(location__icontains=query)  # if you have this field
        #     )
        
        paginator = PageNumberPagination()
        paginator.page_size = 10
            
        items = Items.objects.all()
        paginated_items = paginator.paginate_queryset(items, request)
        serialized_items = ItemsSerializer(paginated_items, many=True)
        return paginator.get_paginated_response(serialized_items.data)


@api_view(["GET", "PATCH", "DELETE"])
def get_patch_delete_item(request, item_id):
    # Check if user exists
    profile_details_response, error = get_profile_details(request)
    if error:
        return Response({
            "status": "failed",
            "message": "401 - UNAUTHORIZED - Must be logged in to access or modify items"
        }, status=status.HTTP_401_UNAUTHORIZED)
    profile_details_response_data = profile_details_response.data
    
    if request.method == "GET":
        try:
            item_data = Items.objects.get(id=item_id)
            serialized_item_data = ItemsSerializer(item_data)
            return Response(serialized_item_data.data)
        except Items.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "PATCH":
        try:
            # Fetch item to update:
            item_to_update = Items.objects.get(id=item_id)
            #Create serialized updated data
            serialized_item_data = ItemsSerializer(item_to_update, data=request.data, partial=True)
            if serialized_item_data.is_valid():
                serialized_item_data.save()
                return Response({
                    "status": "success",
                    "updated_item": serialized_item_data.data
                }, status=status.HTTP_200_OK)
            return Response(serialized_item_data.errors, status=status.HTTP_400_BAD_REQUEST)
        except Items.DoesNotExist:
            return Response({
                "error": "Item not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "error": "Unable to process request",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_ERROR)
            
    if request.method == "DELETE":
        try:
           item_to_delete = Items.objects.get(id=item_id)
           item_to_delete.delete()
           return Response({
               "status": "success",
               "message": f"Item {item_id} deleted successfully"
           }, status=status.HTTP_200_OK)
        except Items.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Item not found"
            }, status=status.HTTP_404_NOT_FOUND)