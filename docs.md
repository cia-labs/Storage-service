# Developer's Guide

## Local Setup.
**Here's a step to step guide to bring up the storage server in your local.** 

### Prerequisites

- Python 3.10 or higher installed on your machine
- pip package manager

### Clone the Repository

```bash
git clone https://github.com/cia-labs/Storage-service.git
cd Storage-service/server
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

---
---

# Deploying the Storage Service as a Docker Container

To deploy the storage service as a container, follow these steps:

## **Create a Dockerfile:**

Create a file named Dockerfile in the root directory of your project and add the following content:
```docker
# Use the latest version of Alpine as the base image
FROM alpine:latest

# Set the working directory inside the container
WORKDIR /code

# Copy all files from directory to /code
COPY . /code

# Install Python and pip in the Alpine image
RUN apk --no-cache add python3 py3-pip

# Set up a virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Expose port 8000
EXPOSE 8000

# Upgrade pip and install the required packages
RUN pip install --upgrade pip && pip install -r requirements.txt  

# Specify the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000","--reload"]

```
 **Now Build the Docker Image and deploy the container**

you can access the Swagger UI over the container ip address at port 8000

- Note: If you want to change the exposed port, modify the EXPOSE and CMD directives in the Dockerfile. Update the EXPOSE line with the desired port, and adjust the --port option in the CMD line accordingly.

```docker
# Change the exposed port to 8080
EXPOSE 8080


