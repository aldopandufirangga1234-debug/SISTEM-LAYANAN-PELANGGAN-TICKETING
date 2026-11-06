import os
import sqlite3
from datetime import datetime

from flask import Flask, current_app, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'ticketing.db')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db


def close_db(_error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with open(os.path.join(BASE_DIR, 'schema.sql'), 'r', encoding='utf-8') as f:
        db.executescript(f.read())

    password_hash = generate_password_hash('rahasia123')

    users = [
        ('customer1', 'customer', password_hash),
        ('admin1', 'admin', password_hash),
        ('admin2', 'admin', password_hash),
        ('teknisi1', 'teknisi', password_hash),
        ('teknisi2', 'teknisi', password_hash),
        ('teknisi3', 'teknisi', password_hash),
    ]

    for username, role, password in users:
        db.execute(
            'INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)',
            (username, password, role),
        )

    customer_user_id = db.execute(
        'SELECT id FROM users WHERE username = ?', ('customer1',)
    ).fetchone()['id']
    admin1_id = db.execute(
        'SELECT id FROM users WHERE username = ?', ('admin1',)
    ).fetchone()['id']
    admin2_id = db.execute(
        'SELECT id FROM users WHERE username = ?', ('admin2',)
    ).fetchone()['id']
    teknisi1_id = db.execute(
        'SELECT id FROM users WHERE username = ?', ('teknisi1',)
    ).fetchone()['id']
    teknisi2_id = db.execute(
        'SELECT id FROM users WHERE username = ?', ('teknisi2',)
    ).fetchone()['id']
    teknisi3_id = db.execute(
        'SELECT id FROM users WHERE username = ?', ('teknisi3',)
    ).fetchone()['id']

    db.execute(
        '''
        INSERT OR IGNORE INTO customers (user_id, nama_customer, email_customer, no_telp_customer, alamat_customer)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (customer_user_id, 'Budi Santoso', 'budi@example.com', '081234567890', 'Bandung'),
    )

    customer_row = db.execute(
        'SELECT id FROM customers WHERE email_customer = ?', ('budi@example.com',)
    ).fetchone()
    customer_id = customer_row['id'] if customer_row else 1

    db.execute(
        '''
        INSERT OR IGNORE INTO admins (user_id, nama_admin, email_admin, no_telp_admin, username_admin)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (admin1_id, 'Rina Admin', 'rina@example.com', '081111111111', 'admin1'),
    )
    db.execute(
        '''
        INSERT OR IGNORE INTO admins (user_id, nama_admin, email_admin, no_telp_admin, username_admin)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (admin2_id, 'Doni Admin', 'doni@example.com', '082222222222', 'admin2'),
    )

    db.execute(
        '''
        INSERT OR IGNORE INTO teknisi (user_id, nama_teknisi, bidang_keahlian, email_teknisi, no_telp_teknisi, username_teknisi)
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        (teknisi1_id, 'Andi Teknik', 'Jaringan', 'andi@example.com', '083111111111', 'teknisi1'),
    )
    db.execute(
        '''
        INSERT OR IGNORE INTO teknisi (user_id, nama_teknisi, bidang_keahlian, email_teknisi, no_telp_teknisi, username_teknisi)
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        (teknisi2_id, 'Sari Teknik', 'Hardware', 'sari@example.com', '083222222222', 'teknisi2'),
    )
    db.execute(
        '''
        INSERT OR IGNORE INTO teknisi (user_id, nama_teknisi, bidang_keahlian, email_teknisi, no_telp_teknisi, username_teknisi)
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        (teknisi3_id, 'Joko Teknik', 'Software', 'joko@example.com', '083333333333', 'teknisi3'),
    )

    admin_data = db.execute('SELECT id, nama_admin FROM admins ORDER BY id LIMIT 1').fetchone()
    admin_id = admin_data['id'] if admin_data else 1
    teknisi_data = db.execute('SELECT id, nama_teknisi FROM teknisi ORDER BY id LIMIT 1').fetchone()
    teknisi_id = teknisi_data['id'] if teknisi_data else 1

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    permasalahan = [
        (customer_id, admin_id, teknisi_id, 'Jaringan Internet Lambat', 'Internet di kantor sering lambat dan putus saat jam sibuk.', 'Tinggi', 'Diproses', now),
        (customer_id, admin_id, teknisi_id + 1 if teknisi_id + 1 <= 3 else 1, 'Akun Tidak Bisa Login', 'User tidak bisa masuk ke sistem karena password tidak valid.', 'Sedang', 'Baru', now),
        (customer_id, admin_id, teknisi_id + 2 if teknisi_id + 2 <= 3 else 1, 'Server Sering Mati', 'Server utama sering restart tanpa sebab saat digunakan.', 'Kritis', 'Diproses', now),
    ]

    for item in permasalahan:
        db.execute(
            '''
            INSERT OR IGNORE INTO permasalahan (
                id_customer,
                id_admin,
                id_teknisi,
                judul_permasalahan,
                deskripsi_permasalahan,
                prioritas,
                status,
                tanggal_permasalahan
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            item,
        )

    db.commit()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='ticketing-secret-key',
        DATABASE=DB_PATH,
    )
    if test_config:
        app.config.update(test_config)

    app.teardown_appcontext(close_db)

    @app.cli.command('init-db')
    def init_db_command():
        with app.app_context():
            init_db()
        print('Database initialized')

    @app.route('/')
    def index():
        if 'user' not in session:
            return redirect(url_for('login'))
        return redirect(url_for('dashboard'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            db = get_db()
            user = db.execute(
                'SELECT * FROM users WHERE username = ?',
                (username,),
            ).fetchone()

            if user and check_password_hash(user['password_hash'], password):
                session['user'] = user['username']
                session['role'] = user['role']
                return redirect(url_for('dashboard'))
            flash('Username atau password salah.')
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('user', None)
        session.pop('role', None)
        return redirect(url_for('login'))

    @app.route('/dashboard', methods=['GET'])
    def dashboard():
        if 'user' not in session:
            return redirect(url_for('login'))

        db = get_db()
        tickets = db.execute(
            'SELECT * FROM permasalahan ORDER BY tanggal_permasalahan DESC'
        ).fetchall()
        stats = {
            'total': len(tickets),
            'baru': sum(1 for item in tickets if item['status'] == 'Baru'),
            'diproses': sum(1 for item in tickets if item['status'] == 'Diproses'),
            'selesai': sum(1 for item in tickets if item['status'] == 'Selesai'),
        }
        return render_template('dashboard.html', tickets=tickets, stats=stats)

    @app.route('/ticket', methods=['POST'])
    def create_ticket():
        if 'user' not in session:
            return redirect(url_for('login'))

        title = request.form.get('title', '').strip()
        customer = request.form.get('customer', '').strip()
        category = request.form.get('category', '').strip()
        priority = request.form.get('priority', '').strip()
        description = request.form.get('description', '').strip()

        if not all([title, customer, category, priority]):
            flash('Semua field wajib diisi.')
            return redirect(url_for('dashboard'))

        db = get_db()
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute(
            '''
            INSERT INTO permasalahan (id_customer, id_admin, id_teknisi, judul_permasalahan, deskripsi_permasalahan, prioritas, status, tanggal_permasalahan)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                1,
                1,
                1,
                title,
                description or f'Keluhan dari pelanggan {customer} dengan kategori {category}',
                priority,
                'Baru',
                created_at,
            ),
        )
        db.commit()
        flash('Ticket berhasil dibuat.')
        return redirect(url_for('dashboard'))

    @app.route('/ticket/<int:ticket_id>/status', methods=['POST'])
    def update_ticket_status(ticket_id):
        if 'user' not in session:
            return redirect(url_for('login'))

        status = request.form.get('status', 'Baru')
        db = get_db()
        db.execute('UPDATE permasalahan SET status = ? WHERE id_permasalahan = ?', (status, ticket_id))
        db.commit()
        flash('Status tiket berhasil diperbarui.')
        return redirect(url_for('dashboard'))

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
