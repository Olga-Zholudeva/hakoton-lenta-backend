import csv
import logging

from products.models import Store
from products.setup_logger import setup_logger


logger = setup_logger()


def main()
    with open('products/data/st_df.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            try:
                logger.info('старт загрузки данных')
                pr_sku_id, pr_group_id, pr_cat_id, pr_subcat_id, pr_uom_id = row
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


if __name__ == '__main__':
    main()
