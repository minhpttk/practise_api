from rest_framework import generics,permissions
from rest_framework.response import Response
from knox.models import AuthToken  
from django.contrib.auth import login
from .serializer import UserSerializer,LoginSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
class RegisterView(APIView): # APIView
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] 

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            token = AuthToken.objects.create(user)[1]
            return Response({ 
                "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
                "token": token
            },)
        except PermissionDenied as e:
            print(f"Permission Denied: {e}")
            raise e
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise e
        

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        _, token = AuthToken.objects.create(user)
        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "token": token
        })
    
    
class UserUpdateView(APIView):
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
    
    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            user=serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({
                "user":user
            }, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    def perform_update(self, serializer):
        serializer.save()

class MeInfoView(APIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
        
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user)
        return Response(serializer.data)


class UserLogoutView(APIView):

    def post(self, request, format=None):
        AuthToken.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
