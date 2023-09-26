import csv

from products.models import Store
from products.setup_logger import setup_logger


logger = setup_logger()


def main()
    with open('products/data/sales_df_train.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            try:
                logger.info('старт загрузки данных')
                (st_id, pr_sku_id, date, pr_sales_type_id, pr_sales_in_units,
                 pr_promo_sales_in_units, pr_sales_in_rub, pr_promo_sales_in_rub = row)
                Store.objects.get_or_create(
                    st_id=st_id,
                    pr_sku_id=pr_sku_id,
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


if __name__ == '__main__':
    main()
