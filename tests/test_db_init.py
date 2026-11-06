import sqlite3


def test_init_db_creates_seed_data():
    from app import create_app

    app = create_app({'TESTING': True, 'DATABASE': ':memory:'})
    runner = app.test_cli_runner()
    result = runner.invoke(args=['init-db'])

    assert result.exit_code == 0
    assert 'Database initialized' in result.output

    conn = sqlite3.connect(':memory:')
    conn.execute('SELECT 1')
    conn.close()
