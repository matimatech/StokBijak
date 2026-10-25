# StokBijak — Product Plan

> Dokumen ini adalah titik awal pembangunan produk machine learning end-to-end untuk membantu UMKM mengelola stok dan memprediksi penjualan.

**Tanggal dibuat:** 25 Oktober 2026
**Status:** Perencanaan awal
**Target MVP:** Asisten stok dan penjualan untuk kedai minuman

---

## 1. Ringkasan Produk

### Nama kerja

**StokBijak**

### Masalah yang ingin diselesaikan

Pemilik kedai minuman sering mengalami kesulitan dalam:

- Mengetahui produk yang akan habis.
- Menentukan kapan harus membeli stok.
- Menentukan jumlah stok yang perlu dibeli.
- Memahami produk yang penjualannya meningkat atau menurun.
- Memperkirakan penjualan beberapa hari ke depan.

### Solusi

StokBijak menerima data penjualan dan stok, kemudian memberikan:

- Ringkasan performa penjualan.
- Prediksi penjualan 7 hari ke depan.
- Peringatan produk yang berisiko kehabisan stok.
- Rekomendasi jumlah restock.
- Alasan yang mudah dipahami untuk setiap rekomendasi.

### Target pengguna awal

Pemilik atau pengelola **kedai minuman kecil** dengan sekitar 20–100 produk dan pencatatan penjualan melalui CSV, spreadsheet, atau input manual.

### Hipotesis produk

> Jika pemilik kedai mendapatkan prediksi penjualan dan rekomendasi restock yang sederhana dan mudah dipahami, mereka dapat mengurangi kehabisan stok serta menghemat waktu dalam menentukan pembelian.

---

## 2. Tujuan Pembelajaran

Produk ini dibangun untuk melatih seluruh alur pengembangan produk machine learning:

- Product discovery dan wawancara pengguna.
- Data collection dan data validation.
- Data cleaning dan exploratory data analysis.
- Time-series forecasting.
- Feature engineering.
- Evaluasi model.
- Pembangunan REST API.
- Database dan data modeling.
- Dashboard aplikasi.
- Deployment menggunakan Docker.
- Monitoring model dan data drift.
- Iterasi berdasarkan feedback pengguna.

---

## 3. Batasan MVP

### Fitur yang wajib dibuat

1. Upload data penjualan melalui CSV.
2. Validasi dan pembersihan data.
3. Pencatatan data produk dan stok.
4. Dashboard ringkasan penjualan.
5. Prediksi penjualan 7 hari ke depan.
6. Rekomendasi restock.
7. Penjelasan untuk setiap rekomendasi.
8. Penyimpanan data ke database.
9. API untuk mengakses data, prediksi, dan rekomendasi.
10. Deployment aplikasi agar dapat dicoba melalui URL.

### Fitur yang belum termasuk MVP

- OCR struk.
- Chatbot WhatsApp.
- Integrasi dengan aplikasi kasir.
- Pembayaran.
- Dukungan multi-cabang.
- Aplikasi mobile native.
- Prediksi harga.
- Rekomendasi pemasok.
- Pembelian stok secara otomatis.
- Model deep learning seperti LSTM atau Transformer.

Fitur tambahan hanya dikerjakan setelah MVP digunakan oleh pengguna nyata dan masalah utamanya telah tervalidasi.

---

## 4. Kriteria Keberhasilan MVP

MVP dianggap selesai apabila:

- [ ] Pengguna dapat mengunggah CSV.
- [ ] Sistem dapat mendeteksi kolom atau nilai yang tidak valid.
- [ ] Sistem dapat menampilkan ringkasan penjualan.
- [ ] Sistem dapat menampilkan grafik penjualan harian.
- [ ] Sistem dapat membuat prediksi penjualan 7 hari.
- [ ] Sistem dapat memberikan rekomendasi jumlah restock.
- [ ] Setiap rekomendasi memiliki alasan yang dapat dipahami.
- [ ] Data dapat disimpan dan dibuka kembali.
- [ ] Aplikasi dapat dijalankan melalui URL.
- [ ] Minimal satu pengguna mencoba aplikasi menggunakan data nyata.
- [ ] Prediksi dapat dibandingkan dengan penjualan aktual.

