from django_filters.rest_framework import FilterSet, filters

from products.models import SalesFact, Forecast, SalesDiff


class SalesFilter(FilterSet):
    city = filters.CharFilter(
        field_name='st_sku_date__st_id__st_city_id'
    )
    store = filters.CharFilter(field_name='st_sku_date__st_id')
    sku = filters.CharFilter(field_name='st_sku_date__pr_sku_id')
    group = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_group_id'
    )
    category = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_cat_id'
    )
    subcategory = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_subcat_id'
    )
    date_from = filters.DateFilter(field_name='st_sku_date__date',
                                   lookup_expr='gte')
    date_to = filters.DateFilter(field_name='st_sku_date__date',
                                 lookup_expr='lte')

    class Meta:
        model = SalesFact
        fields = ['city', 'store', 'sku', 'group',
                  'category', 'subcategory', 'date_from', 'date_to']


class ForecastFilter(FilterSet):
    city = filters.CharFilter(
        field_name='st_sku_date__st_id__st_city_id'
    )
    store = filters.CharFilter(field_name='st_sku_date__st_id')
    sku = filters.CharFilter(field_name='st_sku_date__pr_sku_id')
    group = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_group_id'
    )
    category = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_cat_id'
    )
    subcategory = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_subcat_id'
    )
    date_from = filters.DateFilter(field_name='st_sku_date__date',
                                   lookup_expr='gte')
    date_to = filters.DateFilter(field_name='st_sku_date__date',
                                 lookup_expr='lte')
    forecast_date = filters.DateFilter(field_name='forecast_date')

    class Meta:
        model = Forecast
        fields = ['city', 'store', 'sku', 'group', 'category', 'subcategory',
                  'date_from', 'date_to', 'forecast_date']


class SalesDiffFilter(FilterSet):
    city = filters.CharFilter(
        field_name='st_sku_date__st_id__st_city_id'
    )
    store = filters.CharFilter(field_name='st_sku_date__st_id')
    sku = filters.CharFilter(field_name='st_sku_date__pr_sku_id')
    group = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_group_id'
    )
    category = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_cat_id'
    )
    subcategory = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_subcat_id'
    )
    date_from = filters.DateFilter(field_name='st_sku_date__date',
                                   lookup_expr='gte')
    date_to = filters.DateFilter(field_name='st_sku_date__date',
                                 lookup_expr='lte')

    class Meta:
        model = SalesDiff
        fields = ['city', 'store', 'sku', 'group',
                  'category', 'subcategory', 'date_from', 'date_to']
