from .models import Employee
from django.db.models import Q


def get_object(id):
        try:
            return Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            return None
        
def get_list_employees(data):
    fullname = data.query_params.get('fullname')
    date_of_birth = data.query_params.get('date_of_birth')
    gender = data.query_params.get('gender')
    profile_picture = data.query_params.get('profile_picture')
    
    valid_genders = {'male', 'm', 'female', 'f', 'other', 'o'}
    
    filters = Q()
    
    if fullname:
        filters &= Q(fullname__icontains=fullname)
        
    if date_of_birth:
        year = int(date_of_birth)
        filters &= Q(date_of_birth__year=year)
    
    if gender and gender.lower() in valid_genders:
        filters &= Q(gender__iexact=gender.lower())
    
    if profile_picture:
        filters &= Q(profile_picture=profile_picture)
    
    employees = Employee.objects.filter(filters)  # Lấy danh sách nhân viên
    
    return employees
