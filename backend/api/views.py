from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.permissions import SAFE_METHODS

from api.serializers import (
                             StoreSerializer, SkuSerializer, ForecastSerializer
                             )
from api.filters import ForecastFilter
from products.models import Sku, Store, Forecast


class SkuViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    '''Обработчик для товаров.'''
    queryset = Sku.objects.all()
    serializer_class = SkuSerializer

class ForecastViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    '''Обработчик для прогноза'''
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ForecastFilter

class StoreViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet 
):
    '''Обработчик для магазинов.'''
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

