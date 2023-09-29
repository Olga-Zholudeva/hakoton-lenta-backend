from django.contrib import admin

from products.models import Sku, Store, ForecastSku, Forecast, Sales


@admin.register(Sku)
class SkuAdmin(admin.ModelAdmin):
    list_display = ('pr_sku_id', 'pr_group_id', 'pr_cat_id', 'pr_subcat_id',
                    'pr_uom_id')
    search_fields = ('pr_sku_id', 'pr_group_id', 'pr_cat_id', 'pr_subcat_id')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('st_id', 'st_city_id', 'st_division_code',
                    'st_type_format_id', 'st_type_loc_id',
                    'st_type_size_id', 'st_is_active')
    search_fields = ('st_id', 'st_city_id', 'st_division_code')


@admin.register(ForecastSku)
class ForecastSkuAdmin(admin.ModelAdmin):
    list_display = ('st_id', 'pr_sku_id', 'forecast_date')
    search_fields = ('st_id', 'pr_sku_id', 'forecast_date')


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ('date', 'target', 'forecast_sku_id')
    search_fields = ('date',)


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ('st_id', 'pr_sku_id', 'date', 'sales_type', 'sales_units',
                    'sales_units_promo', 'sales_rub', 'sales_run_promo')
    search_fields = ('st_id', 'pr_sku_id', 'date')
