"""Quick checks so the core business metrics cannot silently drift."""

import unittest

import pandas as pd

from retail.analysis import calculate_kpis, clean_sales, monthly_sales, read_transactions


class RetailAnalysisTests(unittest.TestCase):
    def setUp(self):
        # Isolate these tests from the downloaded real data.
        from retail.analysis import SAMPLE_DATA
        self.raw = read_transactions(SAMPLE_DATA)
        self.sales = clean_sales(self.raw)

    def test_cancellations_and_zero_price_are_removed(self):
        self.assertFalse(self.sales["InvoiceNo"].str.upper().str.startswith("C").any())
        self.assertTrue(self.sales["UnitPrice"].gt(0).all())
        self.assertTrue(self.sales["Quantity"].gt(0).all())

    def test_practice_data_kpis(self):
        kpis = calculate_kpis(self.sales)
        self.assertEqual(kpis["orders"], 10)
        self.assertEqual(kpis["identified_customers"], 6)
        self.assertAlmostEqual(kpis["gross_sales"], 221.5)
        self.assertAlmostEqual(kpis["average_order_value"], 221.5 / 10)

    def test_months_reconcile_to_total(self):
        monthly = monthly_sales(self.sales)
        self.assertAlmostEqual(monthly["LineRevenue"].sum(), self.sales["LineRevenue"].sum())

    def test_empty_sales_metrics_are_safe(self):
        empty = self.sales.iloc[0:0].copy()
        self.assertEqual(calculate_kpis(empty)["average_order_value"], 0)

    def test_does_not_change_original_data(self):
        copy = self.raw.copy(deep=True)
        clean_sales(copy)
        pd.testing.assert_frame_equal(copy, self.raw)


if __name__ == "__main__":
    unittest.main()
