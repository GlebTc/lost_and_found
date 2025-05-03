from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from locations.models import Department
from locations.serializers import DepartmentSerializer
from utils.auth_helpers import get_requestor_role

@api_view(['POST', 'GET'])
def create_list_all_departments(request):
    
    if request.method == "POST":
        # Check role
        role, error = get_requestor_role(request)
        if error:
            return error
        if role != "admin":
            return Response({
                "status": "error",
                "message": "403 - Forbidden - Admin acccess requierd"
            }, status=status.HTTP_403_FORBIDDEN)
            
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        try:
            departments = Department.objects.all()
            serializer = DepartmentSerializer(departments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": 'error',
                'message': 'Department not found',
                'details': str(e)                
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
@api_view(['GET', 'PATCH', 'DELETE'])
def get_patch_delete_department(request, department_id):
    # Handle GET: Retrieve department
    if request.method == "GET":
        try:
            department = Department.objects.get(id=department_id)
            serializer = DepartmentSerializer(department)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response({'error': "Department not found"}, status=status.HTTP_404_NOT_FOUND)

    # Handle PATCH: Update department
    elif request.method == "PATCH":
        role, error = get_requestor_role(request)
        if error:
            return error
        if role != "admin":
            return Response({
                "status": "error",
                "message": "Unauthorized user. Admin access required."
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Department updated successfully",
                "department": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle DELETE: Remove department
    elif request.method == "DELETE":
        role, error = get_requestor_role(request)
        if error:
            return error
        if role != "admin":
            return Response({
                "status": "error",
                "message": "403 Forbidden - Admin access required"
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            department = Department.objects.get(id=department_id)
            department.delete()
            return Response({
                'message': f"Department '{department.name}' deleted successfully"
            }, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)

