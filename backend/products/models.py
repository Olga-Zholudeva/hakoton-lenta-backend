from django.db import models


class Sku(models.Model):
    '''Товар'''
    pr_sku_id = models.CharField(
        primary_key=True,
        max_length=200,
        verbose_name='Товар',
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


class Store(models.Model):
    '''Магазин'''
    st_id = models.CharField(
        primary_key=True,
        max_length=200,
        verbose_name='магазин',
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


class StoreSku(models.Model):
    '''Магазин-товар'''
    st_id = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='store',
        verbose_name='магазин',
    )
    pr_sku_id = models.ForeignKey(
        Sku,
        on_delete=models.CASCADE,
        related_name='sku',
        verbose_name='товар',
    )

    class Meta:
        ordering = ('pr_sku_id',)
        verbose_name = 'магазин-товар'

    def __str__(self):
        return f'{self.pr_sku_id} в {self.st_id}'


class ForecastSku(models.Model):
    '''Дата прогноза'''
    store_sku_id = models.ForeignKey(
        StoreSku,
        on_delete=models.CASCADE,
        related_name='store_sku',
        verbose_name='магазин-товар',
    )
    forecast_date = models.DateTimeField(verbose_name='Дата прогноза',)

    class Meta:
        ordering = ('-forecast_date',)
        verbose_name = 'прогноз'
        verbose_name_plural = 'прогнозы'

    def __str__(self):
        return f'''Прогноз для {self.store_sku_id} на {self.forecast_date}'''


class Forecast(models.Model):
    '''Прогнозы'''
    date = models.DateTimeField(verbose_name='дата прогноза',)
    target = models.IntegerField(verbose_name='цель',)
    forecast_sku_id = models.ForeignKey(
        ForecastSku,
        on_delete=models.CASCADE,
        related_name='forecast',
    )

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'''Прогноз для {self.forecast_sku_id}
                   на {self.date}'''


class Sales(models.Model):
    '''Продажи факт'''
    sales_sku_id = models.ForeignKey(
        StoreSku,
        on_delete=models.CASCADE,
        related_name='sales',
    )
    date = models.DateTimeField(verbose_name='дата прогноза',)
    sales_type = models.IntegerField(verbose_name='тип продаж',)
    sales_units = models.IntegerField(verbose_name='всего шт',)
    sales_units_promo = models.IntegerField(verbose_name='промо шт',)
    sales_rub = models.FloatField(verbose_name='всего руб',)
    sales_run_promo = models.FloatField(verbose_name='промо руб',)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'Факт продаж для {self.sales_sku_id} на {self.date}'
