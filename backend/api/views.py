from rest_framework import viewsets
from products.models import Sku, Sales
from api.serializers import SkuSerializer, SalesSerializer



class SkuViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sku.objects.all()
    serializer_class = SkuSerializer


class SalesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
