from django.db import models


class Sku(models.Model):
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
    st_id = models.CharField(
        primary_key=True,
        max_length=200,
        verbose_name='Магазин',
    )
    st_city_id = models.CharField(
        max_length=200,
        verbose_name='Город',
    )
    st_division_code = models.CharField(
        max_length=200,
        verbose_name='Дивизион',
    )
    st_type_format_id = models.IntegerField(verbose_name='Формат',)
    st_type_loc_id = models.IntegerField(verbose_name='Тип локации/окружения',)
    st_type_size_id = models.IntegerField(verbose_name='Размер',)
    st_is_active = models.IntegerField(verbose_name='Активность',)


class ForecastSku(models.Model):
    st_id = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='store',
        verbose_name='Магазин',
    )
    pr_sku_id = models.ForeignKey(
        Sku,
        on_delete=models.CASCADE,
        related_name='sku',
        verbose_name='Товар',
    )
    forecast_date = models.DateTimeField(verbose_name='Дата прогноза',)

    class Meta:
        ordering = ('-forecast_date',)
        verbose_name = 'Прогноз'
        verbose_name_plural = 'Прогнозы'

    def __str__(self):
        return f'''Прогноз для {self.pr_sku_id} в {self.st_id}
                   на {self.forecast_date}'''


class Forecast(models.Model):
    date = models.DateTimeField(verbose_name='Дата прогноза',)
    target = models.IntegerField(verbose_name='Цель',)
    forecast_id = models.ForeignKey(
        ForecastSku,
        on_delete=models.CASCADE,
        related_name='forecast',
    )

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'''Прогноз для {self.forecast_id}
                   на {self.date}'''
