use actix_web::{HttpServer, App, post, web, HttpResponse,Error };
use futures::StreamExt;
use bytes::BytesMut;

use log::{info, error, warn};
use bincode;
use actix_web::error::ErrorInternalServerError;

// storage.rs contains functionality related to writing files to storage and getting offset and size
//as well as dealing with file retrieval from storage and deletion
mod storage;
use crate::storage::{write_files_to_storage, get_files_from_storage, delete_and_log};


//keys and offset:size lists are managed here 
mod database;
use crate::database::{check_key,append_sql, update_file_db, upload_sql, get_offset_size_lists, delete_from_db, update_key_from_db};


//offset and size of files are converted to binary to be stored in blob format in sql i.e deserialization and serialization fucntions 
fn serialize_offset_size(offset_list: &Vec<u64>, size_list: &Vec<u64>) -> Result<(Vec<u8>, Vec<u8>), actix_web::Error> {
    let offset_bytes = bincode::serialize(&offset_list)
        .map_err(|e| actix_web::error::ErrorInternalServerError(format!("Failed to serialize offset list: {}", e)))?;
    let size_bytes = bincode::serialize(&size_list)
        .map_err(|e| actix_web::error::ErrorInternalServerError(format!("Failed to serialize size list: {}", e)))?;
    
    Ok((offset_bytes, size_bytes))
}
fn deserialize_offset_size(offset_bytes: &[u8], size_bytes: &[u8]) -> Result<(Vec<u64>, Vec<u64>), Error> {
    let offset_list: Vec<u64> = bincode::deserialize(offset_bytes)
        .map_err(|e| ErrorInternalServerError(format!("Failed to deserialize offset list: {}", e)))?;
    let size_list: Vec<u64> = bincode::deserialize(size_bytes)
        .map_err(|e| ErrorInternalServerError(format!("Failed to deserialize size list: {}", e)))?;
    
    Ok((offset_list, size_list))
}

//upload endpoint accepting a key string and payload 
#[actix_web::post("/upload/{key}")]
async fn upload_files(
    key: web::Path<String>,
    mut payload: web::Payload,
) -> Result<HttpResponse, Error> {
    let key = key.into_inner();
    info!("Uploading data with key: {}", key);

    if check_key(&key).map_err(actix_web::error::ErrorInternalServerError)? {
        warn!("Key already exists: {}", key);
        return Ok(HttpResponse::BadRequest().body("Key already exists"));
    }
    
    info!("Starting chunk load");
    let mut bytes = BytesMut::new();
    while let Some(chunk) = payload.next().await {
        let chunk = chunk.map_err(actix_web::error::ErrorInternalServerError)?;
        bytes.extend_from_slice(&chunk);
    }

    if bytes.is_empty() {
        error!("No data uploaded with key: {}", key);
        return Ok(HttpResponse::BadRequest().body("No data was uploaded"));
    }
    
    info!("Total received data size: {} bytes", bytes.len());
    
    //sends the bytes to storage.rs so that the flatbuffer can deserialise it and write to bin and than return offset and size vec list
    let (offset_list, size_list) = storage::write_files_to_storage(&bytes)?;


    if offset_list.is_empty() || size_list.is_empty() {
        error!("No data in data list with key: {}", key);
        return Ok(HttpResponse::BadRequest().body("No data in data list"));
    }
    
    info!(
        "Data written to file. Offset list size: {}, Size list size: {}",
        offset_list.len(),
        size_list.len()
    );
    info!("Serializing offset and size and uploading");

    let (offset_bytes, size_bytes) = serialize_offset_size(&offset_list, &size_list)?;
    
    upload_sql(&key, &offset_bytes, &size_bytes)
        .map_err(actix_web::error::ErrorInternalServerError)?;

    info!("Data uploaded successfully with key: {}", key);
    Ok(HttpResponse::Ok().body(format!("Data uploaded successfully: key = {}", key)))
}


