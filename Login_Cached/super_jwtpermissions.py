from rest_framework import permissions
from django.core.cache import caches
from django.conf import settings
from .super_jwtviews import prefix_access, cache_db_access, authorization_header


class CustomAuthPermission(permissions.BasePermission):
	##return user_infos, that are some most importants infos of the user: is_staff, id	
	def load_access_token(self, access_token):
		return cache_db_access.get(prefix_access+':'+access_token)

	def validate_request_header(self, request):
		try:
			ola = request.headers[authorization_header]
			return True
		except:
			return False

class IsAdminPermission(CustomAuthPermission):
	def has_permission(self, request, view):
		if self.validate_request_header(request):
			user_infos = self.load_access_token(request.headers[authorization_header])
			if user_infos is not None:
				return user_infos['is_staff']
		return False

class IsOwnerAccountPermission(CustomAuthPermission):
	def has_object_permission(self, request, view, obj):
		if obj is None:
			return False

		if self.validate_request_header(request):
			user_infos = self.load_access_token(request.headers[authorization_header])
			if user_infos is not None:
				if user_infos['id']==obj.id:
					return True
		return False