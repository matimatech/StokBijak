"""Pure data and inventory logic for the first StokBijak vertical slice."""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil

import pandas as pd

SALES_REQUIRED_COLUMNS = ("tanggal", "produk", "jumlah_terjual", "harga_satuan")
INVENTORY_REQUIRED_COLUMNS = (
    "produk",
    "stok_saat_ini",
    "waktu_pengiriman_hari",
    "stok_minimum",
)
INVENTORY_OPTIONAL_DEFAULTS = {
    "stok_dalam_perjalanan": 0,
    "jumlah_pesanan_minimum": 1,
}


@dataclass
class ValidationResult:
    """A cleaned frame plus messages that can be shown to a user."""

    frame: pd.DataFrame | None
    errors: list[str]
    warnings: list[str]


@dataclass
class PreparedDataset:
    """The result of validating both uploaded files together."""

    sales: pd.DataFrame | None
    inventory: pd.DataFrame | None
    errors: list[str]
    warnings: list[str]


def _missing_columns(frame: pd.DataFrame, required: tuple[str, ...]) -> list[str]:
    return [column for column in required if column not in frame.columns]


def _normalise_products(frame: pd.DataFrame) -> pd.DataFrame:
    cleaned = frame.copy()
    cleaned["produk"] = cleaned["produk"].astype("string").str.strip()
    return cleaned


def _validate_nonnegative(
    frame: pd.DataFrame,
    column: str,
    label: str,
    errors: list[str],
    *,
    strictly_positive: bool = False,
) -> None:
    values = pd.to_numeric(frame[column], errors="coerce")
    invalid = values.isna()
    if invalid.any():
        errors.append(f"Kolom `{column}` memiliki {int(invalid.sum())} nilai bukan angka.")
    negative = values < 0
    if negative.fillna(False).any():
        errors.append(f"{label} tidak boleh negatif.")
    if strictly_positive:
        zero = values == 0
        if zero.fillna(False).any():
            errors.append(f"{label} harus lebih besar dari nol.")
    frame[column] = values


def validate_sales(frame: pd.DataFrame) -> ValidationResult:
    """Validate and clean the sales CSV contract."""

    errors: list[str] = []
    warnings: list[str] = []
    missing = _missing_columns(frame, SALES_REQUIRED_COLUMNS)
    if missing:
        return ValidationResult(
            None,
            [f"sales.csv belum memiliki kolom wajib: {', '.join(missing)}."],
            [],
        )
    if frame.empty:
        return ValidationResult(None, ["sales.csv tidak boleh kosong."], [])

    cleaned = _normalise_products(frame)
    cleaned["tanggal"] = pd.to_datetime(cleaned["tanggal"], errors="coerce")
    if cleaned["tanggal"].isna().any():
        errors.append("Kolom `tanggal` memiliki tanggal kosong atau format yang tidak valid.")
    if cleaned["produk"].isna().fillna(False).any() or (cleaned["produk"] == "").any():
        errors.append("Kolom `produk` tidak boleh kosong.")
    _validate_nonnegative(cleaned, "jumlah_terjual", "Jumlah terjual", errors)
    _validate_nonnegative(cleaned, "harga_satuan", "Harga satuan", errors)

    duplicate_count = int(cleaned.duplicated().sum())
    if duplicate_count:
        errors.append(f"sales.csv memiliki {duplicate_count} baris duplikat.")

    valid_dates = cleaned["tanggal"].dropna().dt.normalize().drop_duplicates().sort_values()
    if len(valid_dates) >= 2:
        expected_days = (valid_dates.iloc[-1] - valid_dates.iloc[0]).days + 1
        if expected_days != len(valid_dates):
            warnings.append(
                "Ada tanggal yang tidak tercatat di antara tanggal awal dan akhir. "
                "Sistem tidak menganggapnya otomatis sebagai penjualan nol."
            )
    if len(valid_dates) < 7:
        warnings.append(
            "Data memiliki kurang dari 7 hari tercatat. Forecast baseline tetap dibuat, "
            "tetapi belum cukup kuat untuk keputusan operasional."
        )

    return ValidationResult(
        cleaned.sort_values(["tanggal", "produk"]).reset_index(drop=True), errors, warnings
    )