### Sasaran awal untuk eksperimen

Sasaran berikut adalah target eksperimen, bukan jaminan hasil:

- Analisis data selesai dalam waktu kurang dari satu menit.
- WAPE awal berada di bawah 30–40% untuk produk dengan data yang cukup.
- Pengguna dapat memahami rekomendasi tanpa penjelasan langsung.
- Pengguna bersedia menggunakan aplikasi kembali.
- Kejadian kehabisan stok berkurang setelah beberapa siklus penggunaan.

---

## 5. Rencana Validasi Masalah

Sebelum membuat model, lakukan wawancara kepada 3–5 pemilik kedai minuman.

### Pertanyaan wawancara

1. Bagaimana penjualan dicatat saat ini?
2. Seberapa sering kedai mengalami kehabisan stok?
3. Produk apa yang paling sering habis?
4. Bagaimana cara menentukan waktu pembelian stok?
5. Apa dampak stok habis terhadap bisnis?
6. Apakah tersedia data penjualan selama 1–3 bulan terakhir?
7. Seberapa sering stok diperbarui?
8. Apakah ada hari ketika kedai tutup?
9. Apakah terdapat promosi atau event tertentu?
10. Apakah bersedia mencoba dashboard sederhana?

### Output validasi

- [ ] Satu segmen pengguna yang dipilih.
- [ ] Contoh dataset penjualan nyata atau sintetis yang realistis.
- [ ] Masalah utama yang paling sering dialami.
- [ ] Format data yang tersedia.
- [ ] Minimal satu calon pengguna untuk uji coba MVP.

---

## 6. Format Data Awal

### File penjualan: `sales.csv`

```csv
tanggal,produk,jumlah_terjual,harga_satuan
2026-01-01,Kopi Susu,25,12000
2026-01-01,Teh Manis,18,7000
2026-01-02,Kopi Susu,31,12000
```

### File stok: `inventory.csv`

```csv
produk,stok_saat_ini,waktu_pengiriman_hari,stok_minimum
Kopi Susu,40,2,10
Teh Manis,25,3,8
```

### Data produk yang akan dibutuhkan

| Kolom | Keterangan |
|---|---|
| `product_id` | ID unik produk |
| `product_name` | Nama produk |
| `category` | Kategori produk |
| `unit_price` | Harga jual |
| `lead_time_days` | Waktu tunggu pemasok |
| `minimum_order_qty` | Jumlah pembelian minimum |

### Validasi data

Sistem harus memeriksa:

- Tanggal tidak boleh kosong.
- Format tanggal harus benar.
- Jumlah terjual tidak boleh negatif.
- Harga tidak boleh negatif.
- Nama produk harus konsisten.
- Tidak boleh ada baris duplikat.
- Kolom wajib harus tersedia.
- Periode data harus cukup untuk forecasting.
- Hari tanpa transaksi harus dibedakan dari data yang belum dimasukkan.
- Hari kedai tutup harus dapat ditandai.

> Data tanpa transaksi tidak selalu berarti penjualan bernilai nol. Bisa jadi kedai tutup atau data belum dicatat.

---

## 7. Arsitektur Sistem

```text
CSV / Input Manual
        ↓
Validasi Data
        ↓
Data Cleaning
        ↓
Database
        ↓
Feature Engineering
        ↓
Model Forecasting
        ↓
Rekomendasi Restock
        ↓
API
        ↓
Dashboard Pengguna
        ↓
Feedback dan Monitoring
```

### Stack MVP

- **Python** untuk bahasa utama.
- **Pandas atau Polars** untuk pengolahan data.
- **Scikit-learn** untuk model machine learning.
- **FastAPI** untuk REST API.
- **PostgreSQL** untuk database.
- **Streamlit** untuk dashboard awal.
- **Docker dan Docker Compose** untuk menjalankan aplikasi.
- **Git** untuk version control.

