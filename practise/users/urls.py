
from django.urls import path, include
from .views import RegisterView,LoginView,UserLogoutView,UserDetailListView

urlpatterns = [
    path("users/", include([
        path("register", RegisterView.as_view(), name="register"),
        path("user-details",UserDetailListView.as_view(),name="user_detail"),
        path('login', LoginView.as_view(), name="login"),
        path('logout',UserLogoutView.as_view(),name="logout")
    ]))

]