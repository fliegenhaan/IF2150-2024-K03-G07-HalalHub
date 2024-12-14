# HalalHub - Sistem Manajemen Toko Muslim
<p align="center">
  <img src="img/HalalHub_logo.jpg" alt="HalalHub Logo" style="width: 50%; max-width: 500px;"/>
</p>

HalalHub adalah program manajemen penjualan berbasis Python yang dirancang khusus untuk UMKM toko muslim. Aplikasi ini menggunakan GUI tkinter untuk antarmuka pengguna dan file CSV untuk manajemen data, menawarkan solusi lengkap untuk pengelolaan inventaris, pesanan, dan transaksi. Hal ini didasari oleh banyaknya UMKM toko Muslim masih mengandalkan sistem pencatatan manual yang rentan terhadap kesalahan dan tidak efisien. Produk Muslim memiliki karakteristik unik yang membutuhkan penanganan khusus dalam manajemen inventory. Kategorisasi produk yang spesifik seperti pakaian Muslim pria/wanita dan perlengkapan ibadah, ditambah dengan fluktuasi permintaan yang tinggi menjelang hari besar Islam, membutuhkan sistem pengelolaan stok yang cermat. Sistem notifikasi stok menjadi fitur krusial untuk mengantisipasi lonjakan permintaan dan memastikan ketersediaan produk. Melihat kebutuhan akan sistem manajemen yang terjangkau namun efektif, pendekatan ini memungkinkan UMKM untuk mengimplementasikan solusi digital tanpa perlu investasi besar dalam infrastruktur database yang kompleks. HalalHub hadir sebagai solusi yang memahami kebutuhan unik UMKM toko Muslim, membantu mereka bertransformasi digital dengan cara yang sederhana namun efektif, sambil tetap mempertahankan efisiensi operasional dan kemudahan penggunaan.

## Fitur Utama

- Manajemen produk (tambah, edit, hapus)
- Kategorisasi produk (pakaian muslim pria/wanita, perlengkapan ibadah, aksesori)
- Pencarian dan filter produk
- Manajemen stok otomatis
- Pengelolaan pesanan dan transaksi
- Sistem notifikasi stok menipis
- Laporan penjualan dan grafik visualisasi

## Cara Menjalankan Aplikasi

1. Pastikan Python 3.8+ terinstall di sistem anda
2. Install dependencies yang diperlukan:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi dari direktori root:
   ```bash
   python src/main.py
   ```

## Daftar Modul dan Pembagian Tugas

1. Modul Produk ([@danenftyessir](https://github.com/danenftyessir); [@ArdellAghna](https://github.com/ArdellAghna))
   - Manajemen produk (CRUD)
   - Filter dan pencarian produk
   - Pengelolaan stok
   - GUI: DaftarProduk, TambahProduk, EditProduk, DetailProduk
   - Status: ✅ Selesai

2. Modul Pesanan ([@fliegenhaan](https://github.com/fliegenhaan))
   - Input dan pengelolaan pesanan
   - Pembatalan pesanan
   - Status pesanan (pending/selesai/batal)
   - GUI: DaftarPesanan, InputPesanan, DetailPesanan
   - Status: ✅ Selesai

3. Modul Laporan ([@ArdellAghna](https://github.com/ArdellAghna); [@fliegenhaan](https://github.com/fliegenhaan))
   - Laporan penjualan
   - Visualisasi data dan grafik
   - Laporan stok
   - GUI: LaporanPenjualan, GrafikPenjualan
   - Status: ✅ Selesai

4. Modul Transaksi ([@danenftyessir](https://github.com/danenftyessir); [@ArdellAghna](https://github.com/ArdellAghna); [@AbizzarG](https://github.com/AbizzarG))
   - Riwayat transaksi
   - Detail transaksi
   - GUI: RiwayatTransaksi, DetailTransaksi
   - Status: ✅ Selesai


## Struktur Database (CSV)

### 1. produk.csv
| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| id_produk | String | Primary key |
| nama_produk | String | Nama produk |
| kategori | String | Kategori produk |
| harga | Float | Harga produk |
| stok | Integer | Jumlah stok |
| created_at | String | Timestamp pembuatan |
| updated_at | String | Timestamp update |

### 2. pesanan.csv
| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| id_pesanan | String | Primary key |
| id_pelanggan | String | ID pelanggan |
| id_produk | String | Foreign key ke produk |
| jumlah_dipesan | Integer | Jumlah pesanan |
| total_harga | Float | Total harga pesanan |
| status | String | Status pesanan |
| tanggal_pesanan | String | Timestamp pesanan |

### 3. transaksi.csv
| Kolom | Tipe Data | Keterangan |
|-------|-----------|------------|
| id_transaksi | String | Primary key |
| id_pesanan | String | Foreign key ke pesanan |
| total_harga | Float | Total transaksi |
| metode_pembayaran | String | Metode pembayaran |
| tanggal_transaksi | String | Timestamp transaksi |

## Links
- Form Asistensi : https://drive.google.com/file/d/1iRnU7xWbGLx2fMh09QVC8Oy0jJxRcan2/view?usp=sharing
