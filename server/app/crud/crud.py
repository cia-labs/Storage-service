import sqlite3
from fastapi import HTTPException

db_file = "db_name.db"

def create_connection(db_file):
    connection = sqlite3.connect(db_file)
    return connection

def create_table(db_file):
    connection = create_connection(db_file)
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL,
        key_directory TEXT NOT NULL
    )
    """)
    connection.commit()
    connection.close()


def create_image_metadata( key, key_directory):
    connection = create_connection(db_file)
    cursor = connection.cursor()
    create_table(db_file)

    cursor.execute("""
    SELECT EXISTS (SELECT 1 FROM images WHERE key = ? LIMIT 1)
    """, (key,))
    key_exists = cursor.fetchone()[0]

    if key_exists:
        connection.close()
        return {"status": "success", "message":"File uploaded successfully"}

    cursor.execute("""
    INSERT INTO images (key, key_directory) VALUES (?, ?)
    """, (key, key_directory))
    connection.commit()
    connection.close()

def get_metadata(key):

    try:
        connection = create_connection(db_file)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT key_directory FROM images WHERE key = ?
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
    Delete from images where key=? 
                   """,(key,))
    connection.commit()
    cursor.close()