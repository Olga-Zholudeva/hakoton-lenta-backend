import csv

from django.core.management.base import BaseCommand
from tqdm import tqdm

from products.models import Sales, Sku, Store
from products.management.setup_logger import setup_logger


logger = setup_logger()


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('products/data/sales_df_train.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            count = 0
            logger.info('старт загрузки данных')
            for row in tqdm(reader):
                try:
                    st_id, pr_sku_id, date, pr_sales_type_id, pr_sales_in_units, pr_promo_sales_in_units, pr_sales_in_rub, pr_promo_sales_in_rub = row
                    store = Store.objects.get(pk=st_id)
                    sku = Sku.objects.get(pk=pr_sku_id)
                    Sales.objects.get_or_create(
                        st_id=store,
                        pr_sku_id=sku,
                        date=date,
                        sales_type=pr_sales_type_id,
                        sales_units=pr_sales_in_units,
                        sales_units_promo=pr_promo_sales_in_units,
                        sales_rub=pr_sales_in_rub,
                        sales_run_promo=pr_promo_sales_in_rub
                    )
                    count += 1
                except Exception as error:
                    logger.error(f'сбой в работе: {error}')
            logger.info(f'загружено {count} строк')
