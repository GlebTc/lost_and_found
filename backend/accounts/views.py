# Built-in modules
import os  # Used to access environment variables like your Supabase URL and API key
import requests  # Third-party library to make HTTP requests (we use this to contact Supabase)

# Django imports
from django.http import JsonResponse  # Helper to return JSON responses to the client
from rest_framework.decorators import api_view  # Allows you to create views that respond to HTTP methods like POST
from rest_framework.response import Response  # To return API responses
from rest_framework import status  # For HTTP status codes
import pdb

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


@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    print('Got email and password')
    
    # pdb.set_trace()

    if not email or not password:
        return Response({'error': 'Missing email or password'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        url = f"{SUPABASE_PROJECT_URL}/auth/v1/token?grant_type=password"
        headers = {
            "apikey": SUPABASE_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "email": email,
            "password": password
        }

        response = requests.post(url, json=payload, headers=headers)

        print("SUPABASE LOGIN RESPONSE STATUS:", response.status_code)
        print("SUPABASE LOGIN RESPONSE TEXT:", response.text)

        try:
            data = response.json()  # try to parse JSON
        except ValueError:
            data = None  # Not valid JSON
        
        if response.status_code == 200 and data:
            access_token = data.get('access_token')
            print("ACCESS TOKEN:", access_token)

            return Response({
                'message': 'Login successful',
                'access_token': access_token,
                'user': data.get('user')
            }, status=status.HTTP_200_OK)
        else:
            if data:
                return Response({'error': data}, status=response.status_code)
            else:
                return Response({'error': response.text}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

