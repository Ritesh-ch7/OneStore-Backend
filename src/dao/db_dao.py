import sqlite3
from datetime import datetime

DB_PATH = "file_downloads.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create table if it does not exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS downloads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT NOT NULL UNIQUE,  -- Add UNIQUE constraint to prevent duplicates
        count INTEGER DEFAULT 0, 
        upload_date TEXT,  -- Ensure this column is defined
        file_size INTEGER,  -- Ensure file_size is defined
        uploads INTEGER DEFAULT 0
    )
    ''')

    conn.commit()
    conn.close()

def add_file_metadata(file_name, file_size):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO downloads (file_name, count, upload_date, file_size, uploads)
        VALUES (?, 0, ?, ?, 1)  -- Start uploads count at 1
        ON CONFLICT(file_name) DO UPDATE SET uploads = uploads + 1
    ''', (file_name, datetime.now().isoformat(), file_size))
    conn.commit()
    conn.close()

def increment_download_count(file_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE downloads
        SET count = count + 1
        WHERE file_name = ?
    ''', (file_name,))
    conn.commit()
    conn.close()

def get_download_counts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Get the total download count as a single value
    cursor.execute("SELECT SUM(count) FROM downloads")
    total_downloads = cursor.fetchone()[0] or 0  # Fetch the result, default to 0 if None
    conn.close()
    return total_downloads


def get_upload_counts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(uploads) FROM downloads")
    total_uploads = cursor.fetchone()[0] or 0  # Handle case where there are no uploads
    conn.close()
    return total_uploads

def get_all_file_metadata():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT file_name, upload_date, file_size FROM downloads")
    results = cursor.fetchall()
    conn.close()
    return [{"name": file_name, "upload_time": upload_date, "size": file_size} for file_name, upload_date, file_size in results]

def get_all_file_metadata_with_counts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT file_name, upload_date, file_size, count FROM downloads")
    results = cursor.fetchall()
    conn.close()
    return [{"name": file_name, "upload_time": upload_date, "size": file_size, "count": count} for file_name, upload_date, file_size, count in results]


# Initialize the database
init_db()
