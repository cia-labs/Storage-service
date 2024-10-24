//database.rs
use std::sync::Mutex;
use rusqlite::{params, Connection, Result as SqliteResult};
use std::sync::Arc;
use log::warn;
use actix_web::Error;
use lazy_static::lazy_static;

lazy_static! {
    static ref DB_CONN: Arc<Mutex<Connection>> = {
        let conn = Connection::open("metadata.sqlite").expect("Failed to open the database");
        conn.execute(
            "CREATE TABLE IF NOT EXISTS haystack (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                key TEXT NOT NULL,
                offset_size_list BLOB,
                UNIQUE(user, key)
            )",
            [],
        )
        .expect("Failed to create table");
        Arc::new(Mutex::new(conn))
    };
}

pub struct Database {
    user: String
}

impl Database {
    pub fn new(user: &str) -> Result<Self, actix_web::Error> {
        Ok(Database {
            user: user.to_string()
        })
    }

    pub fn check_key(&self, key: &str) -> SqliteResult<bool> {
        let conn = DB_CONN.lock().unwrap();
        let mut stmt = conn.prepare("SELECT COUNT(*) FROM haystack WHERE user = ?1 AND key = ?2")?;
        let count: i64 = stmt.query_row(params![self.user, key], |row| row.get(0))?;
        Ok(count > 0)
    }

    pub fn check_key_nonexistance(&self, key: &str) -> Result<(), Error> {
        if !self.check_key(key).map_err(actix_web::error::ErrorInternalServerError)? {
            warn!("Key does not exist: {}", key);
            return Err(actix_web::error::ErrorNotFound(format!("No data found for key: {}, The key does not exist", key)));
        }
        Ok(())
    }

    pub fn upload_sql(&self, key: &str, offset_size_bytes: &[u8]) -> SqliteResult<()> {
        let conn = DB_CONN.lock().unwrap();
        conn.execute(
            "INSERT INTO haystack (user, key, offset_size_list) VALUES (?1, ?2, ?3)",
            params![self.user, key, offset_size_bytes],
        )?;
        Ok(())
    }

    pub fn get_offset_size_lists(&self, key: &str) -> SqliteResult<Vec<u8>> {
        let conn = DB_CONN.lock().unwrap();
        let mut stmt = conn.prepare("SELECT offset_size_list FROM haystack WHERE user = ?1 AND key = ?2")?;
        let result = stmt.query_row(params![self.user, key], |row| {
            let offset_size_list: Vec<u8> = row.get(0)?;
            Ok(offset_size_list)
        });
        result
    }

    pub fn delete_from_db(&self, key: &str) -> Result<(), actix_web::Error> {
        let conn = DB_CONN.lock().unwrap();
        conn.execute(
            "DELETE FROM haystack WHERE user = ?1 AND key = ?2",
            params![self.user, key],
        ).map_err(actix_web::error::ErrorInternalServerError)?;
        Ok(())
    }

    pub fn update_key_from_db(&self, old_key: &str, new_key: &str) -> Result<(), actix_web::Error> {
        let conn = DB_CONN.lock().unwrap();
        conn.execute(
            "UPDATE haystack SET key = ?1 WHERE user = ?2 AND key = ?3",
            params![new_key, self.user, old_key],
        ).map_err(actix_web::error::ErrorInternalServerError)?;
        Ok(())
    }

    pub fn update_file_db(&self, key: &str, offset_size_bytes: &[u8]) -> Result<(), actix_web::Error> {
        let conn = DB_CONN.lock().unwrap();
        conn.execute(
            "UPDATE haystack SET offset_size_list = ?1 WHERE user = ?2 AND key = ?3",
            params![offset_size_bytes, self.user, key],
        ).map_err(actix_web::error::ErrorInternalServerError)?;
        Ok(())
    }

    pub fn append_sql(&self, key: &str, offset_size_bytes: &[u8]) -> Result<(), actix_web::Error> {
        let conn = DB_CONN.lock().unwrap();
        conn.execute(
            "UPDATE haystack SET offset_size_list = ?1 WHERE user = ?2 AND key = ?3",
            params![offset_size_bytes, self.user, key],
        ).map_err(actix_web::error::ErrorInternalServerError)?;
        Ok(())
    }
}