# Developer's Guide

## Local Setup.
**Here's a step to step guide to bring up the storage server in your local.** 

### Prerequisites

- Python 3.10 or higher installed on your machine
- pip package manager

### Clone the Repository

```bash
git clone https://github.com/cia-labs/Storage-service.git
cd Storage-service
```
### Install Dependencies

```bash
pip install -r requirements.txt
```

### Running the application

```bash
uvicorn main:app --reload
```
### Accessing Api's and testing the functionality. 

Once the app is successfully installed, access http://127.0.0.1:8000/docs, You'll see a screen similar to the below screen shot
<img width="1617" alt="image" src="https://github.com/cia-labs/Storage-service/assets/41864599/e8774034-5a50-4e82-9e4b-c3e84c47bdf9">





