from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import FoundItemSerializer
from .models import FoundItem

@api_view(['POST'])
def add_item(request):
    if request.method == 'POST':
        serializer = FoundItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the validated data to create a new FoundItem object
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['GET'])
def get_all_found_items(request):
    if request.method == 'GET':
        items = FoundItem.objects.all()
        serializer = FoundItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def get_item_by_id(request, item_id):
    if request.method == 'GET':
        try:
            item = FoundItem.objects.get(id=item_id)
            serializer = FoundItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FoundItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['DELETE'])
def delete_item(request, item_id):
    if request.method == 'DELETE':
        try:
            item = FoundItem.objects.get(id=item_id)
            item.delete()
            return Response({'message': 'Item deleted successfully'}, status=status.HTTP_200_OK)
        except FoundItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PUT'])
def edit_found_item(request, item_id):
    if request.method == 'PUT':
        try:
            item = FoundItem.objects.get(id=item_id)
            serializer = FoundItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except FoundItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)