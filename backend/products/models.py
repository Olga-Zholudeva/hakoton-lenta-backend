from django.db import models


class Sku(models.Model):
    '''Товар'''
    pr_sku_id = models.CharField(
        primary_key=True,
        max_length=200,
        verbose_name='Товар',
        db_index=True,
    )
    pr_group_id = models.CharField(
        max_length=200,
        verbose_name='Группа',
    )
    pr_cat_id = models.CharField(
        max_length=200,
        verbose_name='Категория',
    )
    pr_subcat_id = models.CharField(
        max_length=200,
        verbose_name='Подкатегория',
    )
    pr_uom_id = models.IntegerField(verbose_name='Единицы измерения',)

    class Meta:
        ordering = ('pr_sku_id',)


class Store(models.Model):
    '''Магазин'''
    st_id = models.CharField(
        primary_key=True,
        max_length=200,
        verbose_name='магазин',
        db_index=True,
    )
    st_city_id = models.CharField(
        max_length=200,
        verbose_name='город',
    )
    st_division_code = models.CharField(
        max_length=200,
        verbose_name='дивизион',
    )
    st_type_format_id = models.IntegerField(verbose_name='формат',)
    st_type_loc_id = models.IntegerField(verbose_name='тип локации/окружения',)
    st_type_size_id = models.IntegerField(verbose_name='размер',)
    st_is_active = models.IntegerField(verbose_name='активность',)

    class Meta:
        ordering = ('st_id',)


class Sales(models.Model):
    '''Магазин-товар-дата'''
    st_id = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='sales_store',
        verbose_name='магазин',
    )
    pr_sku_id = models.ForeignKey(
        Sku,
        on_delete=models.CASCADE,
        related_name='sales_sku',
        verbose_name='товар',
    )
    date = models.DateField(verbose_name='дата продаж',)

    class Meta:
        ordering = ('-date',)


class SalesFact(models.Model):
    '''Продажи факт'''
    st_sku_date = models.ForeignKey(
        Sales,
        on_delete=models.CASCADE,
        related_name='sales_store_date',
        verbose_name='магазин-товар-дата',
    )
    sales_type = models.IntegerField(verbose_name='тип продаж',)
    sales_units = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        verbose_name='всего шт',
    )
    sales_units_promo = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        verbose_name='промо шт',
    )
    sales_rub = models.DecimalField(
        max_digits=8,
        decimal_places=1,
        verbose_name='всего руб',
    )
    sales_run_promo = models.DecimalField(
        max_digits=8,
        decimal_places=1,
        verbose_name='промо руб',
    )

    class Meta:
        ordering = ('st_sku_date',)


class Forecast(models.Model):
    '''Прогнозы'''
    st_sku_date = models.ForeignKey(
        Sales,
        on_delete=models.CASCADE,
        related_name='sales_store_date',
        verbose_name='магазин-товар-дата',
    )
    sales_units = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        verbose_name='всего шт',
    )
    forecast_date = models.DateField(verbose_name='дата прогноза',)

    class Meta:
        ordering = ('-forecast_date',)


class SalesDiff(models.Model):
    '''Качество прогноза'''
    st_sku_date = models.ForeignKey(
        Sales,
        on_delete=models.CASCADE,
        related_name='sales_store_date',
        verbose_name='магазин-товар-дата',
    )
    diff_sales_units = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        verbose_name='разница шт',
    )
    wape = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        verbose_name='wape',
    )

    class Meta:
        ordering = ('st_sku_date',)
