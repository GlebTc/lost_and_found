# Built-in modules
import os  # Used to access environment variables like your Supabase URL and API key
import requests  # Third-party library to make HTTP requests (we use this to contact Supabase)

# Django imports
from django.http import JsonResponse  # Helper to return JSON responses to the client
from rest_framework.decorators import api_view  # Allows you to create views that respond to HTTP methods like POST
from rest_framework.response import Response  # To return API responses
from rest_framework import status  # For HTTP status codes

# Load your Supabase config from environment variables
SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")  # e.g., https://your-project.supabase.co
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")  # Your public Supabase "anon" key

@api_view(['POST'])
def register_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email or password missing'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Response object if the request goes through successfully
        response = requests.post(
            f"{SUPABASE_PROJECT_URL}/auth/v1/signup",
            headers={
                "apikey": SUPABASE_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "email": email,
                "password": password
            }
        )
        
        # Debugging prints
        print("SUPABASE RESPONSE STATUS:", response.status_code)
        print("SUPABASE RESPONSE TEXT:", response.text)
        print("SUPABASE RESPONSE HEADERS:", response.headers)
    
        if response.status_code in [200, 201]:
            return Response({"message": 'User Registered Successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': response.json()}, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNL_SERVER_ERROR)