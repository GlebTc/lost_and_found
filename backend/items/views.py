import requests
import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Items
from .serializers import ItemsSerializer

SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_ANON_API_KEY")

@api_view(['POST'])
def create_item(request):
    access_token = request.headers.get('Authorization')

    if not access_token:
        return Response({"error": "Authorization header missing."}, status=status.HTTP_401_UNAUTHORIZED)

    token = access_token.split(" ")[1] if " " in access_token else access_token

    # Fetch user info from Supabase
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": SUPABASE_API_KEY,
    }

    auth_response = requests.get(f"{SUPABASE_PROJECT_URL}/auth/v1/user", headers=headers)

    if auth_response.status_code != 200:
        return Response({"error": "Invalid token or Supabase auth failed."}, status=status.HTTP_401_UNAUTHORIZED)

    user_data = auth_response.json()
    user_id = user_data.get("id")



    # Add `accepted_by` and `item_returned_by` based on current user
    data = request.data.copy()
    data["accepted_by"] = user_id
    
    print("Creating item for user:", user_id, "with data:", data)

    serializer = ItemsSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
