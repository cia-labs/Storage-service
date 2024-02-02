# Storage-Service
Multi node, General purpose Kv store/ Value store. 

HLD - High Level Design
https://drive.google.com/file/d/1BWJzX_X4IUtnwxcTL0QxThmeq6kVCHHz/view?usp=drive_link


## CIAOS

Client interface for the storage service

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
Note: A random Key can be generated , if no key is passed to save parameters 
---
### GET
```
from ciaos import get

get(API_URL, key)
```
- API_URL: the url to the fastapi server
- key: the key value which can be used to identify and fetch the data from Database

### Update
```
from ciaos import update

update(API_URL,key,value,new_key):
```


### Delete
```
from ciaos import delete

delete(API_URL,key)
```