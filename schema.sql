PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('customer', 'admin', 'teknisi'))
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    nama_customer TEXT NOT NULL,
    email_customer TEXT NOT NULL UNIQUE,
    no_telp_customer TEXT,
    alamat_customer TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    nama_admin TEXT NOT NULL,
    email_admin TEXT NOT NULL UNIQUE,
    no_telp_admin TEXT,
    username_admin TEXT NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS teknisi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    nama_teknisi TEXT NOT NULL,
    bidang_keahlian TEXT NOT NULL,
    email_teknisi TEXT NOT NULL UNIQUE,
    no_telp_teknisi TEXT,
    username_teknisi TEXT NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS permasalahan (
    id_permasalahan INTEGER PRIMARY KEY AUTOINCREMENT,
    id_customer INTEGER NOT NULL,
    id_admin INTEGER,
    id_teknisi INTEGER,
    judul_permasalahan TEXT NOT NULL,
    deskripsi_permasalahan TEXT NOT NULL,
    tanggal_permasalahan TEXT NOT NULL,
    prioritas TEXT NOT NULL CHECK (prioritas IN ('Rendah', 'Sedang', 'Tinggi', 'Kritis')),
    status TEXT NOT NULL CHECK (status IN ('Baru', 'Diproses', 'Menunggu', 'Selesai')) DEFAULT 'Baru',
    FOREIGN KEY (id_customer) REFERENCES customers(id),
    FOREIGN KEY (id_admin) REFERENCES admins(id),
    FOREIGN KEY (id_teknisi) REFERENCES teknisi(id)
);
