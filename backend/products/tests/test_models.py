from django.test import TestCase

from ..models import SalesFact, Sales, Sku, Store, Sales, Forecast, SalesDiff


class ModelsTest(TestCase):
    def setUp(self):
        self.sku = Sku.objects.create(
            pr_sku_id='test',
            pr_group_id='test_group',
            pr_cat_id='test_category',
            pr_subcat_id='test_subcategory',
            pr_uom_id=1,
        )
        self.store = Store.objects.create(
            st_id='test',
            st_city_id='test_city',
            st_division_code='test_division',
            st_type_format_id=11,
            st_type_loc_id=22,
            st_type_size_id=33,
            st_is_active=44,
        )
        self.sales = Sales.objects.create(
            pr_sku_id=self.sku,
            st_id=self.store,
            date='2021-01-01'
        )
        self.sales_fact = SalesFact.objects.create(
            st_sku_date=self.sales,
            sales_type=1,
            sales_units=100,
            sales_units_promo=5,
            sales_rub=100,
            sales_run_promo=50,
        )
        self.forecast = Forecast.objects.create(
            st_sku_date=self.sales,
            sales_units=90,
            forecast_date='2021-01-01'
        )
        self.sales_diff = SalesDiff.objects.create(
            st_sku_date=self.sales,
        )

    def test_sku_fields(self):
        self.assertEqual(self.sku.pr_sku_id, 'test')
        self.assertEqual(self.sku.pr_group_id, 'test_group')
        self.assertEqual(self.sku.pr_cat_id, 'test_category')
        self.assertEqual(self.sku.pr_subcat_id, 'test_subcategory')
        self.assertEqual(self.sku.pr_uom_id, 1)

    def test_store_fields(self):
        self.assertEqual(self.store.st_id, 'test')
        self.assertEqual(self.store.st_city_id, 'test_city')
        self.assertEqual(self.store.st_division_code, 'test_division')
        self.assertEqual(self.store.st_type_format_id, 11)
        self.assertEqual(self.store.st_type_loc_id, 22)
        self.assertEqual(self.store.st_type_size_id, 33)
        self.assertEqual(self.store.st_is_active, 44)

    def test_sales_fields(self):
        self.assertEqual(self.sales.pr_sku_id, self.sku)
        self.assertEqual(self.sales.st_id, self.store)
        self.assertEqual(self.sales.date, '2021-01-01')

    def test_sales_fact_fields(self):
        self.assertEqual(self.sales_fact.st_sku_date, self.sales)
        self.assertEqual(self.sales_fact.sales_type, 1)
        self.assertEqual(self.sales_fact.sales_units, 100)
        self.assertEqual(self.sales_fact.sales_units_promo, 5)
        self.assertEqual(self.sales_fact.sales_rub, 100)
        self.assertEqual(self.sales_fact.sales_run_promo, 50)

    def test_forecast_fields(self):
        self.assertEqual(self.forecast.st_sku_date, self.sales)
        self.assertEqual(self.forecast.sales_units, 90)
        self.assertEqual(self.forecast.forecast_date, '2021-01-01')

    def test_sales_diff_fields(self):
        sales_diff = SalesDiff(st_sku_date=self.sales, diff_sales_units=0,
                               wape=0)
        sales_diff.save()
        self.assertEqual(sales_diff.diff_sales_units, 10)
        self.assertAlmostEqual(sales_diff.wape, 10, places=1)