Gunakan Streamlit terlebih dahulu agar fokus tetap pada kualitas data, model, dan manfaat produk. Frontend terpisah seperti React atau Next.js dapat dipertimbangkan setelah MVP tervalidasi.

---

## 8. Struktur Data Database

### Tabel `products`

| Kolom | Keterangan |
|---|---|
| `id` | ID produk |
| `name` | Nama produk |
| `category` | Kategori produk |
| `unit_price` | Harga jual |
| `lead_time_days` | Waktu tunggu pemasok |
| `minimum_order_qty` | Jumlah pembelian minimum |

### Tabel `sales`

| Kolom | Keterangan |
|---|---|
| `id` | ID transaksi |
| `sale_date` | Tanggal penjualan |
| `product_id` | ID produk |
| `quantity` | Jumlah terjual |
| `unit_price` | Harga saat transaksi |
| `total_amount` | Total nilai transaksi |

### Tabel `inventory`

| Kolom | Keterangan |
|---|---|
| `product_id` | ID produk |
| `recorded_at` | Waktu pencatatan |
| `current_stock` | Stok saat ini |
| `incoming_stock` | Stok yang sedang dipesan |
| `minimum_stock` | Batas stok minimum |

### Tabel `forecasts`

| Kolom | Keterangan |
|---|---|
| `product_id` | ID produk |
| `forecast_date` | Tanggal prediksi |
| `predicted_quantity` | Jumlah prediksi |
| `model_version` | Versi model |
| `created_at` | Waktu prediksi dibuat |

---

## 9. Strategi Machine Learning

### Tahap 1: Baseline

Buat model sederhana sebelum menggunakan machine learning:

1. Moving average dari beberapa hari terakhir.
2. Penjualan pada hari yang sama di minggu sebelumnya.
3. Rata-rata penjualan mingguan.

Baseline wajib digunakan sebagai pembanding. Model yang lebih kompleks hanya dipakai jika benar-benar memberikan hasil yang lebih baik.

### Tahap 2: Feature engineering

Fitur awal:

```text
lag_1
lag_7
rolling_mean_7
rolling_mean_14
is_weekend
trend
unit_price
```

Tambahkan fitur promosi, hari libur, atau event hanya jika datanya benar-benar tersedia dan konsisten.

### Tahap 3: Model awal

Mulai dengan salah satu model berikut:

- `HistGradientBoostingRegressor`.
- `RandomForestRegressor`.
- Model gradient boosting lain setelah baseline stabil.

Jangan langsung menggunakan LSTM atau Transformer. Dengan data yang terbatas, model tabular dengan fitur lag lebih mudah dijelaskan, diuji, dan dipelihara.

### Tahap 4: Evaluasi

Gunakan pembagian berdasarkan waktu:

```text
70% data awal   → training
15% berikutnya  → validation
15% terakhir    → testing
```

Metrik yang digunakan:

- MAE.
- RMSE.
- WAPE.
- MAPE jika data tidak banyak memiliki nilai nol.

Evaluasi harus dilakukan per produk dan secara keseluruhan. Produk terlaris perlu mendapat perhatian khusus karena kesalahan prediksinya memiliki dampak bisnis lebih besar.

---

## 10. Logika Rekomendasi Restock

### Formula awal

```text
Kebutuhan restock =
    prediksi kebutuhan selama lead time
    + safety stock
    - stok saat ini
    - stok yang sedang dikirim
```

Jika hasilnya kurang dari nol, rekomendasi pembelian menjadi nol.

Jika pemasok memiliki jumlah pembelian minimum, bulatkan hasil ke kelipatan `minimum_order_qty`.

### Contoh

```text
Prediksi kebutuhan 3 hari = 60 unit
Safety stock              = 15 unit
Stok saat ini             = 20 unit
Stok sedang dikirim       = 0 unit

Rekomendasi = 60 + 15 - 20 - 0
            = 55 unit
```

### Contoh penjelasan kepada pengguna

> Beli 55 unit karena stok saat ini diperkirakan hanya cukup untuk 1 hari, sedangkan waktu pengiriman pemasok adalah 3 hari.

Sistem hanya memberikan rekomendasi. Pemilik usaha tetap dapat mengubah jumlah pembelian sebelum mengambil keputusan.


