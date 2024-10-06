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
                offset_list BLOB,
                size_list BLOB
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

pub fn upload_sql(key: &str, offset_bytes: &[u8], size_bytes: &[u8]) -> SqliteResult<()> {
    let conn = DB_CONN.lock().unwrap();
    conn.execute(
        "INSERT INTO haystack (key, offset_list, size_list) VALUES (?1, ?2, ?3)",
        params![key, offset_bytes, size_bytes],
    )?;
    Ok(())
}

pub fn get_offset_size_lists(key: &str) -> SqliteResult<(Vec<u8>, Vec<u8>)> {
    let conn = DB_CONN.lock().unwrap();
    let mut stmt = conn.prepare("SELECT offset_list, size_list FROM haystack WHERE key = ?1")?;
    let result = stmt.query_row(params![key], |row| {
        let offset_list: Vec<u8> = row.get(0)?;
        let size_list: Vec<u8> = row.get(1)?;
        Ok((offset_list, size_list))
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

pub fn update_file_db(key: &str, offset_bytes: &[u8], size_bytes: &[u8]) -> Result<(), actix_web::Error> {
    let conn = DB_CONN.lock().unwrap();
    conn.execute(
        "UPDATE haystack SET offset_list = ?1, size_list = ?2 WHERE key = ?3",
        params![offset_bytes, size_bytes, key],
    ).map_err(actix_web::error::ErrorInternalServerError)?;

    Ok(())
}
pub fn append_sql(key: &str, offset_bytes: &[u8], size_bytes: &[u8]) -> Result<(), actix_web::Error> {
    let conn = DB_CONN.lock().unwrap();
    conn.execute(
        "UPDATE haystack SET offset_list = ?1, size_list = ?2 WHERE key = ?3",
        params![offset_bytes, size_bytes, key],
    ).map_err(actix_web::error::ErrorInternalServerError)?;

    Ok(())
}
