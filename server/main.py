import shutil
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from app.crud.crud import check_key_existence,create_connection,create_image_metadata, get_metadata, delete_metadata,db_file
import os
import string
import random
from fastapi import HTTPException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connection=create_connection(db_file)

def generate_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

@app.post("/upload/")
async def upload(key: Optional[str] = Form(None), encoded_content: List[str] = Form(...)):
    try:
        if not key:
            key = generate_random_string()
        if not encoded_content:
            raise HTTPException(status_code=422, detail="Field 'encoded_content' cannot be empty")
        key_directory = f"{key}"
        directory_key = f"./storage/{key_directory}"
        os.makedirs(directory_key , exist_ok=True)
        existing_files_count = len([name for name in os.listdir(directory_key) if name.startswith("encodedtxt")])
        for i, encoded_item in enumerate(encoded_content, start=existing_files_count + 1):
                output_file_path = os.path.join(directory_key, f'encodedtxt{i}.txt')

                with open(output_file_path, 'wb') as output_file:
                    output_file.write(encoded_item.encode())
        create_image_metadata( key, key_directory)
        return JSONResponse(content={"message": "File uploaded successfully","key": key})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get/{key}")
async def retrieve_file(key: str, metadata_only: Optional[bool] = False):
    try:
        if not check_key_existence(key):
            raise HTTPException(status_code=404, detail="Key not found")

        filepath = get_metadata(key)
        path = f"./storage/{filepath}"

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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   

@app.put("/update/")
async def update_files(key: str, encoded_content: List[str] = Form(...), new_key: Optional[str] = Form(None)):
    filepath = get_metadata(key)

    if filepath is None:
        raise HTTPException(status_code=404, detail="Key not found")

    path = f"./storage/{filepath}"

    if new_key and new_key != key:
 
        new_key_directory = f"./storage/{new_key}"
        os.makedirs(new_key_directory, exist_ok=True)
        create_image_metadata(new_key, new_key_directory)
        path="./storage/"+get_metadata(key)
        #TO-DO : Add the prefix or suffix to the folder name 
        new_path = new_key_directory

        for filename in os.listdir(path):
            source_file_path = os.path.join(path, filename)
            destination_file_path = os.path.join(new_path, filename)
            shutil.copy2(source_file_path, destination_file_path)

        existing_files = [f for f in os.listdir(new_path) if f.startswith("encodedtxt")]
        if existing_files:
            max_existing_index = max(int(f.split("encodedtxt")[1].split(".")[0]) for f in existing_files)
        else:
            max_existing_index = 0

        for i, encoded_items in enumerate(encoded_content, start=max_existing_index+1):
            output_file_path = os.path.join(new_path, f'encodedtxt{i}.txt')

            with open(output_file_path, 'wb') as output_file:
                output_file.write(encoded_items.encode())
        
        return JSONResponse(content={"message": "Files updated successfully"})

    if path or os.path.exists(path):
        existing_files = [f for f in os.listdir(path) if f.startswith("encodedtxt")]
        if existing_files:
            max_existing_index = max(int(f.split("encodedtxt")[1].split(".")[0]) for f in existing_files)
        else:
            max_existing_index = 0

        for i, encoded_items in enumerate(encoded_content, start=max_existing_index+1):
            output_file_path = os.path.join(path, f'encodedtxt{i}.txt')

            with open(output_file_path, 'wb') as output_file:
                output_file.write(encoded_items.encode())

        return JSONResponse(content={"message": "Files updated successfully"})

@app.delete("/delete/")
async def delete_files(key: str):
    folder_path = f"./storage/{key}"

    try:
        shutil.rmtree(folder_path)
        delete_metadata(key)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Folder not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting folder: {str(e)}")

    return {"message": f"Folder '{key}' and its contents deleted successfully"}