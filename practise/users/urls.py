
from django.urls import path
from .views import RegisterView,LoginView,MeInfoView,UserUpdateView,UserLogoutView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/get_me_info/',MeInfoView.as_view(),name='get_me'),
    path('api/update/', UserUpdateView.as_view(), name='user-update'),
    path('api/logout/',UserLogoutView.as_view(),name="logout")
]