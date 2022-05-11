from django.test import TestCase
#from django.contrib.auth.models import User
from django.urls import reverse
import json

class TestAPI(TestCase):
	#7e63638f-64c5-4220-9d9b-e99970893a6c
	model_class=None
	
	#The dict contaim the new valid data test
	post_dict = None

	#Example, 'first_name'
	#This attribute must be a string and must accept 3 characters minimum
	attribute_test_name=None
	
	#Ex, 'owner_detail'
	#Remember, detail link must accept methods: GET, DELETE and PUT
	detail_link_name=None
	
	#Ex, 'owner_list'
	#Remember, lists link must accept methods: GET and POST
	list_link_name=None

	#@classmethod
	#def setUpTestData(cls):
	#	user = User.objects.create_user("genericuser","","Original2001#")
	#def setUp(self):
	#	pass	
		
	def get_object(self, value):
		try:
			data={self.attribute_test_name:value}
			return self.model_class.objects.get(**data)
		except self.model_class.DoesNotExist:
			return None

	def object_exist(self, value):
		object=self.get_object(value)
		if object is None:
			return False
		return True

	#Test ADD
	def test_add(self):
		response = self.client.post(reverse(self.list_link_name),
			data=json.dumps(self.post_dict),content_type='application/json')
		self.assertEqual(response.status_code,201)

	#Test List
	def test_list(self):
		self.test_add()

		response = self.client.get(reverse(self.list_link_name))
		self.assertEqual(response.status_code,200)

	#Test not Found
	def test_not_found(self):
		response = self.client.get(reverse(self.detail_link_name,
			kwargs={"pk":'7e63638f-64c5-4220-9d9b-e99970893a6c'}))
		self.assertEqual(response.status_code,404)
	
	#Test Get
	def test_get(self):
		self.test_add()
		
		value = self.post_dict[self.attribute_test_name]
		self.assertTrue(self.object_exist(value))

		object = self.get_object(value)
		#Test get_absolute_url
		response = self.client.get(object.get_absolute_url())
		self.assertEqual(response.status_code,200)

	
	#Test Put
	def test_alter(self):
		self.test_add()

		value = self.post_dict[self.attribute_test_name]
		self.assertTrue(self.object_exist(value))

		object = self.get_object(value)
		self.post_dict[self.attribute_test_name] = 'Jam'

		response = self.client.put(object.get_absolute_url(),
			data=json.dumps(self.post_dict),content_type='application/json')
		self.assertEqual(response.status_code,200)
	
	#Test Delete
	def test_delete(self):
		self.test_alter()

		self.assertTrue(self.object_exist('Jam'))
		object = self.get_object('Jam')
		
		response = self.client.delete(object.get_absolute_url())
		self.assertEqual(response.status_code,204)