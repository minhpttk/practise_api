
from django.urls import path
from .views import RegisterAPI,LoginAPI,Get_Me_Info,UserUpdateAPIView,UserDeleteAPIView,UserLogoutAPIView

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/get_me_info/<int:id>/',Get_Me_Info.as_view(),name='get_me'),
    path('api/update/<int:id>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('api/delete/<int:id>/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('api/logout/',UserLogoutAPIView.as_view(),name="logout")
]