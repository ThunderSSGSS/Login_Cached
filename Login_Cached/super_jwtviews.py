from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.core.cache import caches

def authentication_fail():
	return {'status':'authentication fail'}

def refresh_fail():
	return {'status':'not authorized'}

"""
#ON SETTINGS:
CACHED_JWT_NAME_REFRESH => str, name of cache refresh, default='default'
CACHED_JWT_NAME_ACCESS => str, name of cache access, default=CACHED_JWT_NAME

CACHED_JWT_ACCESS_TIMEOUT=> int, seconds access timeout, default=300
CACHED_JWT_REFRESH_TIMEOUT=> int, seconds refresh timeout, default= 3600

CACHED_JWT_ACCESS_PREFIX => str, access prefix, default='access'
CACHED_JWT_REFRESH_PREFIX => str, refresh prefix, default='refresh'

CACHED_JWT_HEADER => str, the token header, default='Authorization'
"""
cache_db_refresh = caches[getattr(settings,'CACHED_JWT_NAME_REFRESH','default')]
cache_db_access = caches[getattr(settings,'CACHED_JWT_NAME_ACCESS','default')]

prefix_refresh=getattr(settings,'CACHED_JWT_REFRESH_PREFIX','refresh')
prefix_access=getattr(settings,'CACHED_JWT_ACCESS_PREFIX','access')

timeout_access=getattr(settings,'CACHED_JWT_ACCESS_TIMEOUT',300)
timeout_refresh=getattr(settings,'CACHED_JWT_REFRESH_TIMEOUT',3600)

authorization_header = getattr(settings,'CACHED_JWT_HEADER','Authorization')


#AUTHENTICATE#####################################################################
class ObtainJWTPairView(APIView):
	#For validate username and password
	serializer_class=None

	##User_infos are some most importants infos of the user: is_staff, id
	def save_tokens(self, tokens, user_infos):
		cache_db_refresh.set(prefix_refresh+':'+tokens['refresh'],user_infos,timeout=timeout_refresh)
		cache_db_access.set(prefix_access+':'+tokens['access'],user_infos,timeout=timeout_access)

	def create_tokens(self, request):
		user = authenticate(request,username=request.data['username'],password=request.data['password'])
		if user is not None:
			refresh = RefreshToken.for_user(user)
			tokens =  {'refresh': str(refresh), 'access': str(refresh.access_token)}
			user_infos = {'id':user.id, 'is_staff': user.is_staff}
			self.save_tokens(tokens,user_infos)
			return tokens
		return None

	def post(self,request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			tokens =  self.create_tokens(request)
			if tokens is None:
				return Response(authentication_fail(), status=status.HTTP_400_BAD_REQUEST)
			return Response(tokens, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
	#For validate refresh
	serializer_class=None
	user_model = None

	def load_refresh_token(self, refresh_token):
		return cache_db_refresh.get(prefix_refresh+':'+refresh_token)

	##User_infos are some most importants infos of the user: is_staff, id
	def save_tokens(self,tokens,user_infos):
		cache_db_access.set(prefix_access+':'+tokens['access'],user_infos,timeout=timeout_access)

	def get_user(self, user_id):
		try:
			return  self.user_model.objects.get(id=user_id)
		except self.user_model.DoesNotExist:
			return None

	def refresh_tokens(self, request_data):
		user_infos = self.load_refresh_token(request_data['refresh'])
		if user_infos is not None:
			user = self.get_user(user_infos['id'])
			if user is not None:
				tokens= RefreshToken.for_user(user)
				refreshed_tokens = {'access':str(tokens.access_token)}
				self.save_tokens(refreshed_tokens,user_infos)
				return refreshed_tokens
		return None

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			refreshed_tokens = self.refresh_tokens(request.data)
			if refreshed_tokens is None:
				return Response(refresh_fail(), status=status.HTTP_400_BAD_REQUEST)
			return Response(refreshed_tokens, status=status.HTTP_200_OK)
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)