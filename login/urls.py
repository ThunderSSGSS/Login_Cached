"""Login_Cached URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views

urlpatterns = [
	path('authenticate/',views.ObtainJWTPair.as_view(),name='authenticate'),
	path('refresh/',views.RefreshToken.as_view(), name='refresh'),
	
    #Normal
    path('signup/',views.SignUp.as_view(), name='signup'),
    path('infos/<uuid:pk>',views.MyInfo.as_view(), name='my_info'),

    #Admins
	path('admin/users/',views.ListUser.as_view(),name='list_user'),
	path('admin/user/<uuid:pk>',views.DetailUser.as_view(),name='detail_user')
]
