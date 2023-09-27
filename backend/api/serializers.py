from rest_framework import serializers
from products.models import Sku, Sales
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
    date = serializers.DateField()
    sales_type = serializers.IntegerField()
    sales_units = serializers.DecimalField(max_digits=6, decimal_places=2)
    sales_units_promo = serializers.DecimalField(max_digits=6, decimal_places=2)
    sales_rub = serializers.DecimalField(max_digits=8, decimal_places=2)
    sales_run_promo = serializers.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        model = Sales
        fields = ('date', 'sales_type', 'sales_units', 'sales_units_promo', 'sales_rub', 'sales_run_promo',)

class SalesSerializer(serializers.ModelSerializer):
    store = serializers.CharField(source='st_id')
    sku = serializers.CharField(source='pr_sku_id')
    fact = serializers.SerializerMethodField()
    class Meta:
        model = Sales
        fields = ('store', 'sku','fact')

    def get_fact(self, obj):
        grouped_sales = Sales.objects.filter(st_id=obj.st_id, pr_sku_id=obj.pr_sku_id).values(
            'date', 'sales_type').annotate(
            sales_units=Sum('sales_units'),
            sales_units_promo=Sum('sales_units_promo'),
            sales_rub=Sum('sales_rub'),
            sales_run_promo=Sum('sales_run_promo')
        )

        fact_serializer = SalesFactSerializer(grouped_sales, many=True)
        return fact_serializer.data
            


