from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import SkuViewSet, SalesViewSet, StoreViewSet, ForecastViewSet


router = DefaultRouter()

router.register('categories', SkuViewSet)
router.register('sales', SalesViewSet)
router.register('shops', StoreViewSet)
router.register('forecast', ForecastViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
