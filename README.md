# CIAOS - CIA's Object Store

## About
CIAOS is a general purpose KV/Object store optimised for machine learning practices. 

## System Offerings that are currently being built. 
1. Storage - Key/Value, Files and Blobs. 
2. Fault Tolerance - Uses Erasure Coding to Optimise Data replication - [Discussion]()
3. User Access Management - Seeks contribution for design. [Discussion](https://github.com/cia-labs/Storage-service/issues/36)
4. Search - Seeks contribution for design. -   [Discussion](https://github.com/cia-labs/Storage-service/issues/35)
5. Availability - Seeks contribution for design. [Discussion]()
6. Client Library and Http Services - Client package is currently available for Python only. Both Client and API end points. - [Discussion]()


## Getting Started

```bash
pip install ciaos
```

### Usage
- API_URL: the url to the fastapi server.
- key: the key value which can be used to identify your content in Database.
- Value: the Base64 encoded binary data that you want to save / upload to database.
- new_key: The new_key is an optional parameter. To be used if and only if you want to update the key.

### SAVE

```
from ciaos import save

save(API_URL, key, value)

```
**Note: A random Key will be generated , if no key is passed to save parameters**

### GET

```
from ciaos import get

get(API_URL, key)
```

### UPDATE

```
from ciaos import update

update(API_URL,key,value,new_key)
```

### DELETE

```
from ciaos import delete

delete(API_URL,key)
```

## Developer's Corner
https://github.com/cia-labs/Storage-service/blob/main/docs.md

