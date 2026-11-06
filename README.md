# SISTEM LAYANAN PELANGGAN TICKETING

Sistem Layanan Pelanggan Ticketing adalah aplikasi berbasis web yang membantu perusahaan atau instansi menangani keluhan, permintaan, dan kebutuhan pelanggan secara terstruktur dan terdokumentasi. Setiap keluhan pelanggan dicatat dalam bentuk tiket, dikelola oleh admin atau petugas support, dan dipantau status penyelesaiannya sampai selesai.

## Deskripsi Proyek

Proyek ini bertujuan untuk memudahkan pengelolaan layanan pelanggan dengan pendekatan digital. Sistem ini memungkinkan pelanggan mengirimkan keluhan melalui tiket, sedangkan admin dapat memantau, mengubah status, dan menyelesaikan tiket dengan lebih cepat dan terorganisir.

## Entitas dan Atribut

### 1. Customer
- id_customer
- nama_customer
- email_customer
- no_telp_customer
- alamat_customer

### 2. Admin
- id_admin
- nama_admin
- email_admin
- no_telp_admin
- username_admin
- password_admin

### 3. Teknisi
- id_teknisi
- nama_teknisi
- bidang_keahlian
- email_teknisi
- no_telp_teknisi
- username_teknisi
- password_teknisi

### 4. Permasalahan
- id_permasalahan
- id_customer
- id_admin
- id_teknisi
- judul_permasalahan
- deskripsi_permasalahan
- tanggal_permasalahan
- prioritas
- status

## Fitur Utama

- Sistem login admin
- Dashboard ringkasan tiket
- Penambahan tiket baru
- Pemberian prioritas dan kategori tiket
- Update status tiket
- Pencatatan data pelanggan dan kebutuhan layanan
- Tampilan daftar tiket dan status penyelesaian

## Teknologi yang Digunakan

- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja2

## Struktur Proyek

```bash
SISTEM-LAYANAN-PELANGGAN-TICKETING/
├── app.py
├── schema.sql
├── requirements.txt
├── ticketing.db
├── README.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── login.html
│   └── dashboard.html
├── static/
│   └── style.css
└── tests/
    └── test_app.py
```

## Cara Menjalankan

1. Masuk ke direktori project:
   ```bash
   cd SISTEM-LAYANAN-PELANGGAN-TICKETING
   ```

2. Buat virtual environment dan aktifkan:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependency:
   ```bash
   pip install -r requirements.txt
   ```

4. Inisialisasi database:
   ```bash
   flask --app app init-db
   ```

5. Jalankan aplikasi:
   ```bash
   python app.py
   ```

6. Buka browser ke alamat:
   ```bash
   http://localhost:5000
   ```

## Login Default

- Username: admin1
- Password: rahasia123

## Manfaat

- Mempercepat proses penanganan keluhan pelanggan
- Menyediakan data tiket yang terdokumentasi dengan baik
- Menjadi solusi dasar sistem layanan pelanggan untuk pengembangan lebih lanjut

## Kesimpulan

Aplikasi ini adalah versi awal dari sistem layanan pelanggan ticketing yang dapat dikembangkan menjadi aplikasi yang lebih lengkap dengan fitur pengguna, role, notifikasi, laporan, dan integrasi layanan yang lebih luas.
