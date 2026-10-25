"""Streamlit dashboard for the first StokBijak MVP slice."""

from pathlib import Path

import pandas as pd
import streamlit as st

try:
    from app.domain import (
        daily_sales,
        forecast_7_days,
        prepare_dataset,
        restock_recommendations,
        sales_summary,
    )
except ModuleNotFoundError:  # Streamlit adds the script directory to sys.path.
    from domain import (
        daily_sales,
        forecast_7_days,
        prepare_dataset,
        restock_recommendations,
        sales_summary,
    )

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_SALES = ROOT / "data" / "sample" / "sales.csv"
SAMPLE_INVENTORY = ROOT / "data" / "sample" / "inventory.csv"


def _rupiah(value: float) -> str:
    return f"Rp {value:,.0f}".replace(",", ".")


def _load_csv(uploaded_file, sample_path: Path) -> pd.DataFrame:
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    return pd.read_csv(sample_path)


def main() -> None:
    st.set_page_config(page_title="StokBijak", page_icon="📦", layout="wide")
    st.title("📦 StokBijak")
    st.caption(
        "Asisten stok untuk kedai minuman. Unggah dua CSV untuk melihat ringkasan, "
        "forecast baseline 7 hari, dan rekomendasi restock yang dapat diperiksa."
    )

    with st.sidebar:
        st.header("Data")
        st.write("Gunakan contoh bawaan atau unggah data kedai sendiri.")
        source = st.radio("Sumber data", ["Contoh bawaan", "Upload CSV"])
        sales_upload = None
        inventory_upload = None
        if source == "Upload CSV":
            sales_upload = st.file_uploader("sales.csv", type="csv")
            inventory_upload = st.file_uploader("inventory.csv", type="csv")
            if sales_upload is None or inventory_upload is None:
                st.info("Unggah kedua file CSV untuk memulai analisis.")
                st.stop()
        st.divider()
        st.markdown("**Kontrak kolom wajib**")
        st.code("sales.csv: tanggal, produk, jumlah_terjual, harga_satuan")
        st.code("inventory.csv: produk, stok_saat_ini, waktu_pengiriman_hari, stok_minimum")

    try:
        sales_raw = _load_csv(sales_upload, SAMPLE_SALES)
        inventory_raw = _load_csv(inventory_upload, SAMPLE_INVENTORY)
    except Exception as error:  # pragma: no cover - Streamlit rendering path
        st.error(f"File tidak dapat dibaca: {error}")
        st.stop()

    dataset = prepare_dataset(sales_raw, inventory_raw)
    for warning in dataset.warnings:
        st.warning(warning)
    if dataset.errors:
        st.error("Data belum dapat dianalisis. Perbaiki masalah berikut:")
        for error in dataset.errors:
            st.error(error)
        st.stop()

    sales = dataset.sales
    inventory = dataset.inventory
    assert sales is not None and inventory is not None
    summary = sales_summary(sales)
    recommendations = restock_recommendations(sales, inventory)

    metric_columns = st.columns(4)
    metric_columns[0].metric("Nilai penjualan", _rupiah(summary["total_nilai_penjualan"]))
    metric_columns[1].metric("Unit terjual", f"{summary['total_unit_terjual']:,}".replace(",", "."))
    metric_columns[2].metric("Produk", summary["jumlah_produk"])
    metric_columns[3].metric("Hari tercatat", summary["jumlah_hari"])
    st.caption(
        f"Periode data: {summary['tanggal_awal']} – {summary['tanggal_akhir']}. "
        "Forecast menggunakan rata-rata 7 hari terakhir yang tercatat."
    )

    overview, forecast_tab, restock_tab, quality_tab = st.tabs(
        ["Ringkasan", "Forecast 7 hari", "Rekomendasi restock", "Kualitas data"]
    )
    with overview:
        st.subheader("Penjualan harian")
        daily = daily_sales(sales).set_index("tanggal")
        st.line_chart(daily[["nilai_penjualan"]])
        st.subheader("Produk terlaris")
        top_products = (
            sales.assign(nilai_penjualan=sales["jumlah_terjual"] * sales["harga_satuan"])
            .groupby("produk", as_index=False)[["jumlah_terjual", "nilai_penjualan"]]
            .sum()
            .sort_values("jumlah_terjual", ascending=False)
        )
        top_products["nilai_penjualan"] = top_products["nilai_penjualan"].map(_rupiah)
        st.dataframe(top_products, width="stretch", hide_index=True)

    with forecast_tab:
        st.subheader("Forecast baseline")
        st.caption(
            "Ini bukan model machine learning. Baseline memakai rata-rata penjualan "
            "harian dari maksimal 7 hari terakhir agar hasil awal mudah diperiksa."
        )
        forecast = forecast_7_days(sales)
        forecast_table = forecast.pivot(index="tanggal", columns="produk", values="prediksi_jumlah")
        st.dataframe(
            forecast_table.style.format("{:.1f}"),
            width="stretch",
        )
        st.download_button(
            "Unduh forecast CSV",
            forecast.to_csv(index=False).encode("utf-8"),
            "forecast_7_hari.csv",
            "text/csv",
        )

    with restock_tab:
        st.subheader("Rekomendasi pembelian")
        st.caption(
            "`stok_minimum` dipakai sebagai proxy safety stock pada fase awal. "
            "Sistem memberi bantuan, bukan keputusan pembelian otomatis."
        )
        display = recommendations[
            [
                "produk",
                "status",
                "rekomendasi_restock",
                "prediksi_kebutuhan_lead_time",
                "stok_saat_ini",
                "waktu_pengiriman_hari",
                "alasan",
            ]
        ].rename(
            columns={
                "produk": "Produk",
                "status": "Status",
                "rekomendasi_restock": "Rekomendasi unit",
                "prediksi_kebutuhan_lead_time": "Kebutuhan lead time",
                "stok_saat_ini": "Stok saat ini",
                "waktu_pengiriman_hari": "Lead time (hari)",
                "alasan": "Alasan",
            }
        )
        st.dataframe(display, width="stretch", hide_index=True)
        st.download_button(
            "Unduh rekomendasi CSV",
            recommendations.to_csv(index=False).encode("utf-8"),
            "rekomendasi_restock.csv",
            "text/csv",
        )

    with quality_tab:
        st.subheader("Kualitas dan asumsi data")
        st.write(
            "Validasi memastikan kolom wajib ada, tanggal dapat dibaca, angka tidak "
            "negatif, produk konsisten, dan tidak ada duplikat."
        )
        st.write("Tidak ada error validasi.")
        if dataset.warnings:
            st.write("Peringatan yang perlu diperhatikan:")
            for warning in dataset.warnings:
                st.warning(warning)
        st.write("Data penjualan setelah dibersihkan")
        st.dataframe(sales, width="stretch", hide_index=True)


if __name__ == "__main__":
    main()
