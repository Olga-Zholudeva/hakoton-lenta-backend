from rest_framework import viewsets
from products.models import Sku
from api.serializers import SkuSerializer


class SkuViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sku.objects.all()
    serializer_class = SkuSerializer
