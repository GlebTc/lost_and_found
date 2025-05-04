import requests
import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Items
from .serializers import ItemsSerializer
from utils.auth_helpers import get_requestor_role, get_profile_details

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
            }, status=status.HTTP_401_UAUTHORIZED)
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
            }, status=status.HTTP_401_UAUTHORIZED)
        items = Items.objects.all()
        serialized_items = ItemsSerializer(items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)
        
