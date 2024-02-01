# Storage-Service

Multi node, General purpose Kv store/ Value store.

HLD - High Level Design
https://drive.google.com/file/d/1BWJzX_X4IUtnwxcTL0QxThmeq6kVCHHz/view?usp=drive_link

## S1_Client

Client interface for the storage service

### Installation

```bash
pip install s1_client
```

### Usage

```
from s1_client import crud

print(crud.post())
```

### Server

```
Usage
Endpoints

POST /upload/: Upload files to the server.
GET /retrieve/{key}: Retrieve files from the server.
PUT /update/: Update files on the server.
DELETE /delete/: Delete files from the server

Sample Usage

import requests
API_URL = "http://api-url"
key = "my_key"
encoded_content = ["base64_encoded_string_of_your_file"]

response = requests.post(f"{API_URL}/upload/", data={"key": key, "encoded_content": encoded_content})
response = requests.get(f"{API_URL}/retrieve/{key}")
response = requests.put(f"{API_URL}/update/?key={key}&new_key={new_key}", data={"encoded_content": encoded_content})
response = requests.delete(f"{API_URL}/delete/?key={key}")

print(response.json())

```