---

## 11. Roadmap 10 Minggu

### Minggu 1 — Validasi masalah

- [ ] Pilih jenis kedai yang akan menjadi fokus.
- [ ] Wawancarai 3–5 pemilik kedai.
- [ ] Kumpulkan contoh data penjualan.
- [ ] Tentukan masalah utama.
- [ ] Susun definisi keberhasilan produk.

**Output:** profil pengguna, contoh dataset, dan ruang lingkup MVP.

### Minggu 2 — Data pipeline

- [ ] Tentukan format CSV.
- [ ] Buat proses upload data.
- [ ] Validasi kolom dan tipe data.
- [ ] Tangani data kosong, duplikat, dan tanggal salah.
- [ ] Simpan dataset bersih.

**Output:** data contract dan pipeline cleaning.

### Minggu 3 — Dashboard dasar

- [ ] Tampilkan total penjualan.
- [ ] Tampilkan produk terlaris.
- [ ] Buat grafik penjualan harian.
- [ ] Tambahkan filter produk dan tanggal.
- [ ] Tampilkan stok saat ini.

**Output:** dashboard analitik tanpa model machine learning.

### Minggu 4 — Model baseline

- [ ] Implementasikan moving average.
- [ ] Implementasikan seasonal naive.
- [ ] Buat evaluasi berbasis waktu.
- [ ] Hitung MAE, WAPE, dan RMSE.
- [ ] Simpan hasil eksperimen.

**Output:** model baseline dan tabel perbandingan performa.

### Minggu 5 — Model machine learning

- [ ] Buat fitur lag.
- [ ] Buat fitur rolling average.
- [ ] Tambahkan fitur hari dalam minggu.
- [ ] Latih model berbasis tree.
- [ ] Bandingkan hasil dengan baseline.

**Output:** model forecasting versi pertama.

### Minggu 6 — Rekomendasi restock

- [ ] Tambahkan data lead time.
- [ ] Hitung safety stock.
- [ ] Implementasikan formula restock.
- [ ] Tambahkan minimum order quantity.
- [ ] Tampilkan alasan setiap rekomendasi.

**Output:** halaman rekomendasi restock.

### Minggu 7 — Backend dan database

- [ ] Buat database PostgreSQL.
- [ ] Buat tabel produk, penjualan, stok, dan forecast.
- [ ] Buat endpoint API.
- [ ] Tambahkan validasi request.
- [ ] Pisahkan modul data, model, dan rekomendasi.

**Output:** API yang dapat digunakan dashboard.

### Minggu 8 — Deployment

- [ ] Buat `Dockerfile`.
- [ ] Buat `docker-compose.yml`.
- [ ] Pisahkan environment development dan production.
- [ ] Deploy API, database, dan dashboard.
- [ ] Tambahkan logging dasar.

**Output:** aplikasi yang dapat diakses melalui URL.

### Minggu 9 — Uji coba pengguna

- [ ] Pilih 1–3 pengguna awal.
- [ ] Minta mereka mengunggah data.
- [ ] Amati apakah mereka memahami rekomendasi.
- [ ] Catat rekomendasi yang diterima atau ditolak.
- [ ] Kumpulkan feedback.

**Output:** feedback pengguna dan daftar perbaikan usability.

### Minggu 10 — Monitoring dan perbaikan

- [ ] Simpan prediksi dan hasil aktual.
- [ ] Bandingkan prediksi dengan penjualan nyata.
- [ ] Pantau error model dari waktu ke waktu.
- [ ] Tambahkan deteksi perubahan pola penjualan.
- [ ] Tentukan jadwal retraining.

**Output:** monitoring akurasi dan versi MVP yang lebih stabil.

---

## 12. Struktur Direktori yang Disarankan

