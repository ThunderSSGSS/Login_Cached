from django.shortcuts import render
from login.api import serializers
from Login_Cached import super_jwtpermissions
from Login_Cached import super_jwtviews
from login.models import CustomUser
from rest_framework import generics
from rest_framework import mixins

# Create your views here.


####ADMIN
class ListUser(generics.ListCreateAPIView):
	permission_classes = [super_jwtpermissions.IsAdminPermission]
	serializer_class = serializers.UserAdminSerializer
	queryset = CustomUser.objects.all()

class DetailUser(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = [super_jwtpermissions.IsAdminPermission]
	serializer_class  = serializers.UserAdminSerializer
	queryset = CustomUser.objects.all()

###Normal
class SignUp(mixins.CreateModelMixin, generics.GenericAPIView):
	serializer_class = serializers.UserSerializer

	def post(self, request, *args, **kwargs):
		return self.create(request,*args,**kwargs)

class MyInfo(mixins.RetrieveModelMixin, 
	mixins.UpdateModelMixin, generics.GenericAPIView):
	permission_classes = [super_jwtpermissions.IsOwnerAccountPermission]
	serializer_class = serializers.UserSerializer
	queryset = CustomUser.objects.all()

	def get(self, request, *args, **kwargs):
		return self.retrieve(request,*args,**kwargs)

	def put(self, request, *args, **kwargs):
		return self.update(request,*args,**kwargs)

#Authenticate
class ObtainJWTPair(super_jwtviews.ObtainJWTPairView):
	serializer_class = serializers.LoginSerializer

class RefreshToken(super_jwtviews.RefreshTokenView):
	serializer_class  = serializers.RefreshSerializer
	user_model = CustomUser