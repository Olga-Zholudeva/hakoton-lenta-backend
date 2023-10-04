from django.db.models import Max, Sum
from rest_framework import serializers

from products.models import Sku, Store, Forecast, SalesFact


class SkuSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели Товар'''
    sku = serializers.CharField(source='pr_sku_id')
    group = serializers.CharField(source='pr_group_id')
    category = serializers.CharField(source='pr_cat_id')
    subcategory = serializers.CharField(source='pr_subcat_id')
    uom = serializers.IntegerField(source='pr_uom_id')

    class Meta:
        model = Sku
        fields = ('sku', 'group', 'category', 'subcategory', 'uom',)


class StoreSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Магазины'''
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


class ForecastSkuSerializer(serializers.ModelSerializer):
    date = serializers.CharField(source='st_sku_date.date')

    class Meta:
        model = Forecast
        fields = ('date', 'sales_units',)


class ForecastSerializer(serializers.ModelSerializer):
    '''Сериализатор для страницы с прогнозом продаж'''
    store = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_sku_date.st_id'
    )
    group = serializers.CharField(
        source='st_sku_date.pr_sku_id.pr_group_id'
    )
    category = serializers.CharField(
        source='st_sku_date.pr_sku_id.pr_cat_id'
    )
    subcategory = serializers.CharField(
        source='st_sku_date.pr_sku_id.pr_subcat_id'
    )
    sku = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_sku_date.pr_sku_id'
    )
    forecast = serializers.SerializerMethodField()

    class Meta:
        model = Forecast
        fields = ('store', 'group', 'category', 'subcategory',
                  'sku', 'forecast',)

    def get_forecast(self, obj):
        last_forecast = Forecast.objects.aggregate(
            Max('forecast_date')
        )['forecast_date__max']
        forecast = Forecast.objects.filter(
            forecast_date=last_forecast,
            st_sku_date__st_id=obj.st_sku_date.st_id,
            st_sku_date__pr_sku_id=obj.st_sku_date.pr_sku_id
        )
        return ForecastSkuSerializer(forecast, many=True).data


class ForecastPostSerializer(serializers.ModelSerializer):
    store = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_id',
    )
    sku = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='pr_sku_id',
    )
    forecast_date = serializers.DateField()
    forecast = ForecastSerializer(many=True,)

    class Meta:
        model = Forecast
        fields = ('store', 'sku', 'forecast_date', 'forecast')

    def create(self, validated_data):
        all_forecast = validated_data.pop('forecast')
        forecast_sku = ForecastSku.objects.create(
            st_id=validated_data['store'],
            pr_sku_id=validated_data['sku'],
            forecast_date=validated_data['forecast_date']
        )
        set_forecast(forecast_sku, all_forecast)
        return forecast_sku


class SalesSerializer(serializers.ModelSerializer):
    '''Сериализатор факта продаж'''
    store = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_sku_date.st_id'
    )
    sku = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_sku_date.pr_sku_id'
    )
    date = serializers.DateTimeField(source='st_sku_date.date')

    class Meta:
        model = SalesFact
        fields = ('store', 'sku', 'date', 'sales_type', 'sales_units',
                  'sales_units_promo', 'sales_rub', 'sales_run_promo')


class SalesPostSerializer(serializers.ModelSerializer):
    '''Сериализатор загрузки факта продаж.'''
    store = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_id',
    )
    sku = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='pr_sku_id',
    )
    date = serializers.DateField()
    sales_type = serializers.IntegerField(min_value=0, max_value=1)
    sales_units = serializers.DecimalField(max_digits=6, decimal_places=1)
    sales_units_promo = serializers.DecimalField(max_digits=6,
                                                 decimal_places=1)
    sales_rub = serializers.DecimalField(max_digits=8, decimal_places=1)
    sales_run_promo = serializers.DecimalField(max_digits=8, decimal_places=1)

    class Meta:
        model = Sales
        fields = ('store', 'sku', 'date', 'sales_type', 'sales_units',
                  'sales_units_promo', 'sales_rub', 'sales_run_promo')
