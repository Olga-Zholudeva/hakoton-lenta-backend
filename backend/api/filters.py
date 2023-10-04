from django_filters.rest_framework import FilterSet, filters

from products.models import SalesFact, Forecast, SalesDiff


class SalesFilter(FilterSet):
    st_city_id = filters.CharFilter(
        field_name='st_sku_date__st_id__st_city_id'
    )
    st_id = filters.CharFilter(field_name='st_sku_date__st_id')
    pr_sku_id = filters.CharFilter(field_name='st_sku_date__pr_sku_id')
    pr_group_id = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_group_id'
    )
    pr_cat_id = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_cat_id'
    )
    pr_subcat_id = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_subcat_id'
    )

    class Meta:
        model = SalesFact
        fields = ['st_city_id', 'st_id', 'pr_sku_id', 'pr_group_id',
                  'pr_cat_id', 'pr_subcat_id']


class ForecastFilter(FilterSet):
    st_city_id = filters.CharFilter(
        field_name='st_sku_date__st_id__st_city_id'
    )
    st_id = filters.CharFilter(field_name='st_sku_date__st_id')
    pr_sku_id = filters.CharFilter(field_name='st_sku_date__pr_sku_id')
    pr_group_id = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_group_id'
    )
    pr_cat_id = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_cat_id'
    )
    pr_subcat_id = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_subcat_id'
    )

    class Meta:
        model = Forecast
        fields = ['st_city_id', 'st_id', 'pr_sku_id', 'pr_group_id',
                  'pr_cat_id', 'pr_subcat_id']


class SalesDiffFilter(FilterSet):
    st_city_id = filters.CharFilter(
        field_name='st_sku_date__st_id__st_city_id'
    )
    st_id = filters.CharFilter(field_name='st_sku_date__st_id')
    pr_sku_id = filters.CharFilter(field_name='st_sku_date__pr_sku_id')
    pr_group_id = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_group_id'
    )
    pr_cat_id = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_cat_id'
    )
    pr_subcat_id = filters.CharFilter(
        field_name='st_sku_date__pr_sku_id__pr_subcat_id'
    )

    class Meta:
        model = SalesDiff
        fields = ['st_city_id', 'st_id', 'pr_sku_id', 'pr_group_id',
                  'pr_cat_id', 'pr_subcat_id']
