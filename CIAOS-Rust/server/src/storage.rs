// storage.rs

use std::fs::{OpenOptions, File};
use std::io::{self, Read, Write, Seek, SeekFrom};
use actix_web::Error;
use log::{error, info};
use flatbuffers::{root, FlatBufferBuilder};
use actix_web::error::{ErrorInternalServerError, ErrorBadRequest};
use serde_json::json;

//mod util;
use crate::util::Flatbuffer_Store_generated::store::{FileDataList, FileData, FileDataListArgs, FileDataArgs};



const HAYSTACK_FILE: &str = "CIA_storage.bin";

//OpenFile provides operation functionalities over the .bin file
struct OpenFile {
    file: File,
}



impl OpenFile {
    //the actual function dealing with file 
    fn new() -> io::Result<Self> {
        let file = OpenOptions::new()
            .create(true)
            .read(true)
            .write(true)
            .open(HAYSTACK_FILE)?;
        Ok(Self { file })
    }
    //wirte inputs the data tobe written to file and returns offset and size of teh data
    fn write(&mut self, data: &[u8]) -> io::Result<(u64, u64)> {
        let offset = self.file.seek(SeekFrom::End(0))?;
        self.file.write_all(data)?;
        Ok((offset, data.len() as u64))
    }
    //read accepts the offset adn size of data that needs to be read and returns the data in binary 
    fn read(&mut self, offset: u64, size: u64) -> io::Result<Vec<u8>> {
        self.file.seek(SeekFrom::Start(offset))?;
        let mut buffer = vec![0u8; size as usize];
        self.file.read_exact(&mut buffer)?;
        Ok(buffer)
    }
}


// this function accepts the flatbuffer and returns the offset and size list after proess the files in it
pub fn write_files_to_storage(body: &[u8])
    -> Result<(Vec<u64>, Vec<u64>), Error> {
    // Open the storage file "haystack.bin" in append mode
    let mut haystack = OpenFile::new()?;

    let mut offset_list: Vec<u64> = Vec::new();
    let mut size_list: Vec<u64> = Vec::new();

    //deserialises the binary data thats been accepted into FileDataList object using flatbuffer
    
    let file_data_list = match root::<FileDataList>(&body) {
        Ok(data) => data,
        Err(e) => return Err(ErrorBadRequest(format!("Failed to parse FlatBuffers data: {:?}", e))),
    };
    let files = match file_data_list.files() {
        Some(files) => files,
        None => return Err(ErrorBadRequest("No files found in FlatBuffers data")),
    };
    info!("Deserialized {} files", files.len());

    for (index, file_data) in files.iter().enumerate() {
        let data = match file_data.data() {
            Some(data) => data,
            None => {
                error!("No data in file at index {}", index);
                continue;
            }
        };

        match haystack.write(data.bytes()) {
            Ok((offset, size)) => {
                offset_list.push(offset);
                size_list.push(size);
                info!("Written file {} at offset {} with size {}", index, offset, size);
            }
            Err(e) => {
                error!("Failed to write file {} to haystack: {}", index, e);
                return Err(ErrorInternalServerError(e));
            }
        }
    }

    Ok((offset_list, size_list))
}


pub fn get_files_from_storage(offset_list: Vec<u64>, size_list: Vec<u64>)-> Result<Vec<u8>, Error> {
    info!("connecting to .bin and gettting files");
    let mut haystack = OpenFile::new().map_err(ErrorInternalServerError)?;
    info!("connected to .bin");
    let mut builder = FlatBufferBuilder::new();
    let mut file_data_vec = Vec::new();
    info!("building the flatbuffer to share");
    for (&offset, &size) in offset_list.iter().zip(size_list.iter()) {
        let data = haystack.read(offset, size).map_err(ErrorInternalServerError)?;
        let data_vector = builder.create_vector(&data);
        let file_data = FileData::create(&mut builder, &FileDataArgs { data: Some(data_vector) });
        file_data_vec.push(file_data);
    }
    info!("successfully built the buffer");
    let files = builder.create_vector(&file_data_vec);
    let file_data_list = FileDataList::create(&mut builder, &FileDataListArgs { files: Some(files) });
    builder.finish(file_data_list, None);
    info!("sending buffer");
    Ok(builder.finished_data().to_vec())
    }

////////////////////////////////////////
/// here starts delete functionality ///
////////////////////////////////////////
const DELETE_FILE: &str = "delete_log.json";

struct DeleteFile {
        file: File,
    }
    
impl DeleteFile {
    fn new() -> Result<Self, Error> {
            let file = OpenOptions::new()
                .create(true)
                .append(true)
                .open(DELETE_FILE)
                .map_err(ErrorInternalServerError)?;
            Ok(Self { file })
    }
    
    fn delete(&mut self, key: &str, offset_list: &[u64], size_list: &[u64]) -> Result<(), Error> {
            let log_entry = json!({
                key: {
                    "offset": offset_list,
                    "size": size_list
                }
            });
            
            self.file.seek(SeekFrom::End(0))
                .map_err(ErrorInternalServerError)?;
            writeln!(self.file, "{}", log_entry.to_string())
                .map_err(ErrorInternalServerError)?;
            
            Ok(())
    }
}
    
pub fn delete_and_log(key: &str, offset_list: Vec<u64>, size_list: Vec<u64>) -> Result<(), Error> {
        let mut delete_file = DeleteFile::new()?;
        delete_file.delete(key, &offset_list, &size_list)?;
    
        info!("Deleted and logged data for key: {}", key);
        Ok(())
}
