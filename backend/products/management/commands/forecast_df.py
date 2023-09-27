import csv
from datetime import date

from django.core.management.base import BaseCommand
from tqdm import tqdm

from products.models import ForecastSku, Forecast, Sku, Store
from products.management.setup_logger import setup_logger


logger = setup_logger()
today = date.today()


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('products/data/sales_submission.csv', encoding='utf-8') as f:
            logger.info('старт загрузки данных')
            reader = csv.reader(f)
            count = 0
            forecast_sku_list = []
            forecast_list = []
            all_store = Store.objects.all()
            all_sku = Sku.objects.all()
            for row in tqdm(reader):
                try:
                    st_id, pr_sku_id, date, target = row
                    store = all_store.get(pk=st_id)
                    sku = all_sku.get(pk=pr_sku_id)
                    store_sku = ForecastSku(
                        st_id=store,
                        pr_sku_id=sku,
                        forecast_date=today,
                    )
                    forecast = Forecast(
                        forecast_sku_id=store_sku,
                        date=date,
                        target=target,
                    )
                    forecast_sku_list.append(store_sku)
                    forecast_list.append(forecast)
                    count += 1
                except Exception as error:
                    logger.error(f'сбой в работе: {error}')
            ForecastSku.objects.bulk_create(forecast_sku_list, batch_size=1000)
            Forecast.objects.bulk_create(forecast_list, batch_size=1000)
            logger.info(f'загружено {count} строк')
