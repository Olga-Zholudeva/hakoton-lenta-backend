from django_filters.rest_framework import FilterSet, filters

from products.models import SalesFact, Forecast, SalesDiff, Store, Sku


class SalesFilter(FilterSet):
    city = filters.MultipleChoiceFilter(
        field_name='st_sku_date__st_id__st_city_id',
        # choices=Store.objects.values_list('st_city_id', 'st_city_id')
    )
    store = filters.MultipleChoiceFilter(
        field_name='st_sku_date__st_id',
        # choices=Store.objects.values_list('st_id', 'st_id')
    )
    sku = filters.MultipleChoiceFilter(
        field_name='st_sku_date__pr_sku_id',
        # choices=Sku.objects.values_list('pr_sku_id', 'pr_sku_id')
    )
    group = filters.MultipleChoiceFilter(
        field_name='st_sku_date__pr_sku_id__pr_group_id',
        # choices=Sku.objects.values_list('pr_group_id', 'pr_group_id')
    )
    category = filters.MultipleChoiceFilter(
        field_name='st_sku_date__pr_sku_id__pr_cat_id',
        # choices=Sku.objects.values_list('pr_cat_id', 'pr_cat_id')
    )
    subcategory = filters.MultipleChoiceFilter(
        field_name='st_sku_date__pr_sku_id__pr_subcat_id',
        # choices=Sku.objects.values_list('pr_subcat_id', 'pr_subcat_id')
    )
    date_from = filters.DateFilter(field_name='st_sku_date__date',
                                   lookup_expr='gte')
    date_to = filters.DateFilter(field_name='st_sku_date__date',
                                 lookup_expr='lte')


class SalesFilter(SalesFilter):
    class Meta:
        model = SalesFact
        fields = ['city', 'store', 'sku', 'group',
                  'category', 'subcategory', 'date_from', 'date_to']


class ForecastFilter(SalesFilter):
    forecast_date = filters.DateFilter(field_name='forecast_date')

    class Meta:
        model = Forecast
        fields = ['city', 'store', 'sku', 'group', 'category', 'subcategory',
                  'date_from', 'date_to', 'forecast_date']


class SalesDiffFilter(SalesFilter):
    class Meta:
        model = SalesDiff
        fields = ['city', 'store', 'sku', 'group',
                  'category', 'subcategory', 'date_from', 'date_to']