def validate_inventory(frame: pd.DataFrame) -> ValidationResult:
    """Validate and clean the inventory CSV contract."""

    errors: list[str] = []
    warnings: list[str] = []
    missing = _missing_columns(frame, INVENTORY_REQUIRED_COLUMNS)
    if missing:
        return ValidationResult(
            None,
            [f"inventory.csv belum memiliki kolom wajib: {', '.join(missing)}."],
            [],
        )
    if frame.empty:
        return ValidationResult(None, ["inventory.csv tidak boleh kosong."], [])

    cleaned = _normalise_products(frame)
    if cleaned["produk"].isna().fillna(False).any() or (cleaned["produk"] == "").any():
        errors.append("Kolom `produk` tidak boleh kosong.")

    for column, label in (
        ("stok_saat_ini", "Stok saat ini"),
        ("waktu_pengiriman_hari", "Waktu pengiriman"),
        ("stok_minimum", "Stok minimum"),
    ):
        _validate_nonnegative(cleaned, column, label, errors)

    for column, default in INVENTORY_OPTIONAL_DEFAULTS.items():
        if column not in cleaned.columns:
            cleaned[column] = default
            warnings.append(
                f"Kolom opsional `{column}` tidak ada; nilai default {default} digunakan."
            )
        label = (
            "Jumlah pesanan minimum"
            if column == "jumlah_pesanan_minimum"
            else "Stok dalam perjalanan"
        )
        _validate_nonnegative(
            cleaned,
            column,
            label,
            errors,
            strictly_positive=column == "jumlah_pesanan_minimum",
        )

    duplicate_products = (
        cleaned.loc[cleaned.duplicated("produk", keep=False), "produk"].dropna().unique()
    )
    if len(duplicate_products):
        errors.append(
            "inventory.csv harus memiliki satu baris per produk. Duplikat: "
            + ", ".join(map(str, duplicate_products))
            + "."
        )

    return ValidationResult(cleaned.sort_values("produk").reset_index(drop=True), errors, warnings)


def prepare_dataset(sales: pd.DataFrame, inventory: pd.DataFrame) -> PreparedDataset:
    """Validate both files and check that products can be joined safely."""

    sales_result = validate_sales(sales)
    inventory_result = validate_inventory(inventory)
    errors = [*sales_result.errors, *inventory_result.errors]
    warnings = [*sales_result.warnings, *inventory_result.warnings]

    if sales_result.frame is not None and inventory_result.frame is not None:
        sales_products = set(sales_result.frame["produk"].dropna())
        inventory_products = set(inventory_result.frame["produk"].dropna())
        missing_inventory = sorted(sales_products - inventory_products)
        if missing_inventory:
            errors.append(
                "Produk di sales.csv belum ada di inventory.csv: "
                + ", ".join(missing_inventory)
                + "."
            )
        without_sales = sorted(inventory_products - sales_products)
        if without_sales:
            warnings.append(
                "Produk berikut belum memiliki penjualan pada periode data: "
                + ", ".join(without_sales)
                + "."
            )

    return PreparedDataset(sales_result.frame, inventory_result.frame, errors, warnings)


def add_sales_value(sales: pd.DataFrame) -> pd.DataFrame:
    """Add a derived transaction value without mutating the input."""

    enriched = sales.copy()
    enriched["nilai_penjualan"] = enriched["jumlah_terjual"] * enriched["harga_satuan"]
    return enriched


def sales_summary(sales: pd.DataFrame) -> dict[str, int | float | str]:
    """Return dashboard summary metrics."""

    enriched = add_sales_value(sales)
    dates = enriched["tanggal"].dt.normalize()
    return {
        "total_nilai_penjualan": float(enriched["nilai_penjualan"].sum()),
        "total_unit_terjual": int(enriched["jumlah_terjual"].sum()),
        "jumlah_produk": int(enriched["produk"].nunique()),
        "tanggal_awal": dates.min().strftime("%d %b %Y"),
        "tanggal_akhir": dates.max().strftime("%d %b %Y"),
        "jumlah_hari": int(dates.nunique()),
    }


