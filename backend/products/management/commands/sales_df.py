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
            sales_list = []
            all_store = Store.objects.all()
            all_sku = Sku.objects.all()
            for row in tqdm(reader):
                try:
                    st_id, pr_sku_id, date, pr_sales_type_id, pr_sales_in_units, pr_promo_sales_in_units, pr_sales_in_rub, pr_promo_sales_in_rub = row
                    store = all_store.get(pk=st_id)
                    sku = all_sku.get(pk=pr_sku_id)
                    sales = Sales(
                        st_id=store,
                        pr_sku_id=sku,
                        date=date,
                        sales_type=pr_sales_type_id,
                        sales_units=pr_sales_in_units,
                        sales_units_promo=pr_promo_sales_in_units,
                        sales_rub=pr_sales_in_rub,
                        sales_run_promo=pr_promo_sales_in_rub
                    )
                    sales_list.append(sales)
                    count += 1
                except Exception as error:
                    logger.error(f'сбой в работе: {error}')
            Sales.objects.bulk_create(sales_list)
            logger.info(f'загружено {count} строк')
