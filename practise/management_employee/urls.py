from django.urls import path,include
from .views import *


urlpatterns=[
    path("management/",include([
        path("employees", EmployeesListView.as_view(),name="employees_list_view"),
        path("employees/<int:id>",EmployeesDetailView.as_view(),name="employees_detail_view")
    ]))

   
]