from django.db.models import Sum
from rest_framework import serializers

from products.models import Sku, Sales, Store, Forecast, ForecastSku


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


class SalesFactSerializer(serializers.ModelSerializer):
    '''Промежуточный сериализатор для агрегации продаж по магазину и товару.'''
    class Meta:
        model = Sales
        fields = ('date', 'sales_type', 'sales_units', 'sales_units_promo',
                  'sales_rub', 'sales_run_promo',)


class SalesSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели с фактом продаж.'''
    store = serializers.CharField(source='st_id')
    sku = serializers.CharField(source='pr_sku_id')
    fact = serializers.SerializerMethodField()

    class Meta:
        model = Sales
        fields = ('store', 'sku', 'fact',)

    def get_fact(self, obj):
        '''Получаем данные по продажам,
           сгруппированные по полям st_id и pr_sku_id.'''
        grouped_sales = Sales.objects.filter(st_id=obj.st_id,
                                             pr_sku_id=obj.pr_sku_id).values(
            'date', 'sales_type').annotate(
            sales_units=Sum('sales_units'),
            sales_units_promo=Sum('sales_units_promo'),
            sales_rub=Sum('sales_rub'),
            sales_run_promo=Sum('sales_run_promo')
        )

        fact_serializer = SalesFactSerializer(grouped_sales, many=True)
        return fact_serializer.data


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
        fields = ('store', 'sku', 'date', 'sales_type', 'sales_units'
                  'sales_units_promo', 'sales_rub', 'sales_run_promo')


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


class ForecastSerializer(serializers.ModelSerializer):
    target = serializers.DecimalField(max_digits=6, decimal_places=1)
    date = serializers.DateField()

    class Meta:
        model = Forecast
        fields = ('date', 'target',)


class ForecastSkuSerializer(serializers.ModelSerializer):
    forecast = serializers.SerializerMethodField()

    class Meta:
        model = ForecastSku
        fields = ('st_id', 'pr_sku_id', 'forecast_date', 'forecast',)

    def get_forecast(self, obj):
        forecast = Forecast.objects.filter(forecast_sku_id=obj)
        return ForecastSerializer(forecast, many=True).data


def set_forecast(forecast_sku, all_forecast):
    Forecast.objects.bulk_create([Forecast(
        forecast_sku_id=forecast_sku,
        date=forecast['date'],
        target=forecast['target']) for forecast in all_forecast])


class ForecastSkuPostSerializer(serializers.ModelSerializer):
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
        model = ForecastSku
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
