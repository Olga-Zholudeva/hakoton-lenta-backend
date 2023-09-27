import django_filters
from products.models import Sku

class SkuFilter(django_filters.FilterSet):
    pr_group_id = django_filters.CharFilter(field_name='pr_group_id', lookup_expr='startswith')

    class Meta:
        model = Sku
        fields = ['pr_group_id']