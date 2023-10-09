import csv

from django.core.management.base import BaseCommand
from tqdm import tqdm

from products.models import Sales, Sku, Store, SalesDiff
from products.management.setup_logger import setup_logger


logger = setup_logger()


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('products/data/sales_df_train3.csv', encoding='utf-8') as f:
            logger.info('старт загрузки данных')
            reader = csv.reader(f)
            next(reader)
            count = 0
            all_stores = Store.objects.all()
            all_sku = Sku.objects.all()
            for row in tqdm(reader):
                try:
                    st_id, pr_sku_id, date, pr_sales_type_id, pr_sales_in_units, pr_promo_sales_in_units, pr_sales_in_rub, pr_promo_sales_in_rub = row
                    store = all_stores.get(pk=st_id)
                    sku = all_sku.get(pk=pr_sku_id)
                    obj, created = Sales.objects.get_or_create(
                        st_id=store,
                        pr_sku_id=sku,
                        date=date,
                    )
                    sale_diff = SalesDiff(
                        st_sku_date=obj,
                    )
                    sale_diff.save()
                    count += 1
                except Exception as error:
                    logger.error(f'сбой в работе: {error}', exc_info=True)
            logger.info(f'загружено {count} строк')
