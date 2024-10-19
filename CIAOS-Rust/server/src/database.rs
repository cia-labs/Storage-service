//database.rs

use std::sync::Mutex;
use rusqlite::{params, Connection, Result as SqliteResult};
use std::sync::Arc;
use log::warn;
use actix_web::Error;


pub struct Database {
    db_conn: Arc<Mutex<Connection>>,
}

impl Database {

    pub fn new(user: &str) -> Result<Self, actix_web::Error> {
            let conn = Connection::open(format!("{}.sqlite", user)).expect("Failed to open the database");
            conn.execute(
                "CREATE TABLE IF NOT EXISTS metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL,
                    offset_size_list BLOB
                )",
                [],
            )
            .map_err(actix_web::error::ErrorInternalServerError)?;
            Ok(Database {
            db_conn: Arc::new(Mutex::new(conn)),
            })
    }

    pub fn check_key(&self,key: &str) -> SqliteResult<bool> {
        let conn = self.db_conn.lock().unwrap();
        let mut stmt = conn.prepare("SELECT COUNT(*) FROM metadata WHERE key = ?1")?;
        let count: i64 = stmt.query_row(params![key], |row| row.get(0))?;
        Ok(count > 0)
    }

    pub fn check_key_nonexistance(&self ,key: &str) -> Result<(), Error> {
        if !self.check_key(key).map_err(actix_web::error::ErrorInternalServerError)? {
            warn!("Key does not exist: {}", key);
            return Err(actix_web::error::ErrorNotFound(format!("No data found for key: {}, The key does not exist", key)));
        }
        Ok(())
    }

    pub fn upload_sql(&self,key: &str, offset_size_bytes: &[u8]) -> SqliteResult<()> {
        let conn = self.db_conn.lock().unwrap();
        conn.execute(
            "INSERT INTO metadata (key, offset_size_list) VALUES (?1, ?2)",
            params![key, offset_size_bytes],
        )?;
        Ok(())
    }

    pub fn get_offset_size_lists(&self,key: &str) -> SqliteResult<Vec<u8>> {
        let conn = self.db_conn.lock().unwrap();
        let mut stmt = conn.prepare("SELECT offset_size_list FROM metadata WHERE key = ?1")?;
        let result = stmt.query_row(params![key], |row| {
            let offset_size_list: Vec<u8> = row.get(0)?;
            Ok(offset_size_list)
        });
        result
    }

    // Function to delete a key from the database
    pub fn delete_from_db(&self,key: &str) -> Result<(), actix_web::Error> {
        let conn = self.db_conn.lock().unwrap();
        conn.execute(
            "DELETE FROM metadata WHERE key = ?1",
            params![key],
        ).map_err(actix_web::error::ErrorInternalServerError)?;

        Ok(())
    }

    pub fn update_key_from_db(&self,old_key: &str, new_key: &str) -> Result<(), actix_web::Error> {
        let conn = self.db_conn.lock().unwrap();
        conn.execute(
            "UPDATE metadata SET key = ?1 WHERE key = ?2",
            params![new_key, old_key],
        ).map_err(actix_web::error::ErrorInternalServerError)?;

        Ok(())
    }

    pub fn update_file_db(&self,key: &str, offset_size_bytes: &[u8]) -> Result<(), actix_web::Error> {
        let conn = self.db_conn.lock().unwrap();
        conn.execute(
            "UPDATE metadata SET offset_size_list = ?1 WHERE key = ?2",
            params![offset_size_bytes, key],
        ).map_err(actix_web::error::ErrorInternalServerError)?;

        Ok(())
    }
    pub fn append_sql(&self,key: &str, offset_size_bytes: &[u8]) -> Result<(), actix_web::Error> {
        let conn = self.db_conn.lock().unwrap();
        conn.execute(
            "UPDATE metadata SET offset_size_list = ?1 WHERE key = ?2",
            params![offset_size_bytes, key],
        ).map_err(actix_web::error::ErrorInternalServerError)?;

        Ok(())
    }
}