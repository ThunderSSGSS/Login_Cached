from rest_framework import serializers
from login.models import CustomUser
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.validators import UniqueValidator

class UserAdminSerializer(serializers.ModelSerializer):
	username = serializers.CharField(max_length=120, 
		validators=[UniqueValidator(queryset=CustomUser.objects.all())])
	email= serializers.EmailField(
		validators=[UniqueValidator(queryset=CustomUser.objects.all())])

	first_name = serializers.CharField(max_length=50, required=False, allow_blank=True)
	last_name= serializers.CharField(max_length=50,required=False, allow_blank=True)
	is_superuser= serializers.BooleanField(default=False, required=False)
	is_staff= serializers.BooleanField(default=False, required=False)
	is_active=serializers.BooleanField(default=True, required=False)
	password = serializers.CharField(min_length=6,max_length=128,write_only=True)

	class Meta:
		model = CustomUser
		fields =  ['id','username','password','first_name','last_name','email','is_superuser','is_staff','is_active','date_joined']

	def hash_password(self, validated_data_password):
		validated_data_password = make_password(validated_data_password)
		return validated_data_password

	def compare_password(self, instance, validated_data):
		return check_password(validated_data['password'], instance.password)

	#create
	def create(self, validated_data):
		validated_data['password'] = self.hash_password(validated_data['password'])
		return super().create(validated_data)

	#update
	#compare the password, then change the field password to new_password
	def update(self, instance, validated_data):
		if self.compare_password(instance,validated_data):
			validated_data['password'] = self.hash_password(validated_data['password'])
			return super().update(instance,validated_data)
		return instance


class UserSerializer(UserAdminSerializer):
	is_superuser= None
	is_staff= None
	is_active= None

	class Meta:
		model = CustomUser
		fields= ['id','username','password','first_name','last_name','email']

	#create
	def create(self, validated_data):
		validated_data['is_superuser']=False
		validated_data['is_staff']=False
		validated_data['is_active']=True
		return super().create(validated_data)



#ONLY FOR VALIDATION to ObtainJWTPair view
class LoginSerializer(serializers.ModelSerializer):
	username = serializers.CharField(max_length=120)
	password = serializers.CharField(max_length=128)

	class Meta:
		model = CustomUser
		fields= ['username','password']

#ONLY FOR RefreshToken view
class RefreshSerializer(serializers.ModelSerializer):
	refresh = serializers.CharField()

	class Meta:
		model = CustomUser
		fields= ['refresh']