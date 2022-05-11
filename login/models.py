from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse 
import uuid
# Create your models here.

class CustomUser(AbstractUser):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4)

	def new_password(self):
		return None

	def get_absolute_url(self):
		return reverse("detail_user",kwargs={"pk":self.id})