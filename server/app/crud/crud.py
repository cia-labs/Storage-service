import sqlite3
from fastapi import HTTPException
import os

db_file = "../server/app/crud/db_name.db"

if os.getenv("DB_FILE"):
    db_file = os.getenv("DB_FILE")

def create_connection(db_file):
    connection = sqlite3.connect(db_file)
    return connection

def create_table(db_file):
    connection = create_connection(db_file)
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS store (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL,
        key_directory TEXT NOT NULL
    )
    """)
    connection.commit()
    connection.close()

#To avoid creation of multiple database
create_table(db_file)

def create_image_metadata( key, key_directory):
    connection = create_connection(db_file)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT EXISTS (SELECT 1 FROM store WHERE key = ? LIMIT 1)
    """, (key,))
    key_exists = cursor.fetchone()[0]

    if key_exists:
        connection.close()
        return {"status": "success", "message":"File uploaded successfully"}

    cursor.execute("""
    INSERT INTO store (key, key_directory) VALUES (?, ?)
    """, (key, key_directory))
    connection.commit()
    connection.close()

def get_metadata(key):

    try:
        connection = create_connection(db_file)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT key_directory FROM store WHERE key = ?
        """, (key,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching metadata: {str(e)}")
    finally:
        connection.close()

def delete_metadata(key):
    connection= create_connection(db_file)
    cursor= connection.cursor()
    cursor.execute("""
    Delete from store where key=? 
                   """,(key,))
    connection.commit()
    cursor.close()

def check_key_existence(key):
        connection = create_connection(db_file)
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM store WHERE key=?", (key,))
        result = cursor.fetchone()
        connection.close()
        if result is None:
            return False
        else:
            return True


def get_latest_generated_key():
    try:
        connection = create_connection(db_file)
        cursor = connection.cursor()
        cursor.execute("SELECT key FROM store ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching latest key: {str(e)}")
    finally:
        connection.close()
