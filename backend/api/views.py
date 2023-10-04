from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.permissions import SAFE_METHODS

from api.serializers import (SalesSerializer, SalesPostSerializer,
                             StoreSerializer, SkuSerializer,
                             ForecastSerializer, ForecastPostSerializer,
                             SalesDiffSerializer)
from api.filters import SalesFilter, ForecastFilter, SalesDiffFilter
from products.models import Sku, SalesFact, Store, Forecast, SalesDiff


class StoreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    '''Обработчик для магазинов'''
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class SkuViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    '''Обработчик для товаров'''
    queryset = Sku.objects.all()
    serializer_class = SkuSerializer


class SalesViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    '''Обработчик для фактических продаж'''
    queryset = SalesFact.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SalesFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return SalesSerializer
        return SalesPostSerializer


class ForecastViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    '''Обработчик для прогноза'''
    queryset = Forecast.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ForecastFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ForecastSerializer
        return ForecastPostSerializer


class SalesDiffViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    '''Обработчик для качества'''
    queryset = SalesDiff.objects.all()
    serializer_class = SalesDiffSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SalesDiffFilter
