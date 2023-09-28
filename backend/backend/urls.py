from django.contrib import admin
from django.urls import include, path

from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('api.urls')),
]