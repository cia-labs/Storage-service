import shutil
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from app.crud.crud import create_connection, check_key_existence, create_image_metadata, get_metadata,delete_metadata
from app.crud.crud import db_file
import os
import string
import random
# import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# db_file = "../server/app/crud/db_name.db"

connection = create_connection(db_file)

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


@app.put("/update/")
async def update_files(key: str, encoded_content: List[str] = Form(...), new_key: Optional[str] = Form(None)):
    path = "./storage/"+get_metadata(key)

    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Key not found")

    if new_key and new_key != key:
        new_path = get_metadata(new_key)

        if not new_path:
            new_key_directory = f"{new_key}"
            os.makedirs(new_key_directory, exist_ok=True)
            create_image_metadata(new_key, new_key_directory)
            new_path = get_metadata(new_key)

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


@app.delete("/delete/{key}")
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
