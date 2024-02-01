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

```
