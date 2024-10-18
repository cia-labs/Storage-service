use actix_web::{HttpServer, App};

use log::info;

/*storage.rs contains functionality related to writing files to storage and getting offset and size
as well as dealing with file retrieval from storage and deletion */ 
mod storage;
//keys and offset:size lists are managed here 
mod database;
//offset and size of files are converted to binary to be stored in blob format in sql i.e deserialization and serialization fucntions 
mod util;

mod api;
use crate::api::{upload,retrieve,append,delete,update_key,update};

mod service;
use log4rs;


#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Initialize logging, server setup, etc.
    log4rs::init_file("server_log.yaml", Default::default()).unwrap();
    info!("Starting server on 127.0.0.1:8080");
    
    HttpServer::new(|| {
        App::new()
            .wrap(actix_web::middleware::Logger::default())
            .service(upload) 
            .service(retrieve) 
            .service(append)
            .service(delete)
            .service(update_key)
            .service(update)
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}