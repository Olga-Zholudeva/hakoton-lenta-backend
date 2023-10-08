from datetime import date

from django.db import models
from django.db.models import Max, Sum
from django.db.models.functions import Coalesce
from rest_framework import serializers

from products.models import Sku, Store, Forecast, SalesFact, Sales, SalesDiff
from products.management.setup_logger import setup_logger


logger = setup_logger()


def set_diff(sale):
    obj, created = SalesDiff.objects.get_or_create(st_sku_date=sale)
    obj.save


class SkuSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели Товар'''
    pr_sku_id = serializers.CharField(max_length=200)
    pr_group_id = serializers.CharField(max_length=200)
    pr_cat_id = serializers.CharField(max_length=200)
    pr_subcat_id = serializers.CharField(max_length=200)
    pr_uom_id = serializers.IntegerField()

    class Meta:
        model = Sku
        fields = ('pr_sku_id', 'pr_group_id', 'pr_cat_id', 'pr_subcat_id',
                  'pr_uom_id')


class StoreSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Магазины'''
    st_id = serializers.CharField(max_length=200)
    st_city_id = serializers.CharField(max_length=200)
    st_division_code = serializers.CharField(max_length=200)
    st_type_format_id = serializers.IntegerField()
    st_type_loc_id = serializers.IntegerField()
    st_type_size_id = serializers.IntegerField()
    st_is_active = serializers.IntegerField()

    class Meta:
        model = Store
        fields = ('st_id', 'st_city_id', 'st_division_code',
                  'st_type_format_id', 'st_type_loc_id', 'st_type_size_id',
                  'st_is_active')


class ForecastSkuSerializer(serializers.ModelSerializer):
    date = serializers.DateField(read_only=True, source='st_sku_date.date')

    class Meta:
        model = Forecast
        fields = ('date', 'sales_units')


class ForecastSerializer(serializers.ModelSerializer):
    '''Сериализатор для вывода прогноза продаж'''
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
                  'sku', 'forecast')

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
    '''Сериализатор для загрузки прогноза продаж'''
    st_id = serializers.PrimaryKeyRelatedField(
        queryset=Store.objects.all(),
        source='st_sku_date.st_id'
    )
    pr_sku_id = serializers.PrimaryKeyRelatedField(
        queryset=Sku.objects.all(),
        source='st_sku_date.pr_sku_id'
    )
    date = serializers.DateField(source='st_sku_date.date')
    target = serializers.DecimalField(max_digits=6, decimal_places=1,
                                      source='sales_units')

    class Meta:
        model = Forecast
        fields = ('st_id', 'pr_sku_id', 'date', 'target')

    def create(self, validated_data):
        obj, created = Sales.objects.get_or_create(
            st_id=validated_data['st_sku_date']['st_id'],
            pr_sku_id=validated_data['st_sku_date']['pr_sku_id'],
            date=validated_data['st_sku_date']['date']
        )
        forecast = Forecast.objects.create(
            st_sku_date=obj,
            sales_units=validated_data['sales_units'],
            forecast_date=date.today()
        )
        return forecast


class SalesSerializer(serializers.ModelSerializer):
    '''Сериализатор вывода факта продаж'''
    store = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_sku_date.st_id'
    )
    sku = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_sku_date.pr_sku_id'
    )
    date = serializers.DateField(
        read_only=True,
        source='st_sku_date.date'
    )

    class Meta:
        model = SalesFact
        fields = ('store', 'sku', 'date', 'sales_type', 'sales_units',
                  'sales_units_promo', 'sales_rub', 'sales_run_promo')