#[actix_web::get("/get/{key}")]
async fn retrieve_data(key: web::Path<String>) -> Result<HttpResponse, Error> {
    let key = key.into_inner();
    if !check_key(&key).map_err(actix_web::error::ErrorInternalServerError)? {
        warn!("Key does not exist: {}", key);
        return Ok(HttpResponse::NotFound().body(format!("No data found for key: {}", key)));
    }
    info!("Retrieving data for key: {}", key);

    // Connect to the SQLite database and retrieve offset and size data
    let (offset_bytes, size_bytes) = match get_offset_size_lists(&key) {
        Ok((offset_bytes, size_bytes)) => (offset_bytes, size_bytes),
        Err(e) => {
            warn!("Key does not exist or database error: {}", e);
            return Ok(HttpResponse::BadRequest().body("Key does not exist"));
        }
    };

    // Deserialize offset and size data
    let (offset_list, size_list) = deserialize_offset_size(&offset_bytes, &size_bytes)?;

    let data = get_files_from_storage(offset_list, size_list)?;

    // Return the FlatBuffers serialized data
    Ok(HttpResponse::Ok()
        .content_type("application/octet-stream")
        .body(data))
}

#[actix_web::post("/append/{key}")]
async fn append_files(
    key: web::Path<String>,
    mut payload: web::Payload,
) -> Result<HttpResponse, Error> {
    let key = key.into_inner();
    info!("appending data with key: {}", key);
    if !check_key(&key).map_err(actix_web::error::ErrorInternalServerError)? {
        warn!("Key does not exist: {}", key);
        return Ok(HttpResponse::NotFound().body(format!("No data found for key: {}", key)));
    }
    info!("Starting chunk load");
    let mut bytes = BytesMut::new();
    while let Some(chunk) = payload.next().await {
        let chunk = chunk.map_err(actix_web::error::ErrorInternalServerError)?;
        bytes.extend_from_slice(&chunk);
    }
    if bytes.is_empty() {
        error!("No data uploaded with key: {}", key);
        return Ok(HttpResponse::BadRequest().body("No data was uploaded"));
    }
    
    info!("Total received data size: {} bytes", bytes.len());

    let (mut offset_list_append,mut  size_list_append) = storage::write_files_to_storage(&bytes)?;


    if offset_list_append.is_empty() || size_list_append.is_empty() {
        error!("No data in data list with key: {}", key);
        return Ok(HttpResponse::BadRequest().body("No data in data list"));
    }
   
    info!("Serializing offset and size and uploading");

    let (offset_bytes, size_bytes) = match get_offset_size_lists(&key) {
            Ok((offset_bytes, size_bytes)) => (offset_bytes, size_bytes),
            Err(e) => {
                warn!("Key does not exist or database error: {}", e);
                return Ok(HttpResponse::BadRequest().body("Key does not exist"));
            }
        };
    
        // Deserialize offset and size data
        let (mut offset_list,mut size_list) = deserialize_offset_size(&offset_bytes, &size_bytes)?;

    
    offset_list.append(&mut offset_list_append);  // Appending offset_list_append to offset_list
    size_list.append(&mut size_list_append);      // Appending size_list_append to size_list

    let (offset_bytes_append , size_bytes_append) = serialize_offset_size(&offset_list, &size_list)?;

    append_sql(&key, &offset_bytes_append, &size_bytes_append)
            .map_err(actix_web::error::ErrorInternalServerError)?;
    
    info!("Data apended successfully with key: {}", key);
    Ok(HttpResponse::Ok().body(format!("Data appended successfully: key = {}", key)))
    
}

