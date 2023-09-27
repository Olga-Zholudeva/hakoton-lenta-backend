from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from api.views import SkuViewSet, SalesViewSet

router = DefaultRouter()

router.register('categories', SkuViewSet)
router.register('sales', SalesViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
