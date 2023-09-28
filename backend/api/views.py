from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS

from api.serializers import (SalesSerializer, SalesPostSerializer,
                             StoreSerializer, SkuSerializer,
                             ForecastSkuSerializer, ForecastSkuPostSerializer)
from api.filters import SalesFilter, ForecastFilter
from products.models import Sku, Sales, Store, ForecastSku


class SkuViewSet(viewsets.ReadOnlyModelViewSet):
    '''Обработчик для товаров.'''
    queryset = Sku.objects.all()
    serializer_class = SkuSerializer


class SalesViewSet(viewsets.ModelViewSet):
    '''Обработчик для фактических продаж.'''
    queryset = Sales.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SalesFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return SalesSerializer
        return SalesPostSerializer


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    '''Обработчик для магазинов.'''
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class ForecastViewSet(viewsets.ModelViewSet):
    '''Обработчик для прогноза.'''
    queryset = ForecastSku.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ForecastFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ForecastSkuSerializer
        return ForecastSkuPostSerializer
