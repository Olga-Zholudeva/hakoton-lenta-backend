import os
import sys
import csv
from datetime import datetime


current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


from backend.products.models import ForecastSku, Forecast
from backend.products.setup_logger import setup_logger


logger = setup_logger()


def main():
    with open('backend/products/data/sales_submission.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            try:
                logger.info('старт загрузки данных')
                st_id, pr_sku_id, date, target = row
                store_sku = ForecastSku.objects.get_or_create(
                    st_id=st_id,
                    pr_sku_id=pr_sku_id,
                    date=datetime.now(),
                )
                Forecast.objects.get_or_create(
                    forecast_sku_id =store_sku.id,
                    date=date,
                    target=target,
                )
                count += 1
            except Exception as error:
                logger.error(f'сбой в работе: {error}')
        logger.info(f'загружено {count} строк')


if __name__ == '__main__':
    main()
