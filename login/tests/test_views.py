from django.test import TestCase
from login.models import CustomUser
from Login_Cached import super_tests
# Create your tests here

class TestUser(super_tests.TestAPI):
	model_class = CustomUser
	post_dict = {
		'username':'thunderssgss',
		'fist_name':'',
		'last_name':'',
		'email':'ojamesartur@gmail.com',
		'password':'Original'
	}
	attribute_test_name='username'
	detail_link_name='detail_user'
	list_link_name='list_user'
