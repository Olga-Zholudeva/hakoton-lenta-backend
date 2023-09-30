from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import SkuViewSet, SalesViewSet, StoreViewSet, ForecastViewSet


router_v1 = DefaultRouter()

router_v1.register('categories', SkuViewSet)
router_v1.register('sales', SalesViewSet)
router_v1.register('shops', StoreViewSet)
router_v1.register('forecast', ForecastViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
