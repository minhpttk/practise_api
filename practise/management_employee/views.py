from rest_framework import permissions
from .serializers import *
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination
from .models import Employee
from .service import *
# Create your views here.


class EmployeesListView(APIView):   
    
    serializer_class=EmployeesListSerializer
    pagination_class = LimitOffsetPagination 
    permission_classes = [permissions.AllowAny] 

    def get(self, request):
        employees=get_list_employees(request)
        paginator = self.pagination_class()
        paginator.default_limit = 10  # Đặt giới hạn mặc định
        page = paginator.paginate_queryset(employees, request)
        if page is not None:
            serializer = EmployeesListSerializer(page, many=True) 
            return paginator.get_paginated_response(serializer.data)
        serializer = EmployeesListSerializer(employees, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            employee = serializer.save()
            # Serialize the employee instance before returning
            employee_data = EmployeesListSerializer(employee).data
            return Response({ 
                "employee":employee_data
            })
        except PermissionDenied as e:
            print(f"Permission Denied: {e}")
            raise e

class EmployeesDetailView(APIView):
    
    permission_classes = [permissions.AllowAny] 
        
    def get(self, request, id):
        employee = get_object(id)
        if not employee:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GetOneEmployeeSerializer(employee)
 
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        employee = get_object(id)
        if not employee:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UpdateEmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, id):
        try:
            employee = get_object(id=id)
            serializer = SoftDeleteEmployeeSerializer(data={'deleted': True})
            if serializer.is_valid():
                employee.deleted = serializer.validated_data['deleted']
                employee.save()
                return Response({"message": "Employee soft deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
    