#[actix_web::delete("/delete/{key}")]
async fn delete_file(key: web::Path<String>) -> Result<HttpResponse, Error> {
    let key = key.into_inner();
    if !check_key(&key).map_err(actix_web::error::ErrorInternalServerError)? {
        return Ok(HttpResponse::NotFound().body("Key not found"));
    }
    let (offset_bytes, size_bytes) = match get_offset_size_lists(&key) {
        Ok((offset_bytes, size_bytes)) => (offset_bytes, size_bytes),
        Err(e) => {
            warn!("Key does not exist or database error: {}", e);
            return Ok(HttpResponse::BadRequest().body("Key does not exist"));
        }
    };
    let (offset_list,size_list) = deserialize_offset_size(&offset_bytes, &size_bytes)?;
    // Deserialize offset and size data
    
    delete_and_log(&key, offset_list, size_list)?;

    match delete_from_db(&key) {
        Ok(()) => Ok(HttpResponse::Ok().body(format!("File deleted successfully: key = {}", key))),
        Err(e) => Ok(HttpResponse::InternalServerError().body(format!("Failed to delete key: {}", e))),
    }
}

#[actix_web::put("/update/{old_key}/{new_key}")]
async fn update_key(
    path: web::Path<(String, String)>
) -> Result<HttpResponse, Error> {
    let (old_key, new_key) = path.into_inner();
    
    // Check if the old key exists
    if !check_key(&old_key).map_err(actix_web::error::ErrorInternalServerError)? {
        return Ok(HttpResponse::NotFound().body(format!("Key not found: {}", old_key)));
    }

    // Update the key in the database
    match update_key_from_db(&old_key, &new_key) {
        Ok(()) => Ok(HttpResponse::Ok().body(format!("Key updated successfully from {} to {}", old_key, new_key))),
        Err(e) => Ok(HttpResponse::InternalServerError().body(format!("Failed to update key: {}", e))),
    }
}

#[actix_web::post("/update_data/{key}")]
async fn update_files(
    key: web::Path<String>,
    mut payload: web::Payload,
) -> Result<HttpResponse, Error> {
    let key = key.into_inner();
    info!("Uploading data with key: {}", key);
    if !check_key(&key).map_err(actix_web::error::ErrorInternalServerError)? {
        return Ok(HttpResponse::NotFound().body(format!("Key not found: {}", key)));
    }

    info!("Starting chunk load");
    let mut bytes = BytesMut::new();
    while let Some(chunk) = payload.next().await {
        let chunk = chunk.map_err(actix_web::error::ErrorInternalServerError)?;
        bytes.extend_from_slice(&chunk);
    }

    if bytes.is_empty() {
        error!("No data uploaded with key: {}", key);
        return Ok(HttpResponse::BadRequest().body("No data was uploaded"));
    }
    
    info!("Total received data size: {} bytes", bytes.len());
    info!("Starting deserialization");
    
    let (offset_list, size_list) = storage::write_files_to_storage(&bytes)?;
    if offset_list.is_empty() || size_list.is_empty() {
        error!("No data in data list with key: {}", key);
        return Ok(HttpResponse::BadRequest().body("No data in data list"));
    }
    
    info!(
        "Data written to file. Offset list size: {}, Size list size: {}",
        offset_list.len(),
        size_list.len()
    );
    info!("Serializing offset and size and uploading");

    let (offset_bytes, size_bytes) = serialize_offset_size(&offset_list, &size_list)?;
    update_file_db(&key, &offset_bytes, &size_bytes)
    .map_err(actix_web::error::ErrorInternalServerError)?;

    info!("Data uploaded successfully with key: {}", key);
    Ok(HttpResponse::Ok().body(format!("Data uploaded successfully: key = {}", key)))

}


#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Initialize logging, server setup, etc.
    env_logger::init();
    
    info!("Starting server on 127.0.0.1:8080");
    
    HttpServer::new(|| {
        App::new()
            .wrap(actix_web::middleware::Logger::default())
            .service(upload_files) // Register the upload route
            .service(retrieve_data) // Register the retrieve route (this was missing)
            .service(append_files)
            .service(delete_file)
            .service(update_key)
            .service(update_files)
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}