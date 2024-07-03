from rest_framework import permissions
from .serializers import *
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .models import Employee
# Create your views here.


class CreateEmployeeView(APIView):
    serializer_class= CreatEmployeeSerializer
    permission_classes = [permissions.AllowAny] 

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            employee = serializer.save()
            # Serialize the employee instance before returning
            employee_data = CreatEmployeeSerializer(employee).data
            return Response({ 
                "employee":employee_data
            })
        except PermissionDenied as e:
            print(f"Permission Denied: {e}")
            raise e
        

class FilterEmployeeView(APIView):
    serializer_class= FilterEmployeeSerializer 
    pagination_class = PageNumberPagination
    permission_classes = [permissions.AllowAny] 
    
    def get(self, request):
        # Lấy các tham số lọc từ request
        fullname = request.query_params.get('fullname')
        date_of_birth = request.query_params.get('date_of_birth')
        gender = request.query_params.get('gender')
        profile_picture = request.query_params.get('profile_picture')
        #Giá trị gender hợp lệ
        valid_genders = {'male', 'm', 'female', 'f', 'other', 'o'}
        # Tạo query filter
        filters = Q()
        if fullname:
            filters &= Q(fullname__icontains=fullname)
        if date_of_birth:
            year = int(date_of_birth)
            filters &= Q(date_of_birth__year=year)
        if gender and gender.lower() in valid_genders:
            filters &= Q(gender__iexact=gender.lower())
        if profile_picture:
            filters &= Q(profile_picture=profile_picture )
        employees = Employee.objects.filter(filters) # Lấy danh sách nhân viên
        paginator = self.pagination_class() # Phân trang
        page = paginator.paginate_queryset(employees, request)
        serializer = FilterEmployeeSerializer(page, many=True) # Serialize và trả về dữ liệu
        return paginator.get_paginated_response(serializer.data)


class GetOneEmployeeDetailView(APIView):
    permission_classes = [permissions.AllowAny] 

    def get_object(self, employee_id):
        try:
            return Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return None
    
    def get(self, request, employee_id):
        employee = self.get_object(employee_id)
        if not employee:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GetOneEmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateEmployeeUpdateView(APIView):
    permission_classes = [permissions.AllowAny] 

    def get_object(self, employee_id):
        try:
            return Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return None
    
    def put(self, request, employee_id):
        employee = self.get_object(employee_id)
        if not employee:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UpdateEmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SoftDeleteEmployeeView(APIView):
    permission_classes = [permissions.AllowAny] 

    def post(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
            serializer = SoftDeleteEmployeeSerializer(data={'deleted': True})
            if serializer.is_valid():
                employee.deleted = serializer.validated_data['deleted']
                employee.save()
                return Response({"message": "Employee soft deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)