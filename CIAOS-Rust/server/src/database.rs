//database.rs

use std::sync::Mutex;
use rusqlite::{params, Connection, Result as SqliteResult};
use lazy_static::lazy_static;

lazy_static! {
    static ref DB_CONN: Mutex<Connection> = {
        let conn = Connection::open("haystack.sqlite").expect("Failed to open the database");
        conn.execute(
            "CREATE TABLE IF NOT EXISTS haystack (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                offset_size_list BLOB
            )",
            [],
        )
        .expect("Failed to create table");
        Mutex::new(conn)
    };
}

pub fn check_key(key: &str) -> SqliteResult<bool> {
    let conn = DB_CONN.lock().unwrap();
    let mut stmt = conn.prepare("SELECT COUNT(*) FROM haystack WHERE key = ?1")?;
    let count: i64 = stmt.query_row(params![key], |row| row.get(0))?;
    Ok(count > 0)
}

pub fn upload_sql(key: &str, offset_size_bytes: &[u8]) -> SqliteResult<()> {
    let conn = DB_CONN.lock().unwrap();
    conn.execute(
        "INSERT INTO haystack (key, offset_size_list) VALUES (?1, ?2)",
        params![key, offset_size_bytes],
    )?;
    Ok(())
}

pub fn get_offset_size_lists(key: &str) -> SqliteResult<Vec<u8>> {
    let conn = DB_CONN.lock().unwrap();
    let mut stmt = conn.prepare("SELECT offset_size_list FROM haystack WHERE key = ?1")?;
    let result = stmt.query_row(params![key], |row| {
        let offset_size_list: Vec<u8> = row.get(0)?;
        Ok(offset_size_list)
    });
    result
}

// Function to delete a key from the database
pub fn delete_from_db(key: &str) -> Result<(), actix_web::Error> {
    let conn = DB_CONN.lock().unwrap();
    conn.execute(
        "DELETE FROM haystack WHERE key = ?1",
        params![key],
    ).map_err(actix_web::error::ErrorInternalServerError)?;

    Ok(())
}

pub fn update_key_from_db(old_key: &str, new_key: &str) -> Result<(), actix_web::Error> {
    let conn = DB_CONN.lock().unwrap();
    conn.execute(
        "UPDATE haystack SET key = ?1 WHERE key = ?2",
        params![new_key, old_key],
    ).map_err(actix_web::error::ErrorInternalServerError)?;

    Ok(())
}

pub fn update_file_db(key: &str, offset_size_bytes: &[u8]) -> Result<(), actix_web::Error> {
    let conn = DB_CONN.lock().unwrap();
    conn.execute(
        "UPDATE haystack SET offset_size_list = ?1 WHERE key = ?2",
        params![offset_size_bytes, key],
    ).map_err(actix_web::error::ErrorInternalServerError)?;

    Ok(())
}
pub fn append_sql(key: &str, offset_size_bytes: &[u8]) -> Result<(), actix_web::Error> {
    let conn = DB_CONN.lock().unwrap();
    conn.execute(
        "UPDATE haystack SET offset_size_list = ?1 WHERE key = ?2",
        params![offset_size_bytes, key],
    ).map_err(actix_web::error::ErrorInternalServerError)?;

    Ok(())
}
