# CIAOS - CIA's Object Store

##System Offerings that are currently being built. 
1. Fault Tolerance - Uses Erasure Coding to Optimise Data replication - Currently being built by [@Tejus_CJ]([https://github.com/username](https://github.com/Tejas-ChandraShekarRaju)).
2. Search - Seeks contribution for design.
3. Availability - Seeks contribution for design. 

HLD - High Level Design
https://drive.google.com/file/d/1BWJzX_X4IUtnwxcTL0QxThmeq6kVCHHz/view?usp=drive_link

Client SDK

### Installation

```bash
pip install ciaos
```

## Usage

### SAVE

```
from ciaos import save

save(API_URL, key, value)
```

- API_URL: the url to the fastapi server
- key: the key value which can be used to identify your content in Database
- Value: the Base64 encoded binary data that you want to save / upload to database

---

## Note: A random Key will be generated , if no key is passed to save parameters

### GET

```
from ciaos import get

get(API_URL, key)
```

- API_URL: the url to the fastapi server
- key: the key value which can be used to identify and fetch the data from Database

### UPDATE

```
from ciaos import update

update(API_URL,key,value,new_key)
```

- NOTE: The new_key is an optional parameter. To be used if and only if you want to update the key.

### DELETE

```
from ciaos import delete

delete(API_URL,key)
```

### Server

```
API SPECIFICATION

POST /upload/: Upload files to the server.
GET /retrieve/{key}: Retrieve files from the server.
PUT /update/: Update files on the server.
DELETE /delete/: Delete files from the server

```
