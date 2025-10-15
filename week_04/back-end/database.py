import sqlite3
import os

# Database configuration
DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'library.db')

def init_db():
    print(f"Initializing database at: {DATABASE}")
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Drop existing tables to ensure a clean slate for schema updates
    cursor.execute('DROP TABLE IF EXISTS books')
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('DROP TABLE IF EXISTS borrows')

    # Create books table
    cursor.execute('''
        CREATE TABLE books (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT
        )
    ''')
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    ''')
    
    # Create borrows table
    cursor.execute('''
        CREATE TABLE borrows (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            book_id INTEGER,
            borrow_date TEXT,
            return_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def add_sample_data():
    print(f"Adding sample data to database at: {DATABASE}")
    """Add sample data to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Add sample books
    cursor.execute('''INSERT INTO books (id, title, author) VALUES (?, ?, ?)''', (1, 'The Lord of the Rings', 'J.R.R. Tolkien'))
    cursor.execute('''INSERT INTO books (id, title, author) VALUES (?, ?, ?)''', (2, 'Pride and Prejudice', 'Jane Austen'))
    cursor.execute('''INSERT INTO books (id, title, author) VALUES (?, ?, ?)''', (3, '1984', 'George Orwell'))

    # Add sample users
    cursor.execute('''INSERT INTO users (id, name, email) VALUES (?, ?, ?)''', (1, 'Alice Smith', 'alice@example.com'))
    cursor.execute('''INSERT INTO users (id, name, email) VALUES (?, ?, ?)''', (2, 'Bob Johnson', 'bob@example.com'))

    # Add sample borrows
    cursor.execute('''INSERT INTO borrows (id, user_id, book_id, borrow_date, return_date) VALUES (?, ?, ?, ?, ?)''', (1, 1, 1, '2023-01-01', '2023-01-15'))
    cursor.execute('''INSERT INTO borrows (id, user_id, book_id, borrow_date, return_date) VALUES (?, ?, ?, ?, ?)''', (2, 2, 3, '2023-02-10', None))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    add_sample_data()
    print("Database initialized and populated with sample data successfully.")