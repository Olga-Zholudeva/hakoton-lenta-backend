import csv

from django.core.management.base import BaseCommand
from tqdm import tqdm

from products.models import Store
from products.management.setup_logger import setup_logger


logger = setup_logger()


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('products/data/st_df.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            count = 0
            logger.info('старт загрузки данных')
            for row in tqdm(reader):
                try:
                    st_id, st_city_id, st_division_code, st_type_format_id, st_type_loc_id, st_type_size_id, st_is_active = row
                    Store.objects.get_or_create(
                        st_id=st_id,
                        st_city_id=st_city_id,
                        st_division_code=st_division_code,
                        st_type_format_id=st_type_format_id,
                        st_type_loc_id=st_type_loc_id,
                        st_type_size_id=st_type_size_id,
                        st_is_active=st_is_active
                    )
                    count += 1
                except Exception as error:
                    logger.error(f'сбой в работе: {error}')
            logger.info(f'загружено {count} строк')
