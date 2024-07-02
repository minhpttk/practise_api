from rest_framework import generics,permissions
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from .serializer import UserSerializer,LoginSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist

class RegisterAPI(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] 
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            token = AuthToken.objects.create(user)[1]
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": token
            },)
        except PermissionDenied as e:
            print(f"Permission Denied: {e}")
            raise e
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise e
class LoginAPI(KnoxLoginView):
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
class UserUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    
    def get_object(self):
        try:
            if self.request.user.is_authenticated:
                return self.request.user
            else:
                raise NotFound("User not found")
        except NotFound as e:
            raise e   
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
 
class Get_Me_Info(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        try:
            if self.request.user.is_authenticated:
                return self.request.user
            else:
                raise NotFound("User not found")
        except NotFound as e:
            raise e   
    
    
class UserDeleteAPIView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        try:
            if self.request.user.is_authenticated:
                return self.request.user
            else:
                raise NotFound("User not found")
        except NotFound as e:
            raise e    
    
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message":"Delete Successfull"
        },status=status.HTTP_204_NO_CONTENT)

class UserLogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        AuthToken.objects.filter(user=request.user).delete()
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)