from django.contrib import admin
from django.urls import include, path

from django.urls import path, include
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Создайте router и зарегистрируйте ваши views и url-ы
router = routers.DefaultRouter(trailing_slash=False)

# Определение schema_view для использования в Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation for your project",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('api.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # Путь к документации ReDoc
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
