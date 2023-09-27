# Generated by Django 4.2.5 on 2023-09-27 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_forecast_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='date',
            field=models.DateField(verbose_name='дата продаж'),
        ),
        migrations.AlterField(
            model_name='sales',
            name='sales_rub',
            field=models.DecimalField(decimal_places=1, max_digits=8, verbose_name='всего руб'),
        ),
        migrations.AlterField(
            model_name='sales',
            name='sales_run_promo',
            field=models.DecimalField(decimal_places=1, max_digits=8, verbose_name='промо руб'),
        ),
        migrations.AlterField(
            model_name='sales',
            name='sales_units',
            field=models.DecimalField(decimal_places=0, max_digits=6, verbose_name='всего шт'),
        ),
        migrations.AlterField(
            model_name='sales',
            name='sales_units_promo',
            field=models.DecimalField(decimal_places=1, max_digits=6, verbose_name='промо шт'),
        ),
    ]
