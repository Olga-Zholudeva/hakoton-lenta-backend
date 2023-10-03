from django.db.models import Sum
from rest_framework import serializers

from products.models import Sku, Store, Forecast

from django.db.models import Max


class SkuSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели Товар.'''
    sku = serializers.CharField(source='pr_sku_id')
    group = serializers.CharField(source='pr_group_id')
    category = serializers.CharField(source='pr_cat_id')
    subcategory = serializers.CharField(source='pr_subcat_id')
    uom = serializers.IntegerField(source='pr_uom_id')

    class Meta:
        model = Sku
        fields = ('sku', 'group', 'category', 'subcategory', 'uom',)

class StoreSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Магазины.'''
    store = serializers.CharField(source='st_id')
    city = serializers.CharField(source='st_city_id')
    division = serializers.CharField(source='st_division_code')
    type_format = serializers.IntegerField(source='st_type_format_id')
    loc = serializers.IntegerField(source='st_type_loc_id')
    size = serializers.IntegerField(source='st_type_size_id')
    is_active = serializers.IntegerField(source='st_is_active')

    class Meta:
        model = Store
        fields = ('store', 'city', 'division', 'type_format', 'loc', 'size',
                  'is_active',)
class FarecastSkuSerializer(serializers.ModelSerializer):
    date = serializers.CharField(source='st_sku_date.date')
    class Meta:
        model = Forecast
        fields = ('date', 'sales_units',)


class ForecastSerializer(serializers.ModelSerializer):
    '''Сериализатор для страницы с прогнозом продаж'''
    st_id = serializers.CharField(
        source='st_sku_date.st_id'
    )
    pr_group_id = serializers.CharField(source='st_sku_date.pr_sku_id.pr_group_id')
    pr_cat_id = serializers.CharField(source='st_sku_date.pr_sku_id.pr_cat_id')
    subcategory = serializers.CharField(source='st_sku_date.pr_sku_id.pr_subcat_id')
    pr_sku_id = serializers.CharField(
        source='st_sku_date.pr_sku_id'
    )
    forecast = serializers.SerializerMethodField()
    class Meta:
        model = Forecast
        fields = ('st_id', 'pr_group_id', 'pr_cat_id', 'subcategory', 'pr_sku_id', 'forecast',)
    
    def get_forecast(self, obj):
        last_forecast = Forecast.objects.aggregate(Max('forecast_date'))['forecast_date__max']
        forecast = Forecast.objects.filter(
            forecast_date = last_forecast,
            st_sku_date__st_id=obj.st_sku_date.st_id,
            st_sku_date__pr_sku_id=obj.st_sku_date.pr_sku_id
        )
        return FarecastSkuSerializer(forecast, many=True).data