def daily_sales(sales: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales for the daily chart."""

    enriched = add_sales_value(sales)
    return (
        enriched.assign(tanggal=enriched["tanggal"].dt.normalize())
        .groupby("tanggal", as_index=False)[["jumlah_terjual", "nilai_penjualan"]]
        .sum()
        .sort_values("tanggal")
    )


def _daily_product_matrix(sales: pd.DataFrame) -> pd.DataFrame:
    dates = pd.date_range(
        sales["tanggal"].min().normalize(), sales["tanggal"].max().normalize(), freq="D"
    )
    matrix = (
        sales.assign(tanggal=sales["tanggal"].dt.normalize())
        .groupby(["tanggal", "produk"])["jumlah_terjual"]
        .sum()
        .unstack(fill_value=0)
        .reindex(dates, fill_value=0)
    )
    return matrix.fillna(0)


def baseline_daily_forecast(sales: pd.DataFrame) -> pd.DataFrame:
    """Create an explainable seven-day baseline from the most recent seven days."""

    matrix = _daily_product_matrix(sales)
    window = matrix.tail(min(7, len(matrix)))
    return (
        window.mean()
        .rename("prediksi_harian")
        .reset_index()
        .rename(columns={"produk": "produk"})
    )


def forecast_7_days(sales: pd.DataFrame) -> pd.DataFrame:
    """Return one row per product and future date for the baseline forecast."""

    daily = baseline_daily_forecast(sales)
    first_date = sales["tanggal"].max().normalize() + pd.Timedelta(days=1)
    future_dates = pd.date_range(first_date, periods=7, freq="D")
    rows = [
        {"tanggal": date, "produk": row.produk, "prediksi_jumlah": row.prediksi_harian}
        for row in daily.itertuples(index=False)
        for date in future_dates
    ]
    return pd.DataFrame(rows)


def restock_recommendations(sales: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    """Calculate transparent restock suggestions from the baseline forecast.

    `stok_minimum` is used as the first MVP's safety-stock proxy. This keeps the
    recommendation grounded in the inventory file until variability data exists.
    """

    daily = baseline_daily_forecast(sales)
    result = inventory.merge(daily, on="produk", how="left").fillna({"prediksi_harian": 0})
    result["prediksi_kebutuhan_lead_time"] = (
        result["prediksi_harian"] * result["waktu_pengiriman_hari"]
    )
    result["safety_stock_proxy"] = result["stok_minimum"]
    result["kebutuhan_sebelum_pembulatan"] = (
        result["prediksi_kebutuhan_lead_time"]
        + result["safety_stock_proxy"]
        - result["stok_saat_ini"]
        - result["stok_dalam_perjalanan"]
    ).clip(lower=0)

    def round_to_moq(row: pd.Series) -> int:
        need = float(row["kebutuhan_sebelum_pembulatan"])
        moq = int(row["jumlah_pesanan_minimum"])
        return 0 if need <= 0 else int(ceil(need / moq) * moq)

    result["rekomendasi_restock"] = result.apply(round_to_moq, axis=1)
    result["coverage_days"] = result.apply(
        lambda row: None
        if row["prediksi_harian"] <= 0
        else row["stok_saat_ini"] / row["prediksi_harian"],
        axis=1,
    )
    result["status"] = result["rekomendasi_restock"].map(
        lambda quantity: "Segera restock" if quantity > 0 else "Stok cukup"
    )

    def explain(row: pd.Series) -> str:
        if row["rekomendasi_restock"] <= 0:
            return (
                f"Stok {row['stok_saat_ini']:.0f} unit dan stok dalam perjalanan "
                f"{row['stok_dalam_perjalanan']:.0f} unit masih mencukupi kebutuhan "
                f"lead time {row['waktu_pengiriman_hari']:.0f} hari plus stok minimum."
            )
        return (
            f"Beli {row['rekomendasi_restock']:.0f} unit: estimasi kebutuhan lead time "
            f"{row['prediksi_kebutuhan_lead_time']:.1f} unit, stok minimum "
            f"{row['stok_minimum']:.0f} unit, stok tersedia "
            f"{row['stok_saat_ini']:.0f} unit, dan waktu kirim "
            f"{row['waktu_pengiriman_hari']:.0f} hari."
        )

    result["alasan"] = result.apply(explain, axis=1)
    return result.sort_values(
        ["rekomendasi_restock", "prediksi_kebutuhan_lead_time"], ascending=False
    ).reset_index(drop=True)
