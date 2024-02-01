# Storage-Service
Multi node, General purpose Kv store/ Value store. 

HLD - High Level Design
https://drive.google.com/file/d/1BWJzX_X4IUtnwxcTL0QxThmeq6kVCHHz/view?usp=drive_link


## S1_Client

Client interface for the storage service

### Installation

```bash
pip install ciaos
```

## Usage 

### To save any file to the database i.e upload 
```
from ciaos import save

save(API_URL, key, value)
```
The Parameters 
- API_URL being the URL to the fastapi server running database
- key being the identity which u want to assign to the content you are uploading
- value being the list of encoded data you are saving

### To retrieve/get files from the database
```
from ciaos import retreieve
retreieve(API_URL, key)

```
The Paramets :
- API_URL being the URL to the fastapi server running database
- key being the identity which u had  assign to the content, that you want to Get

