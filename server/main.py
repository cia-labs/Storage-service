import shutil
from fastapi import FastAPI, UploadFile, HTTPException, Form, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from server.app.crud.crud import create_image_metadata, get_metadata, delete_metadata
import os
import string
import random
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE = 'db_name.db'


def connect_db():
    return sqlite3.connect(DATABASE)

@app.put("/update/{key}")
async def update_files(key: str, updated_files: List[UploadFile] = File(...), new_key: Optional[str] = Form(None)):
    path = get_metadata(key)

    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Key not found")

    if new_key and new_key != key:
        new_path = get_metadata(new_key)

        if not new_path:
            new_key_directory = f"{new_key}"
            os.makedirs(new_key_directory, exist_ok=True)
            create_image_metadata(new_key, new_key_directory)
            new_path = get_metadata(new_key)

        for filename in os.listdir(path):
            source_file_path = os.path.join(path, filename)
            destination_file_path = os.path.join(new_path, filename)
            shutil.copy2(source_file_path, destination_file_path)

        for updated_file in updated_files:
            filename = updated_file.filename
            file_path = os.path.join(new_path, filename)

            with open(file_path, "wb") as f:
                f.write(updated_file.file.read())
        
        return JSONResponse(content={"message": "Files updated successfully"})

    if path or os.path.exists(path):
        for updated_file in updated_files:
            filename = updated_file.filename
            file_path = os.path.join(path, filename)

            with open(file_path, "wb") as f:
                f.write(updated_file.file.read())

        return JSONResponse(content={"message": "Files updated successfully"})