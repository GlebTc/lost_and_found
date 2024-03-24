from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomUserSerializer, CustomUser
from rest_framework import status
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def register_user(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        serialized_user = CustomUserSerializer(user).data
        return Response({"message": "User created successfully", "user_data": serialized_user, }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        return Response({
                    'success': True,
                    'user_id': user.id,
                    'message': 'User logged in successfully.',
                    'username': user.email,  # Use email as username field,
                    'is_active_user': user.is_active,
                    'role': user.role,
                }, status=status.HTTP_200_OK)
    else:
        # User authentication failed
        return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_user(request):
    user = request.user
    serialized_user = CustomUserSerializer(user).data
    return Response(serialized_user, status=status.HTTP_200_OK)

@api_view(['PUT'])
def edit_user(request):
    user = request.user
    serializer = CustomUserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_all_users(request):
    users = CustomUser.objects.all()
    serialized_users = CustomUserSerializer(users, many=True).data
    return Response(serialized_users, status=status.HTTP_200_OK)
