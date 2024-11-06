use bincode;
use actix_web::error::ErrorInternalServerError;
use actix_web::Error;


pub fn serialize_offset_size(offset_size_list: &Vec<(u64, u64)>) -> Result<Vec<u8>, actix_web::Error> {
    bincode::serialize(&offset_size_list)
        .map_err(|e| actix_web::error::ErrorInternalServerError(format!("Failed to serialize size list: {}", e)))
    
}

pub fn deserialize_offset_size(bytes: &[u8]) -> Result<Vec<(u64, u64)>, Error> {
    bincode::deserialize(bytes)
        .map_err(|e| ErrorInternalServerError(format!("Failed to deserialize offset list: {}", e)))
}