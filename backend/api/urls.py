from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (SkuViewSet, StoreViewSet, ForecastViewSet, SalesViewSet,
                       SalesDiffViewSet)


router = DefaultRouter()

router.register('categories', SkuViewSet)
router.register('sales', SalesViewSet)
router.register('shops', StoreViewSet)
router.register('forecast', ForecastViewSet)
router.register('salesdiff', SalesDiffViewSet)

urlpatterns = [
    path('api/auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('api/', include(router.urls)),
]
