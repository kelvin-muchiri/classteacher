"""classteacher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.views.static import serve

from users.views import (
    UserCreateAPIView,
    UserLoginAPIView,
    UserRetrieveUpdateAPIView,
)

authpatterns = [
    path(r'accounts/', include('rest_framework.urls')),
    path(r'register/', UserCreateAPIView.as_view(), name='register'),
    path(r'login/', UserLoginAPIView.as_view(), name='login'),
    path(r'me/', UserRetrieveUpdateAPIView.as_view()),
]


apipatterns = [
    path(r'users/', include('users.urls')),
    path(r'auth/', include(authpatterns)),
    path(r'classes/', include('classes.urls')),
    path(r'students/', include('students.urls')),
    path(r'subjects/', include('subjects.urls')),
]

urlpatterns = [
    path(r'api/', include(apipatterns)),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