class SalesPostSerializer(serializers.ModelSerializer):
    '''Сериализатор загрузки факта продаж'''
    st_id = serializers.PrimaryKeyRelatedField(
        queryset=Store.objects.all(),
        source='st_sku_date.st_id'
    )
    pr_sku_id = serializers.PrimaryKeyRelatedField(
        queryset=Sku.objects.all(),
        source='st_sku_date.pr_sku_id'
    )
    date = serializers.DateField(source='st_sku_date.date')
    pr_sales_type_id = serializers.IntegerField(min_value=0, max_value=1,
                                                source='sales_type')
    pr_sales_in_units = serializers.DecimalField(max_digits=6,
                                                 decimal_places=1,
                                                 source='sales_units')
    pr_promo_sales_in_units = serializers.DecimalField(
        max_digits=6,
        decimal_places=1,
        source='sales_units_promo'
    )
    pr_sales_in_rub = serializers.DecimalField(max_digits=8, decimal_places=1,
                                               source='sales_rub')
    pr_promo_sales_in_rub = serializers.DecimalField(max_digits=8,
                                                     decimal_places=1,
                                                     source='sales_run_promo')

    class Meta:
        model = SalesFact
        fields = ('st_id', 'pr_sku_id', 'date', 'pr_sales_type_id',
                  'pr_sales_in_units', 'pr_promo_sales_in_units',
                  'pr_sales_in_rub', 'pr_promo_sales_in_rub')

    def create(self, validated_data):
        obj, created = Sales.objects.get_or_create(
            st_id=validated_data['st_sku_date']['st_id'],
            pr_sku_id=validated_data['st_sku_date']['pr_sku_id'],
            date=validated_data['st_sku_date']['date']
        )
        sale = SalesFact.objects.create(
            st_sku_date=obj,
            sales_type=validated_data['sales_type'],
            sales_units=validated_data['sales_units'],
            sales_units_promo=validated_data['sales_units_promo'],
            sales_rub=validated_data['sales_rub'],
            sales_run_promo=validated_data['sales_run_promo']
        )
        set_diff(obj)
        return sale


class SalesDiffSerializer(serializers.ModelSerializer):
    '''Сериализатор для вывода качества прогноза'''
    store = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_sku_date.st_id'
    )
    group = serializers.CharField(
        read_only=True,
        source='st_sku_date.pr_sku_id.pr_group_id'
    )
    category = serializers.CharField(
        read_only=True,
        source='st_sku_date.pr_sku_id.pr_cat_id'
    )
    subcategory = serializers.CharField(
        read_only=True,
        source='st_sku_date.pr_sku_id.pr_subcat_id'
    )
    sku = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_sku_date.pr_sku_id'
    )
    date = serializers.DateField(
        read_only=True,
        source='st_sku_date.date'
    )
    sales_units = serializers.SerializerMethodField()
    forecast_units = serializers.SerializerMethodField()

    class Meta:
        model = SalesDiff
        fields = ('store', 'group', 'category', 'subcategory', 'sku', 'date',
                  'sales_units', 'forecast_units', 'diff_sales_units', 'wape')

    def get_sales_units(self, obj):
        return SalesFact.objects.filter(st_sku_date=obj.st_sku_date).aggregate(
            total_sales_units=Coalesce(
                Sum('sales_units'),
                0,
                output_field=models.DecimalField(max_digits=6,
                                                 decimal_places=1)
            )
        )['total_sales_units']

    def get_forecast_units(self, obj):
        forecast = Forecast.objects.filter(st_sku_date=obj.st_sku_date).first()
        if forecast:
            forecast_units = forecast.sales_units
        else:
            forecast_units = 0
        return forecast_units


class ForecastSkuSerializer(serializers.ModelSerializer):
    date = serializers.DateField(read_only=True, source='st_sku_date.date')

    class Meta:
        model = Forecast
        fields = ('date', 'sales_units')

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


class FSkuSerializer(serializers.ModelSerializer):
    sku = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_sku_date.pr_sku_id'
    )
    forecast = serializers.SerializerMethodField()

    class Meta:
        model = Forecast
        fields = ('sku', 'forecast')


class SubcategorySerializer(serializers.ModelSerializer):
    subcategory = serializers.CharField(
        source='st_sku_date.pr_sku_id.pr_subcat_id'
    )
    sku = FSkuSerializer(read_only=True)

    class Meta:
        model = Forecast
        fields = ('subcategory', 'sku')


class CategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(
        source='st_sku_date.pr_sku_id.pr_cat_id'
    )
    subcategory = SubcategorySerializer(read_only=True)

    class Meta:
        model = Forecast
        fields = ('category', 'subcategory')


class GroupSerializer(serializers.ModelSerializer):
    group = serializers.CharField(
        source='st_sku_date.pr_sku_id.pr_group_id'
    )
    category =CategorySerializer(read_only=True)

    class Meta:
        model = Forecast
        fields = ('group', 'category')


class FStoreSerializer(serializers.ModelSerializer):
    store = serializers.PrimaryKeyRelatedField(
        read_only=True, source='st_sku_date.st_id'
    )
    group = GroupSerializer(read_only=True)

    class Meta:
        model = Forecast
        fields = ('store', 'group')


class FForecastSerializer(serializers.ModelSerializer):
    '''Сериализатор для вывода прогноза продаж2'''
    city = serializers.CharField(
        source='st_sku_date.st_id.st_city_id'
    )
    store = FStoreSerializer(read_only=True)

    class Meta:
        model = Forecast
        fields = ('city', 'store')
