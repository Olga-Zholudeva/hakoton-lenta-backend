import csv
from datetime import date

from django.core.management.base import BaseCommand
from tqdm import tqdm

from products.models import Sales, Forecast, Sku, Store
from products.management.setup_logger import setup_logger


logger = setup_logger()
today = date.today()


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('products/data/sales_submission.csv', encoding='utf-8') as f:
            logger.info('старт загрузки данных')
            reader = csv.reader(f)
            next(reader)
            count = 0
            sales_list = []
            forecast_list = []
            all_stores = Store.objects.all()
            all_sku = Sku.objects.all()
            all_sales = Sales.objects.all()
            for row in tqdm(reader):
                try:
                    st_id, pr_sku_id, date, pr_sales_in_units = row
                    store = all_stores.get(pk=st_id)
                    sku = all_sku.get(pk=pr_sku_id)
                    sale = all_sales.filter(st_id=store, pr_sku_id=sku,
                                            date=date)
                    if not sale:
                        sale = Sales(
                            st_id=store,
                            pr_sku_id=sku,
                            date=date,
                        )
                        sales_list.append(sale)
                    forecast = Forecast(
                        st_sku_date=sale,
                        sales_units=pr_sales_in_units,
                        forecast_date=today,
                    )
                    forecast_list.append(forecast)
                    count += 1
                    if count > 9999:
                        Sales.objects.bulk_create(sales_list, batch_size=1000)
                        Forecast.objects.bulk_create(forecast_list,
                                                     batch_size=1000)
                        logger.info(f'загружено {count} строк')
                        sales_list = []
                        forecast_list = []
                        count = 0
                except Exception as error:
                    logger.error(f'сбой в работе: {error}')
            Sales.objects.bulk_create(sales_list, batch_size=1000)
            Forecast.objects.bulk_create(forecast_list, batch_size=1000)
            logger.info(f'загружено {count} строк')
