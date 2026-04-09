import sqlite3

DB_FILE = "database/universalbank.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    import os
    os.makedirs("database", exist_ok=True)
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            acc_num       TEXT    UNIQUE NOT NULL,
            branch        TEXT    NOT NULL,
            ifsc_code     TEXT    NOT NULL,
            mobile        TEXT    UNIQUE NOT NULL,
            username      TEXT    UNIQUE NOT NULL,
            password      TEXT    NOT NULL,
            balance       REAL    DEFAULT 0,
            credit_count  INTEGER DEFAULT 0,
            debit_count   INTEGER DEFAULT 0
        )
    ''')
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        sample_users = [
            ("Shubham Raut", "8631361646", "Pune",   "SBIN000523", "9876543210", "shubham", "pass1", 5000),
            ("Rahul Sharma", "9876543210", "Mumbai", "HDFC000123", "9123456780", "rahul",   "pass2", 12000),
            ("Priya Mehta",  "1122334455", "Delhi",  "ICIC000789", "9988776655", "priya",   "pass3", 8500),
        ]
        c.executemany(
            "INSERT INTO users (name,acc_num,branch,ifsc_code,mobile,username,password,balance) VALUES (?,?,?,?,?,?,?,?)",
            sample_users
        )
    conn.commit()
    conn.close()
