
from fastapi import FastAPI,Form,  UploadFile, HTTPException #,File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from .crud import create_table, create_image_metadata, get_metadata #update_image_metadata, delete_image_metadata
import os
from fastapi.responses import FileResponse #, HTMLResponse , StreamingResponse
import string
import random
import base64
import uvicorn


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def DatabseRun(API_URL,Port):
    if not API_URL:
        API_URL = "http://127.0.0.1"
    if not Port:
        Port = "8000"
    uvicorn.run(app, host=f"{API_URL}", port=f"{Port}", reload=True)



def generate_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

@app.post("/upload/")
async def update_file(key: str = Form(...), encoded_content: List[str] = Form(...)):
    try:
        if not key:
            key = generate_random_string()
        key_directory = f"{key}"
        directory_key = f"./storage/{key_directory}"
        os.makedirs(directory_key , exist_ok=True)
        for i, encoded_items in enumerate(encoded_content, start=1):
                output_file_path = os.path.join(directory_key, f'encodedtxt{i}.txt')

                with open(output_file_path, 'wb') as output_file:
                    output_file.write(encoded_items.encode())
        create_image_metadata( key, key_directory)
        return JSONResponse(content={"message": "File uploaded successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''@app.post("/upload/")
async def upload_file(files: List[UploadFile], key: Optional[str] = None):
    if not key:
        key = generate_random_string()

    key_directory = f"{key}"
    directory_key = f"./{key_directory}"
    os.makedirs(directory_key , exist_ok=True)
    for file in files:
        file_path = f"{key}/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())

    create_image_metadata( key, key_directory)
    return JSONResponse(content={"message": "File uploaded successfully"})'''

@app.get("/retrieve/{key}")
async def retrieve_file(key: str, metadata_only: Optional[bool] = False):
    path = get_metadata(key)
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Key not found")

    binary_data_list = []

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)

        if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                binary_data = file.read()

                binary_data_list.append(binary_data)


    return binary_data_list
'''
@app.get("/retrieve/{key}")
async def retrieve_file(key: str, metadata_only: Optional[bool] = False):

    path = get_metadata(key)
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Key not found")

    encoded_files = []

    # Iterate through files in the specified path
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)

        # Check if the item is a file
        if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                # Read the file content
                file_content = file.read()

                # Encode the file content using base64
                encoded_data = base64.b64encode(file_content).decode("utf-8")

                # Append the encoded data to the list
                encoded_files.append({
                    "encoded_data": encoded_data
                })

    return encoded_files
'''

#the below is not maintained will return error as huge as the whale that lives down the street
'''
    zip_file_path = f"{key}.zip"
    if os.path.exists(path):
        if metadata_only:
            return {"path": path}
        else:
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        zipf.write(os.path.join(root, file), 
                           os.path.relpath(os.path.join(root, file), 
                           os.path.join(path, '..')))
                        
            with open(zip_file_path, 'rb') as file:
                zip_bytes = file.read()

            os.remove(zip_file_path)


            return StreamingResponse(io.BytesIO(zip_bytes),
                                     media_type="application/zip",
                                     headers={"Content-Disposition": f"attachment; filename={key}.zip"})
    else:
        raise HTTPException(status_code=404, detail="Key not found in the database.")
    
'''
'''

@app.delete("/delete/{db_name}/{key}")
async def delete_file(db_name: str = "", key: str= ""):
    if not db_name:
        db_name = "default"
    db_file = f"{db_name}.db"

    metadata = get_image_metadata(db_file, key)

    if not metadata:
        raise HTTPException(status_code=404, detail="Image not found")

    file_path = metadata[2]
    os.remove(file_path)

    delete_image_metadata(db_name, key)
    return JSONResponse(content={"message": "File deleted successfully"})
'''
