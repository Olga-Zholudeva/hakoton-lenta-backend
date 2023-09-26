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
            reader = csv.reader(f)
            count = 0
            logger.info('старт загрузки данных')
            for row in tqdm(reader):
                try:
                    st_id, pr_sku_id, date, target = row
                    store = Store.objects.get(pk=st_id)
                    sku = Sku.objects.get(pk=pr_sku_id)
                    store_sku = ForecastSku.objects.get_or_create(
                        st_id=store,
                        pr_sku_id=sku,
                        date=today,
                    )
                    Forecast.objects.get_or_create(
                        forecast_sku_id=store_sku,
                        date=date,
                        target=target,
                    )
                    count += 1
                except Exception as error:
                    logger.error(f'сбой в работе: {error}')
            logger.info(f'загружено {count} строк')
