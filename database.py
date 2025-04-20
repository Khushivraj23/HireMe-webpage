import sqlite3

def init_db():
    conn = sqlite3.connect('db/hireme.db')
    cursor = conn.cursor()

    # Create students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            usn TEXT PRIMARY KEY NOT NULL,
            student_name TEXT NOT NULL,
            contact_number TEXT NOT NULL,
            college_name TEXT NOT NULL,
            branch TEXT NOT NULL,
            skills TEXT,
            email_id TEXT NOT NULL,
            password TEXT NOT NULL
        );
    ''')

    # Create recruiters table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recruiters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            company TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            email_id TEXT NOT NULL
        );
    ''')

    # Create jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_role TEXT NOT NULL,
            company TEXT NOT NULL,
            package TEXT NOT NULL,
            job_description TEXT NOT NULL
        );
    ''')

    # Create student_applications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usn TEXT NOT NULL,
            job_id INTEGER NOT NULL,
            status TEXT DEFAULT 'applied',
            FOREIGN KEY (usn) REFERENCES students(usn),
            FOREIGN KEY (job_id) REFERENCES jobs(id),
            UNIQUE(usn, job_id)
        );
    ''')

    conn.commit()
    conn.close()
