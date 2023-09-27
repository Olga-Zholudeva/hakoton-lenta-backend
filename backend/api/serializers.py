from rest_framework import serializers
from products.models import Sku, Sales, Store
from django.db.models import Sum


class SkuSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели Товар.'''
    sku = serializers.CharField(source='pr_sku_id')
    group = serializers.CharField(source='pr_group_id')
    category = serializers.CharField(source='pr_cat_id')
    subcategory = serializers.CharField(source='pr_subcat_id')
    uom = serializers.CharField(source='pr_uom_id')
    class Meta:
        model = Sku
        fields = ('sku', 'group', 'category', 'subcategory', 'uom',)

class SalesFactSerializer(serializers.ModelSerializer):
    '''Промежуточный сериализатор для агрегации продаж по магазину и товару.'''
    class Meta:
        model = Sales
        fields = ('date', 'sales_type', 'sales_units', 'sales_units_promo', 'sales_rub', 'sales_run_promo',)

class SalesSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели с фактом продаж.'''
    store = serializers.CharField(source='st_id')
    sku = serializers.CharField(source='pr_sku_id')
    fact = serializers.SerializerMethodField()
    class Meta:
        model = Sales
        fields = ('store', 'sku','fact',)

    def get_fact(self, obj):
        '''Получаем данные по продажам, сгруппированные по полям st_id и pr_sku_id.'''
        grouped_sales = Sales.objects.filter(st_id=obj.st_id, pr_sku_id=obj.pr_sku_id).values(
            'date', 'sales_type').annotate(
            sales_units=Sum('sales_units'),
            sales_units_promo=Sum('sales_units_promo'),
            sales_rub=Sum('sales_rub'),
            sales_run_promo=Sum('sales_run_promo')
        )

        fact_serializer = SalesFactSerializer(grouped_sales, many=True)
        return fact_serializer.data


class StoreSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Магазины.'''
    store = serializers.CharField(source='st_id')
    city = serializers.CharField(source='st_city_id')
    division = serializers.CharField(source='st_division_code')
    type_format = serializers.CharField(source='st_type_format_id')
    loc = serializers.CharField(source='st_type_loc_id')
    size = serializers.CharField(source='st_type_size_id')
    is_active = serializers.CharField(source='st_is_active')
    class Meta:
        model = Store
        fields = ('store', 'city', 'division', 'type_format', 'loc', 'size', 'is_active',)


