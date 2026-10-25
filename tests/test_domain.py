import unittest

import pandas as pd

from app.domain import (
    baseline_daily_forecast,
    forecast_7_days,
    prepare_dataset,
    restock_recommendations,
    sales_summary,
)


def sales_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["2026-10-01", "Kopi Susu", 10, 18000],
            ["2026-10-02", "Kopi Susu", 20, 18000],
            ["2026-10-03", "Kopi Susu", 30, 18000],
            ["2026-10-04", "Kopi Susu", 20, 18000],
            ["2026-10-05", "Kopi Susu", 20, 18000],
            ["2026-10-06", "Kopi Susu", 20, 18000],
            ["2026-10-07", "Kopi Susu", 20, 18000],
            ["2026-10-01", "Teh Lemon", 5, 12000],
            ["2026-10-02", "Teh Lemon", 5, 12000],
            ["2026-10-03", "Teh Lemon", 5, 12000],
            ["2026-10-04", "Teh Lemon", 5, 12000],
            ["2026-10-05", "Teh Lemon", 5, 12000],
            ["2026-10-06", "Teh Lemon", 5, 12000],
            ["2026-10-07", "Teh Lemon", 5, 12000],
        ],
        columns=["tanggal", "produk", "jumlah_terjual", "harga_satuan"],
    )


def inventory_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["Kopi Susu", 10, 2, 10, 0, 5],
            ["Teh Lemon", 50, 3, 10, 0, 5],
        ],
        columns=[
            "produk",
            "stok_saat_ini",
            "waktu_pengiriman_hari",
            "stok_minimum",
            "stok_dalam_perjalanan",
            "jumlah_pesanan_minimum",
        ],
    )


class DomainTests(unittest.TestCase):
    def test_valid_dataset_produces_summary_forecast_and_restock(self) -> None:
        dataset = prepare_dataset(sales_frame(), inventory_frame())

        self.assertEqual(dataset.errors, [])
        self.assertEqual(sales_summary(dataset.sales)["total_unit_terjual"], 175)
        self.assertEqual(len(baseline_daily_forecast(dataset.sales)), 2)
        self.assertEqual(len(forecast_7_days(dataset.sales)), 14)

        recommendations = restock_recommendations(dataset.sales, dataset.inventory)
        kopi = recommendations.loc[recommendations["produk"] == "Kopi Susu"].iloc[0]
        self.assertEqual(kopi["rekomendasi_restock"], 40)
        self.assertEqual(kopi["status"], "Segera restock")
        self.assertIn("Beli 40 unit", kopi["alasan"])

    def test_invalid_sales_is_rejected_with_actionable_error(self) -> None:
        invalid_sales = sales_frame().copy()
        invalid_sales.loc[0, "jumlah_terjual"] = -1
        invalid_sales.loc[1, "tanggal"] = "bukan tanggal"

        dataset = prepare_dataset(invalid_sales, inventory_frame())

        self.assertTrue(any("tidak boleh negatif" in error for error in dataset.errors))
        self.assertTrue(any("tanggal" in error for error in dataset.errors))

    def test_unknown_product_is_not_silently_ignored(self) -> None:
        inventory = inventory_frame().iloc[[0]].copy()

        dataset = prepare_dataset(sales_frame(), inventory)

        self.assertTrue(any("Teh Lemon" in error for error in dataset.errors))

    def test_missing_optional_inventory_columns_use_safe_defaults(self) -> None:
        inventory = inventory_frame().drop(
            columns=["stok_dalam_perjalanan", "jumlah_pesanan_minimum"]
        )

        dataset = prepare_dataset(sales_frame(), inventory)

        self.assertEqual(dataset.errors, [])
        self.assertTrue(any("stok_dalam_perjalanan" in warning for warning in dataset.warnings))
        self.assertTrue(any("jumlah_pesanan_minimum" in warning for warning in dataset.warnings))


if __name__ == "__main__":
    unittest.main()
