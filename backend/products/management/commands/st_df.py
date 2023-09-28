import csv

from django.core.management.base import BaseCommand
from tqdm import tqdm

from products.models import Store
from products.management.setup_logger import setup_logger


logger = setup_logger()


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('products/data/st_df.csv', encoding='utf-8') as f:
            logger.info('старт загрузки данных')
            reader = csv.reader(f)
            count = 0
            stores_list = []
            for row in tqdm(reader):
                try:
                    st_id, st_city_id, st_division_code, st_type_format_id, st_type_loc_id, st_type_size_id, st_is_active = row
                    store = Store(
                        st_id=st_id,
                        st_city_id=st_city_id,
                        st_division_code=st_division_code,
                        st_type_format_id=st_type_format_id,
                        st_type_loc_id=st_type_loc_id,
                        st_type_size_id=st_type_size_id,
                        st_is_active=st_is_active
                    )
                    stores_list.append(store)
                    count += 1
                except Exception as error:
                    logger.error(f'сбой в работе: {error}')
            Store.objects.bulk_create(stores_list, batch_size=1000)
            logger.info(f'загружено {count} строк')
