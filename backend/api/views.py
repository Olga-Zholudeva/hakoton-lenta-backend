from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS

from api.serializers import (SkuSerializer, SalesSerializer, StoreSerializer,
                             ForecastSkuSerializer, ForecastSkuPostSerializer)
from api.filters import SalesFilter
from products.models import Sku, Sales, Store, ForecastSku


class SkuViewSet(viewsets.ReadOnlyModelViewSet):
    '''Обработчик для товаров.'''
    queryset = Sku.objects.all()
    serializer_class = SkuSerializer


class SalesViewSet(viewsets.ReadOnlyModelViewSet):
    '''Обработчик для фактических продаж.'''
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SalesFilter


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    '''Обработчик для магазинов.'''
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class ForecastViewSet(viewsets.ModelViewSet):
    '''Обработчик для прогноза'''
    queryset = ForecastSku.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ForecastSkuSerializer
        return ForecastSkuPostSerializer
