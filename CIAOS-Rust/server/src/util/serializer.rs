use bincode;
use actix_web::error::ErrorInternalServerError;
use actix_web::Error;


pub fn serialize_offset_size(offset_list: &Vec<u64>, size_list: &Vec<u64>) -> Result<(Vec<u8>, Vec<u8>), actix_web::Error> {
    let offset_bytes = bincode::serialize(&offset_list)
        .map_err(|e| actix_web::error::ErrorInternalServerError(format!("Failed to serialize offset list: {}", e)))?;
    let size_bytes = bincode::serialize(&size_list)
        .map_err(|e| actix_web::error::ErrorInternalServerError(format!("Failed to serialize size list: {}", e)))?;
    
    Ok((offset_bytes, size_bytes))
}
pub fn deserialize_offset_size(offset_bytes: &[u8], size_bytes: &[u8]) -> Result<(Vec<u64>, Vec<u64>), Error> {
    let offset_list: Vec<u64> = bincode::deserialize(offset_bytes)
        .map_err(|e| ErrorInternalServerError(format!("Failed to deserialize offset list: {}", e)))?;
    let size_list: Vec<u64> = bincode::deserialize(size_bytes)
        .map_err(|e| ErrorInternalServerError(format!("Failed to deserialize size list: {}", e)))?;
    
    Ok((offset_list, size_list))
}