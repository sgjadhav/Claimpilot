import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "claimpilot.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            policy_type TEXT
        )
    ''')
    
    # Create claims table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            status TEXT,
            claim_amount REAL,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def seed_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if data already exists to prevent duplication on multiple runs
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        print("Database is already seeded. Skipping seed.")
        conn.close()
        return

    # Insert dummy user Alice
    cursor.execute('''
        INSERT INTO users (name, policy_type)
        VALUES ('Alice', 'Auto')
    ''')
    alice_id = cursor.lastrowid
    
    # Insert dummy claim for Alice
    cursor.execute('''
        INSERT INTO claims (user_id, status, claim_amount, description)
        VALUES (?, 'Pending', 1500.0, 'Car accident, front bumper damage')
    ''', (alice_id,))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("Seeding data...")
    seed_data()
    print("Database initialized and seeded successfully!")
