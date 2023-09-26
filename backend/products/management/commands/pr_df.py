import csv

from django.core.management.base import BaseCommand
from tqdm import tqdm

from products.models import Sku
from products.management.setup_logger import setup_logger


logger = setup_logger()


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('products/data/pr_df.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            count = 0
            logger.info('старт загрузки данных')
            for row in tqdm(reader):
                try:
                    pr_sku_id, pr_group_id, pr_cat_id, pr_subcat_id, pr_uom_id = row
                    Sku.objects.get_or_create(
                        pr_sku_id=pr_sku_id,
                        pr_group_id=pr_group_id,
                        pr_cat_id=pr_cat_id,
                        pr_subcat_id=pr_subcat_id,
                        pr_uom_id=pr_uom_id
                    )
                    count += 1
                except Exception as error:
                    logger.error(f'сбой в работе: {error}')
            logger.info(f'загружено {count} строк')
