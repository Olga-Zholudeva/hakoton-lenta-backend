import csv

from django.core.management.base import BaseCommand
from tqdm import tqdm

from products.models import Sku
from products.management.setup_logger import setup_logger


logger = setup_logger()


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('products/data/pr_df.csv', encoding='utf-8') as f:
            logger.info('старт загрузки данных')
            reader = csv.reader(f)
            next(reader)
            count = 0
            sku_list = []
            for row in tqdm(reader):
                try:
                    pr_sku_id, pr_group_id, pr_cat_id, pr_subcat_id, pr_uom_id = row
                    sku = Sku(
                        pr_sku_id=pr_sku_id,
                        pr_group_id=pr_group_id,
                        pr_cat_id=pr_cat_id,
                        pr_subcat_id=pr_subcat_id,
                        pr_uom_id=pr_uom_id
                    )
                    sku_list.append(sku)
                    count += 1
                except Exception as error:
                    logger.error(f'сбой в работе: {error}')
            Sku.objects.bulk_create(sku_list, batch_size=1000)
            logger.info(f'загружено {count} строк')
