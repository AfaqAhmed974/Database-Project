import sqlite3

def create_connection(db_name):
    try:
        conn = sqlite3.connect(db_name)
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraint
        print(f"[INFO] Connected to database '{db_name}' successfully.")
        return conn
    except sqlite3.Error as e:
        print(f"[ERROR] Database connection failed: {e}")
        return None

def create_tables(conn):
    cursor = conn.cursor()

    table_queries = {
        'users': '''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone_number TEXT,
                email TEXT UNIQUE
            )
        ''',
        'specializations': '''
            CREATE TABLE IF NOT EXISTS specializations (
                specialization_id INTEGER PRIMARY KEY AUTOINCREMENT,
                specialization_name TEXT UNIQUE NOT NULL
            )
        ''',
        'doctors': '''
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                specialization_id INTEGER,
                FOREIGN KEY (specialization_id) REFERENCES specializations(specialization_id) ON DELETE SET NULL
            )
        ''',
        'pharmacies': '''
            CREATE TABLE IF NOT EXISTS pharmacies (
                pharmacy_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone_number TEXT,
                location TEXT
            )
        ''',
        'appointments': '''
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                doctor_id INTEGER,
                appointment_date DATE,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
            )
        ''',
        'prescriptions': '''
            CREATE TABLE IF NOT EXISTS prescriptions (
                prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                doctor_id INTEGER,
                pharmacy_id INTEGER,
                prescription_date DATE,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
                FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(pharmacy_id) ON DELETE CASCADE
            )
        '''
    }

    for name, query in table_queries.items():
        cursor.execute(query)
        print(f"[INFO] Table '{name}' created or already exists.")

    conn.commit()
    print("[INFO] All tables created successfully.")

def insert_initial_data(conn):
    cursor = conn.cursor()

    # Insert specializations
    specializations = [
        ('Cardiology',),
        ('Dermatology',),
        ('Neurology',),
        ('Pediatrics',),
        ('Orthopedics',),
        ('Oncology',),
        ('Psychiatry',),
        ('Gastroenterology',),
        ('Endocrinology',),
        ('Ophthalmology',)
    ]
    cursor.executemany('INSERT OR IGNORE INTO specializations (specialization_name) VALUES (?)', specializations)
    print("[INFO] Inserted specializations.")

    # Insert users
    users = [
        ('Ali', '0300-1234567', 'ali786@gmail.com'),
        ('Iqra', '0312-6543210', 'iqra2025@gmail.com'),
        ('Sania', '0321-1122334', 'sania999@gmail.com'),
        ('Qomal', '0333-9988776', 'qomal11@gmail.com'),
        ('Huzaifa', '0345-5566778', 'huzaifa456@gmail.com'),
        ('Safiullah', '0301-4455667', 'safiullah007@gmail.com')
    ]
    cursor.executemany('INSERT OR IGNORE INTO users (name, phone_number, email) VALUES (?, ?, ?)', users)
    print("[INFO] Inserted users.")

    # Insert doctors (10 doctors with emails and specialization)
    doctors = [
        ('Dr. Ahsan', 'ahsan.cardiology@example.com', 'Cardiology'),
        ('Dr. Maria', 'maria.dermatology@example.com', 'Dermatology'),
        ('Dr. Shahid', 'shahid.neuro@example.com', 'Neurology'),
        ('Dr. Sara', 'sara.pediatrics@example.com', 'Pediatrics'),
        ('Dr. Kamran', 'kamran.ortho@example.com', 'Orthopedics'),
        ('Dr. Zoya', 'zoya.oncology@example.com', 'Oncology'),
        ('Dr. Asif', 'asif.psychiatry@example.com', 'Psychiatry'),
        ('Dr. Rabia', 'rabia.gastro@example.com', 'Gastroenterology'),
        ('Dr. Bilal', 'bilal.endo@example.com', 'Endocrinology'),
        ('Dr. Usman', 'usman.eye@example.com', 'Ophthalmology')
    ]
    for name, email, specialization_name in doctors:
        cursor.execute('''
            INSERT INTO doctors (name, email, specialization_id)
            SELECT ?, ?, specialization_id FROM specializations WHERE specialization_name = ?
        ''', (name, email, specialization_name))
    print("[INFO] Inserted doctors.")

    # Insert pharmacies
    pharmacies = [
        ('United Pharmacy', '042-9876543', 'Mansehra'),
        ('MediPlus Pharmacy', '042-8765432', 'Islamabad'),
        ('Rehmat Pharmacy', '0992-4455667', 'Abbottabad')
    ]
    cursor.executemany('INSERT OR IGNORE INTO pharmacies (name, phone_number, location) VALUES (?, ?, ?)', pharmacies)
    print("[INFO] Inserted pharmacies.")

    # Insert appointments
    appointments = [
        (1, 1, '2025-04-10'),
        (2, 2, '2025-04-11'),
        (3, 3, '2025-04-12'),
        (4, 4, '2025-04-13'),
        (5, 5, '2025-04-14')
    ]
    cursor.executemany('INSERT OR IGNORE INTO appointments (user_id, doctor_id, appointment_date) VALUES (?, ?, ?)', appointments)
    print("[INFO] Inserted appointments.")

    # Insert prescriptions
    prescriptions = [
        (1, 1, 1, '2025-04-10'),
        (2, 2, 2, '2025-04-11'),
        (3, 3, 3, '2025-04-12'),
        (4, 4, 1, '2025-04-13'),
        (5, 5, 2, '2025-04-14')
    ]
    cursor.executemany('INSERT OR IGNORE INTO prescriptions (user_id, doctor_id, pharmacy_id, prescription_date) VALUES (?, ?, ?, ?)', prescriptions)
    print("[INFO] Inserted prescriptions.")

    conn.commit()
    print("[INFO] All initial data inserted successfully.")

def main():
    database_name = 'healthcare.db'
    conn = create_connection(database_name)

    if conn:
        create_tables(conn)
        insert_initial_data(conn)
        conn.close()
        print(f"[SUCCESS] Database '{database_name}' setup completed.")
    else:
        print("[ERROR] Database setup failed.")

if __name__ == "__main__":
    main()
