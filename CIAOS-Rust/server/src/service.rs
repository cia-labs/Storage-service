//service.rs
use actix_web::{ web, HttpResponse,Error };
use futures::StreamExt;
use bytes::BytesMut;
use log::{info, error, warn};
use actix_web::error::ErrorInternalServerError;

use crate::storage::{write_files_to_storage, get_files_from_storage, delete_and_log};
use crate::database::{check_key,append_sql, update_file_db, upload_sql, get_offset_size_lists, delete_from_db, update_key_from_db};
use crate::util::serializer::{serialize_offset_size, deserialize_offset_size};

fn check_key_exists(key: &str) -> Result<(), Error> {
    if !check_key(key).map_err(ErrorInternalServerError)? {
        warn!("Key does not exist: {}", key);
        return Err(actix_web::error::ErrorNotFound(format!("No data found for key: {}, The key does not exist", key)));
    }
    Ok(())
}


pub async fn post_service(key: String, mut payload: web::Payload ) -> Result<HttpResponse, Error>{

    if check_key(&key).map_err(ErrorInternalServerError)? {
        warn!("Key already exists: {}", key);
        return Ok(HttpResponse::BadRequest().body("Key already exists"));
    }

    info!("Starting chunk load");
    let mut bytes = BytesMut::new();
    while let Some(chunk) = payload.next().await {
        let chunk = chunk.map_err(ErrorInternalServerError)?;
        bytes.extend_from_slice(&chunk);
    }

    if bytes.is_empty() {
        error!("No data uploaded with key: {}", key);
        return Ok(HttpResponse::BadRequest().body("No data was uploaded"));
    }

    info!("Total received data size: {} bytes", bytes.len());

    //sends the bytes to storage.rs so that the flatbuffer can deserialise it and write to bin and than return offset and size vec list
    let offset_size_list = write_files_to_storage(&bytes)?;


    if offset_size_list.is_empty()  {
        error!("No data in data list with key: {}", key);
        return Ok(HttpResponse::BadRequest().body("No data in data list"));
    }

    info!("Serializing offset and size and uploading");

    let offset_size_bytes = serialize_offset_size(&offset_size_list)?;

    upload_sql(&key, &offset_size_bytes)
        .map_err(ErrorInternalServerError)?;

    info!("Data uploaded successfully with key: {}", key);
    Ok(HttpResponse::Ok().body(format!("Data uploaded successfully: key = {}", key)))
}

pub async fn get_service(key: String)-> Result<HttpResponse, Error>{

    check_key_exists(&key)?;
    info!("Retrieving data for key: {}", key);

    // Connect to the SQLite database and retrieve offset and size data
    let offset_size_bytes = match get_offset_size_lists(&key) {
        Ok(offset_size_bytes) => offset_size_bytes,
        Err(e) => {
            warn!("Key does not exist or database error: {}", e);
            return Ok(HttpResponse::BadRequest().body("Key does not exist"));
        }
    };

    // Deserialize offset and size data
    let offset_size_list = deserialize_offset_size(&offset_size_bytes)?;

    let data = get_files_from_storage(offset_size_list)?;

    // Return the FlatBuffers serialized data
    Ok(HttpResponse::Ok()
        .content_type("application/octet-stream")
        .body(data))
}

pub async fn append_service(key: String, mut payload: web::Payload ) -> Result<HttpResponse, Error> {
    
    check_key_exists(&key)?;
    info!("Starting chunk load");
    let mut bytes = BytesMut::new();
    while let Some(chunk) = payload.next().await {
        let chunk = chunk.map_err(ErrorInternalServerError)?;
        bytes.extend_from_slice(&chunk);
    }
    if bytes.is_empty() {
        error!("No data uploaded with key: {}", key);
        return Ok(HttpResponse::BadRequest().body("No data was uploaded"));
    }
    
    info!("Total received data size: {} bytes", bytes.len());

    let mut offset_size_list_append = write_files_to_storage(&bytes)?;


    if offset_size_list_append.is_empty() {
        error!("No data in data list with key: {}", key);
        return Ok(HttpResponse::BadRequest().body("No data in data list"));
    }
   
    info!("Serializing offset and size and uploading");

    let offset_size_bytes = match get_offset_size_lists(&key) {
        Ok(offset_size_bytes) => offset_size_bytes,
        Err(e) => {
            warn!("Key does not exist or database error: {}", e);
            return Ok(HttpResponse::BadRequest().body("Key does not exist"));
        }
    };
    
        // Deserialize offset and size data
    let mut offset_size_list = deserialize_offset_size(&offset_size_bytes)?;

    
    offset_size_list.append(&mut offset_size_list_append);  // Appending offset_list_append to offset_list

    let offset_size_bytes_append = serialize_offset_size(&offset_size_list)?;

    append_sql(&key, &offset_size_bytes_append)
            .map_err(ErrorInternalServerError)?;
    
    info!("Data apended successfully with key: {}", key);
    Ok(HttpResponse::Ok().body(format!("Data appended successfully: key = {}", key)))
    
}

pub async  fn delete_service(key: String)-> Result<HttpResponse, Error>{
    
    check_key_exists(&key)?;
    let offset_size_bytes = match get_offset_size_lists(&key) {
        Ok(offset_size_bytes) => offset_size_bytes,
        Err(e) => {
            warn!("Key does not exist or database error: {}", e);
            return Ok(HttpResponse::BadRequest().body("Key does not exist"));
        }
    };
    let offset_size_list = deserialize_offset_size(&offset_size_bytes)?;
    // Deserialize offset and size data
    
    delete_and_log(&key, offset_size_list)?;

    match delete_from_db(&key) {
        Ok(()) => Ok(HttpResponse::Ok().body(format!("File deleted successfully: key = {}", key))),
        Err(e) => Ok(HttpResponse::InternalServerError().body(format!("Failed to delete key: {}", e))),
    }
}

pub async fn update_key_service(old_key: String, new_key: String)->  Result<HttpResponse, Error>{
    
    check_key_exists(&old_key)?;
    // Update the key in the database
    match update_key_from_db(&old_key, &new_key) {
        Ok(()) => Ok(HttpResponse::Ok().body(format!("Key updated successfully from {} to {}", old_key, new_key))),
        Err(e) => Ok(HttpResponse::InternalServerError().body(format!("Failed to update key: {}", e))),
    }
}

pub async  fn update_service(key: String, mut payload: web::Payload ) ->  Result<HttpResponse, Error>{
    
    check_key_exists(&key)?;

    info!("Starting chunk load");
    let mut bytes = BytesMut::new();
    while let Some(chunk) = payload.next().await {
        let chunk = chunk.map_err(ErrorInternalServerError)?;
        bytes.extend_from_slice(&chunk);
    }

    if bytes.is_empty() {
        error!("No data uploaded with key: {}", key);
        return Ok(HttpResponse::BadRequest().body("No data was uploaded"));
    }
    
    info!("Total received data size: {} bytes", bytes.len());
    info!("Starting deserialization");
    
    let offset_size_list = write_files_to_storage(&bytes)?;
   
    if offset_size_list.is_empty()  {
        error!("No data in data list with key: {}", key);
        return Ok(HttpResponse::BadRequest().body("No data in data list"));
    }
    

    let offset_size_bytes = serialize_offset_size(&offset_size_list)?;
    update_file_db(&key, &offset_size_bytes)
    .map_err(ErrorInternalServerError)?;

    info!("Data uploaded successfully with key: {}", key);
    Ok(HttpResponse::Ok().body(format!("Data uploaded successfully: key = {}", key)))


}