```text
stokbijak/
├── app/
│   ├── api/
│   ├── dashboard/
│   ├── services/
│   └── main.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
├── ml/
│   ├── preprocessing.py
│   ├── features.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
├── database/
│   ├── models.py
│   └── migrations/
├── tests/
├── notebooks/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

Pisahkan sejak awal komponen berikut:

- Pengolahan data.
- Training model.
- Prediksi.
- Logika rekomendasi.
- API.
- Dashboard.

Hindari membuat seluruh sistem di dalam satu notebook besar karena akan sulit diuji dan di-deploy.

---

## 13. Endpoint API Awal

```text
POST /sales/upload
GET  /sales/summary
GET  /forecast/{product_id}
GET  /inventory/recommendations
POST /inventory/update
```

Endpoint dapat berubah setelah struktur data dan kebutuhan pengguna lebih jelas.

---

## 14. Risiko dan Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Data penjualan terlalu sedikit | Prediksi tidak stabil | Mulai dari baseline dan tampilkan confidence level |
| Nama produk tidak konsisten | Data terpecah | Buat master produk dan normalisasi nama |
| Data stok tidak diperbarui | Restock tidak akurat | Tampilkan waktu pembaruan stok |
| Hari tutup dianggap penjualan nol | Model bias | Tambahkan penanda hari tutup |
| Pengguna tidak memahami prediksi | Rekomendasi tidak dipakai | Gunakan bahasa sederhana dan alasan yang jelas |
| Model kompleks tidak lebih baik | Waktu pengembangan terbuang | Bandingkan selalu dengan baseline |
| Rekomendasi terlalu dipercaya | Risiko keputusan bisnis | Tampilkan rekomendasi sebagai bantuan, bukan keputusan otomatis |

---

## 15. Prinsip Produk

1. **Mulai dari satu segmen pengguna.** Jangan langsung menyelesaikan semua masalah UMKM.
2. **Kualitas data lebih penting daripada model kompleks.**
3. **Pisahkan prediksi dari keputusan bisnis.** Model memprediksi; aturan bisnis menentukan rekomendasi.
4. **Tampilkan alasan di balik rekomendasi.** Pengguna harus dapat memeriksa hasilnya.
5. **Jangan otomatis membeli stok.** Keputusan akhir tetap berada di tangan pemilik usaha.
6. **Uji dengan data nyata sedini mungkin.**
7. **Ukur manfaat bisnis, bukan hanya akurasi model.**

---

## 16. Metrik Produk

### Metrik machine learning

- MAE.
- RMSE.
- WAPE.
- Error per produk.
- Perbedaan antara prediksi dan penjualan aktual.

### Metrik bisnis

- Jumlah kejadian kehabisan stok.
- Jumlah stok berlebih.
- Produk terbuang.
- Waktu yang dihemat pengguna.
- Persentase rekomendasi yang diikuti.
- Jumlah pengguna yang kembali menggunakan aplikasi.

---

## 17. Langkah Pertama yang Harus Dikerjakan

Mulai dengan urutan berikut:

1. Pilih satu kedai minuman sebagai target awal.
2. Wawancarai minimal tiga pemilik atau pengelola kedai.
3. Minta contoh data penjualan 1–3 bulan jika memungkinkan.
4. Buat dataset sintetis jika data nyata belum tersedia.
5. Tetapkan format `sales.csv` dan `inventory.csv`.
6. Buat proyek Python sederhana.
7. Implementasikan validasi dan eksplorasi data sebelum membuat model.

### Fokus MVP dalam satu kalimat

> StokBijak membantu pemilik kedai mengetahui produk mana yang perlu dibeli dalam 7 hari ke depan dan berapa jumlahnya.

Jangan menambahkan fitur lain sebelum alur utama tersebut dapat digunakan dari awal sampai akhir.

---

## 18. Definisi Selesai untuk Fase Awal

Fase awal dianggap selesai apabila kamu sudah memiliki:

- [ ] Masalah yang tervalidasi.
- [ ] Target pengguna yang spesifik.
- [ ] Dataset contoh.
- [ ] Format data yang terdokumentasi.
- [ ] Repository proyek.
- [ ] Pipeline cleaning sederhana.
- [ ] EDA awal.
- [ ] Baseline forecasting.
- [ ] Catatan hasil eksperimen.

Setelah checklist ini selesai, lanjutkan ke implementasi model machine learning dan dashboard.
