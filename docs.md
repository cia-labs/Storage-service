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
## **Build the Docker Image:**

In the terminal, navigate to the directory containing the Dockerfile and run the following command to build the Docker image. Replace your_image_name:tag with a name and tag for your image.

```bash
docker build -t your_image_name:tag .
 ```

## **Upload the Docker Image to Docker Hub:**

If you haven't done so already, create an account on Docker Hub. After creating an account, log in to Docker Hub in the terminal using the following command:
    
```bash
docker login
```

Tag the built image with your Docker Hub username and the desired repository name:
```bash
docker tag your_image_name:tag your_dockerhub_username/repository_name:tag
```
Push the image to Docker Hub:

```bash
docker push your_dockerhub_username/repository_name:tag
```
## **Pull and Deploy the Docker Image:**

On the machine where you want to deploy the storage service, ensure that Docker is installed. Pull the Docker image from Docker Hub:

```bash
docker pull your_dockerhub_username/repository_name:tag
```
Run the container from the pulled image:
```
docker run -p host_port:container_port your_dockerhub_username/repository_name:tag
```

Replace host_port with the port on your host machine where you want to expose the service, and container_port with the port specified in the Dockerfile (in this case, 8000).

Now, the storage service should be running inside the Docker container. Access it through the specified host port on your machine.

Note: If you want to change the exposed port, modify the EXPOSE and CMD directives in the Dockerfile. Update the EXPOSE line with the desired port, and adjust the --port option in the CMD line accordingly.

```docker
    # Change the exposed port to 8080
EXPOSE 8080

    # Change the CMD line to use port 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080","--reload"]
```



