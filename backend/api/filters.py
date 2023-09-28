from django_filters.rest_framework import FilterSet, filters

from products.models import Sales, ForecastSku


class SalesFilter(FilterSet):
    st_id = filters.CharFilter()
    pr_sku_id = filters.CharFilter(field_name='pr_sku_id__pr_group_id')
    pr_cat_id = filters.CharFilter(field_name='pr_sku_id__pr_cat_id')
    pr_subcat_id = filters.CharFilter(field_name='pr_sku_id__pr_subcat_id')

    class Meta:
        model = Sales
        fields = ['st_id', 'pr_sku_id', 'pr_cat_id', 'pr_subcat_id']


class ForecastFilter(FilterSet):
    st_id = filters.CharFilter()
    pr_sku_id = filters.CharFilter()
    forecast_date = filters.DateFilter()

    class Meta:
        model = ForecastSku
        fields = ['st_id', 'pr_sku_id', 'forecast_date']
