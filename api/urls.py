"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from apps.outlook.views import OutlookAuthViewSet, OutlookMessageViewSet

router = DefaultRouter()
router.register(r'outlook-auth', OutlookAuthViewSet, basename='outlook-auth')
router.register(r'outlook-message', OutlookMessageViewSet, basename='outlook-message')

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
