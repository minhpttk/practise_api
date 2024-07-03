from django.urls import path
from .views import *


urlpatterns=[
    path('api/create_employee/',CreateEmployeeView.as_view(),name="create_employees"),
    path('api/filter_employee/',FilterEmployeeView.as_view(),name="filer_list"),
    path('api/get_one_employee/<int:employee_id>/', GetOneEmployeeDetailView.as_view(), name='employee-detail'),
    path('api/update_employee/<int:employee_id>/',UpdateEmployeeUpdateView.as_view(),name="update_employee"),
    path('api/soft_delete_employee/<int:employee_id>/', SoftDeleteEmployeeView.as_view(), name='soft-delete-employee'),
]