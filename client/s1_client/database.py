
from fastapi import FastAPI,Form,  UploadFile, HTTPException #,File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from crud import create_connection, check_key_existence, create_image_metadata, get_metadata #update_image_metadata, delete_image_metadata
import os
from fastapi.responses import FileResponse #, HTMLResponse , StreamingResponse
import string
import random

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




def generate_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

@app.post("/upload/")
async def update_file(key: str = Form(...), encoded_content: List[str] = Form(...)):
    try:
        if check_key_existence(key):
            raise HTTPException(status_code=400, detail="Key already exists")
        if not key:
            key = generate_random_string()
        key_directory = f"{key}"
        ########################################################################
        #u can change the below path to the path where files need to be saved .#
        ########################################################################
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
