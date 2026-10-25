# Validasi Masalah StokBijak

Status: **validasi sekunder**, 26 Oktober 2026.

Dokumen ini memakai data internet untuk menguji apakah masalah manajemen stok
relevan sebelum wawancara langsung dilakukan. Temuan ini mendukung hipotesis
masalah, tetapi **belum menggantikan wawancara dengan minimal tiga pemilik kedai**.

## Temuan utama

1. Sektor makanan dan minuman cukup besar untuk menjadi segmen awal. Statistik
   BPS 2024 mencatat sekitar 5,28 juta usaha penyedia makanan dan minuman di
   Indonesia. Sekitar 50,65% tercatat menggunakan internet, sehingga produk
   sederhana berbasis dashboard memiliki konteks adopsi yang masuk akal, tetapi
   tidak boleh mengasumsikan semua usaha siap memakai aplikasi.
2. Studi kasus IPB University pada Bali Food Industry menemukan masalah
   **stock out** dan **over stock** pada UMKM makanan dan minuman. Studi tersebut
   memakai safety stock, reorder point, dan EOQ; hasil kasusnya menunjukkan
   efisiensi biaya 5,23% dibandingkan cara sebelumnya.
3. Studi Bank Indonesia tentang adopsi digital UMSE menempatkan pencatatan
   transaksi, inventaris, dan keputusan usaha sebagai bagian dari area digital
   yang perlu diperkuat. Ini mendukung pilihan untuk memulai dari CSV dan
   rekomendasi yang dapat dijelaskan, bukan langsung dari model kompleks.

## Kesimpulan produk

Hipotesis awal cukup kuat untuk membangun **vertical slice** kecil:

> Pemilik kedai minuman akan lebih mudah menentukan pembelian jika mereka dapat
> mengunggah data penjualan dan stok, melihat data yang bermasalah, lalu menerima
> rekomendasi restock dengan alasan yang dapat diperiksa.

Irisan yang dibangun sekarang sengaja tidak mengklaim bahwa masalah sudah
tervalidasi secara primer. Produk menampilkan asumsi dan peringatan agar pengguna
tidak memperlakukan forecast sebagai keputusan otomatis.

## Keputusan scope berdasarkan bukti

- Mulai dengan CSV karena format ini lebih ringan daripada integrasi kasir.
- Tampilkan validasi dan peringatan kualitas data sebelum hasil analitik.
- Gunakan baseline rata-rata 7 hari sebagai pembanding yang mudah dijelaskan.
- Gunakan `stok_minimum` sebagai proxy safety stock sementara data variasi
  permintaan belum tersedia.
- Minta wawancara langsung berikutnya untuk menguji frekuensi stockout, cara
  pencatatan saat ini, dan apakah rekomendasi benar-benar dipakai.

## Pertanyaan yang masih harus dijawab oleh wawancara

- Apakah pemilik kedai memiliki data harian minimal 1–3 bulan?
- Apakah `stok_minimum` sudah dipahami atau perlu dihitung oleh sistem?
- Apakah keputusan pembelian memakai satuan produk, bahan baku, atau kemasan?
- Seberapa sering stok dalam perjalanan dan hari kedai tutup perlu dicatat?
- Apakah alasan rekomendasi lebih penting daripada angka forecast yang presisi?

## Sumber

- Badan Pusat Statistik, *Statistik Penyediaan Makanan Minuman 2024*:
  https://www.bps.go.id/id/publication/2025/12/31/e46a55af756331ede8016b91/statistik-penyediaan-makanan-minuman-2024.html
- Putra, Asnawi, dan Shalihati, IPB University, *Analisis Strategi Manajemen
  Persediaan Bahan Baku untuk Optimalisasi Bisnis UMKM. Studi Kasus: Bali Food
  Industry* (2024):
  https://repository.ipb.ac.id/handle/123456789/158491
- Bank Indonesia, *A Study of National Digital Adoption Index for Indonesian
  UMSEs (Expansion)*:
  https://www.bi.go.id/en/publikasi/kajian/Pages/A-Study-Of-National-Digital-Adoption-Index-For-Indonesian-Umses-%28Expansion%29.aspx
