# StokBijak

Status: vertical slice MVP tersedia secara lokal. Dokumen rencana lengkap tersedia di
[`STOKBIJAK_PRODUCT_PLAN.md`](STOKBIJAK_PRODUCT_PLAN.md).

## Goal

StokBijak membantu pemilik atau pengelola kedai minuman kecil mengetahui produk
yang perlu dibeli dalam 7 hari ke depan dan jumlah restock yang disarankan.

- Pengguna awal: kedai minuman kecil dengan sekitar 20–100 produk.
- Masalah: sulit mengetahui stok yang akan habis, waktu pembelian, jumlah
  pembelian, dan perubahan tren penjualan.
- Fitur pertama: validasi dan eksplorasi data dari `sales.csv` dan
  `inventory.csv`, ringkasan penjualan, forecast baseline 7 hari, dan
  rekomendasi restock yang dapat dijelaskan.

## Choices

- Language and framework: Python; Pandas atau Polars; scikit-learn; FastAPI;
  Streamlit.
- Where it will run: lokal terlebih dahulu, lalu deployment menggunakan Docker
  dan Docker Compose.
- Data it needs to keep: produk, penjualan, stok, forecast, serta hasil aktual
  untuk evaluasi.
- Things we will leave for later: OCR struk, WhatsApp, integrasi kasir,
  pembayaran, multi-cabang, aplikasi mobile native, pembelian otomatis, dan
  model LSTM atau Transformer.

## MVP scope

MVP harus mendukung upload CSV, validasi dan pembersihan data, pencatatan
produk dan stok, ringkasan penjualan, grafik harian, prediksi 7 hari,
rekomendasi restock dengan alasan yang mudah dipahami, penyimpanan database,
API, dan dashboard.

Keputusan pembelian tetap berada pada pemilik usaha. Sistem hanya memberi
rekomendasi dan tidak membeli stok secara otomatis.

## First-phase acceptance criteria

- [ ] Satu segmen pengguna dipilih dan masalahnya divalidasi melalui wawancara
      dengan minimal tiga pemilik atau pengelola kedai.
- [x] Dataset contoh sintetis yang realistis tersedia di `data/sample/`.
- [x] Format `sales.csv` dan `inventory.csv` terdokumentasi di dashboard dan
      `STOKBIJAK_PRODUCT_PLAN.md`.
- [x] Pipeline cleaning dan validasi sederhana tersedia di `app/domain.py`.
- [x] EDA awal tersedia melalui ringkasan, grafik harian, dan produk terlaris.
- [x] Baseline forecasting 7 hari tersedia dan dapat dibandingkan dengan
      aktual.

## Current task

- The user action and result we need: unggah `sales.csv` dan `inventory.csv`
  atau gunakan contoh bawaan, lalu lihat ringkasan, forecast baseline, dan
  rekomendasi restock.
- How we will check that result: jalankan test domain, lint, buka dashboard
  Streamlit, dan coba alur contoh serta CSV yang tidak valid.
- Relevant files or components: `app/domain.py`, `app/streamlit_app.py`,
  `data/sample/`, `tests/test_domain.py`, dan `docs/PROBLEM_VALIDATION.md`.
- Known failure or current baseline: validasi langsung melalui wawancara belum
  dilakukan; database, API, dan model ML belum termasuk irisan pertama.
- Remaining work and next step: uji coba dengan minimal satu pemilik kedai,
  bandingkan rekomendasi dengan keputusan nyata, lalu iterasikan kontrak data.

## Commands

- Prepare starter skills: `npm run setup`
- Check starter kit: `npm run check:starter`
- Check configured project commands: `npm run check:project`
- Create environment: `python3 -m venv .venv && .venv/bin/python -m pip install -r requirements-dev.txt`
- Start the app: `.venv/bin/streamlit run app/streamlit_app.py`
- Run app tests: `.venv/bin/python -m unittest discover -s tests -p 'test_*.py'`
- Check code style: `.venv/bin/ruff check app tests`
- Check types, if used: belum dikonfigurasi; type checker belum dipakai pada irisan awal.
- Build, if needed: tidak berlaku; Streamlit dijalankan sebagai aplikasi Python.

## Accepted decisions

- `STOKBIJAK_PRODUCT_PLAN.md` menjadi sumber rencana produk lengkap; file ini
  menyimpan kontrak proyek yang ringkas dan dapat diperbarui.
- MVP berfokus pada satu segmen, yaitu kedai minuman kecil, agar manfaat utama
  dapat divalidasi sebelum menambah fitur lain.
- Kualitas data dan baseline harus dibuktikan sebelum memakai model yang lebih
  kompleks.
- Validasi internet hanya dipakai sebagai bukti sekunder; keputusan product-market
  fit tetap menunggu wawancara langsung.
- Vertical slice pertama sengaja memakai Streamlit dan fungsi domain murni tanpa
  database/API agar alur utama dapat diuji lebih cepat.
- `stok_minimum` dipakai sebagai proxy safety stock dan kolom inventori opsional
  diberi default aman; asumsi ini harus dikonfirmasi saat uji pengguna.
- Stack awal mengikuti rencana produk: Python, Pandas atau Polars,
  scikit-learn, FastAPI, PostgreSQL, Streamlit, Docker, dan Git.
- Sumber keputusan: bagian 1, 3, 5, 7, 17, dan 18 dari
  `STOKBIJAK_PRODUCT_PLAN.md`.
