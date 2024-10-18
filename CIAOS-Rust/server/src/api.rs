//api.rs
use actix_web::{post, web, HttpResponse,Error };
use log::info;

use crate::service::{get_service, post_service, append_service , delete_service, update_key_service,update_service};
//upload endpoint accepting a key string and payload 

#[actix_web::post("/post/{key}")]
async fn upload(
    key: web::Path<String>,
    payload: web::Payload,
) -> Result<HttpResponse, Error> {
    info!("Uploading data with key: {}", key);
    post_service(key.into_inner(), payload).await
}

#[actix_web::get("/get/{key}")]
async fn retrieve(key: web::Path<String>) -> Result<HttpResponse, Error> {
    info!("checking key and retrieving : {}", key);
    get_service(key.into_inner()).await
}


#[actix_web::post("/append/{key}")]
async fn append(
    key: web::Path<String>,
    payload: web::Payload,
) -> Result<HttpResponse, Error> {
    info!("appending data with key: {}", key);
    append_service(key.into_inner(), payload).await
}

#[actix_web::delete("/delete/{key}")]
async fn delete(key: web::Path<String>) -> Result<HttpResponse, Error> {
    info!("deleting data with key: {}", key);
    delete_service(key.into_inner()).await
}


#[actix_web::put("/update/{old_key}/{new_key}")]
async fn update_key(
    path: web::Path<(String, String)>
) -> Result<HttpResponse, Error> {
    let (old_key, new_key) = path.into_inner();
    info!("updating old key with key: {}", new_key);
    update_key_service(old_key, new_key).await
}


#[actix_web::post("/update_data/{key}")]
async fn update(
    key: web::Path<String>,
    payload: web::Payload,
) -> Result<HttpResponse, Error> {
    info!("Uploading data with key: {}", key);
    update_service(key.into_inner(), payload).await
}