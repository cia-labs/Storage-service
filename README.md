# CIAOS - CIA's Object Store

## System Offerings that are currently being built. 
1. Fault Tolerance - Uses Erasure Coding to Optimise Data replication - Currently being built by [@Tejus_CJ](https://github.com/Tejas-ChandraShekarRaju).
2. User Access Management - Seeks contribution for design. 
3. Search - Seeks contribution for design.
4. Availability - Seeks contribution for design.
5. Client Library and Http Services - Client package is currently available for Python only. Both Client and API end points are built by [@Siddiq](https://github.com/noobed-max) and [@Ashish](https://github.com/Ashish9738).

HLD - High Level Design
https://drive.google.com/file/d/1BWJzX_X4IUtnwxcTL0QxThmeq6kVCHHz/view?usp=drive_link

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

