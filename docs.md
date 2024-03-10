# Document for Developers
___
### Libraries used:
``` fastapi ``` The framework used

``` uvicorn ``` For hosting fastapi server

**Other dependencies** :

```
python-multiparts
httpx
pytest
pydantic
```
---

## Getting Started with Main.py from Server :

```
uvicorn main:app --reload
```

The above command line spins up a Fastapi server on you localhost , The API has four main functionalities:

---
---

## **Upload** 
- to uplaod any content to the storage service

#### To comunicate through the url where the api is hosted, in order to interact with add ```/upload``` path over URL

 **What Kind of input do the above api calls expect:**

**UPLOAD** / ```/upload```: 

- Expect a Base64  encoded byte data, which needs to be uploaded in a List, the List can have n Number of Base64 encoded strings which can represent any file etc.

- A key can also be passed which can be used to perform delete, update, get operation on uploaded content, the key is optional as the Storage service auto generates a new key for you if a key is not pasased.

- - The API returns a successful message on upload with the key name

---

## **Get** 
- to retrieve the content which you have uploaded to storage service

#### To comunicat through the url where the api is hosted, in order to interact with add ```/get``` path over URL

- Pass the key paramter of the contents which you want to retrieve from the storage service 

- - The Get will return a Base64 Byte string data of List which contains all the content appended in a List , which is tagged with the key pair which you passed



## **Delete** 
- to delete the content which was uploaded, given that you have the key of the uploaded content
#### To comunicat through the url where the api is hosted, in order to interact with add ```/delete``` path over URL

- Just like **GET** vene delete needs a key to delete the content from storage service


## **Update** 
- to update the content with the new content given that a key is passed , (Note: you can also generate a new key if you would like)
#### To comunicat through the url where the api is hosted, in order to interact with add add ```/update``` path over URL

- A key is passed with the new encoded base64 content which is needs to be updated with for the given key, you can also give a new key so that a new copy of the content which belongs to the key is created and also append it with the new value which is passed

---
---

## Description For the main and crud files in Server:

## Crud.py:

The crud.py module handles database operations related to storing metadata about uploaded content. It includes functions to create a database connection, create a table, and perform operations like creating metadata, retrieving metadata, deleting metadata, and checking key existence.

- The `create_image_metadata` function inserts a new record into the 'store' table with the provided 'key' and 'key_directory'.  
  It first checks if the key already exists using a SELECT EXISTS query.  
  If the key exists, it returns a success message without inserting a new record.  
  If the key does not exist, it inserts a new record and returns a success message.

- The `get_metadata` function retrieves the 'key_directory' associated with the given 'key' from the 'store' table.  
  It includes error handling using a try-except block to raise an HTTPException with a 500 status code in case of an error.  
  If the record exists, it returns the 'key_directory'; otherwise, it returns None.

- The `delete_metadata` function deletes a record from the 'store' table based on the provided 'key'.  
  It executes a DELETE query and commits the changes to the database.

- The `check_key_existence` function checks if a record with the provided 'key' exists.  
  It executes a SELECT query and returns True if the record exists, and False otherwise.  
  The database connection is closed before returning the result.


   

### Main.py

**The upload function:**

- expects two parameters: key (an optional string) and encoded_content (a list of strings). The key parameter is optional and can be provided in the request. If not provided, a random string is generated.
- If encoded_content is empty, it raises an HTTPException with a **422** status code and the detail message "Field 'encoded_content' cannot be empty."

- It creates a directory path based on the provided or generated key inside the "./storage/" directory. It iterates over the provided encoded_content list, creating a file path for each item. The content of each item is then written to a corresponding file with a name like "encodedtxt1.txt," "encodedtxt2.txt," etc.
- If the file upload process is successful, it returns a JSON response with a success message and the key used for the uploaded files. If any exception occurs during the file upload process, it raises an HTTPException with a 500 status code and the details of the exception converted to a string.

**The GET function**:

- It expects a key parameter in the URL path. It checks whether the provided key exists by calling the `check_key_existence` function. If the key does not exist, it raises an HTTPException with a 404 status code and the detail message "Key not found."

- It retrieves the file path associated with the key by calling the `get_metadata` function. The file path is then constructed using the "./storage/" directory. It checks whether the constructed path exists. If the path does not exist or is empty, it raises an HTTPException with a 404 status code and the detail message "Key not found." 

- It iterates over the files in the specified path, reads each file in binary mode, and appends the binary data to a list (binary_data_list). If the file retrieval process is successful, it returns a list containing the binary data of each file. If any exception occurs during the file retrieval process, it raises an HTTPException with a 500 status code and the details of the exception converted to a string.

**The Update Function**:

- Defines a PUT endpoint at the "/update/" URL path. It expects three parameters: key (string), encoded_content (a list of strings), and an optional new_key parameter.

- It retrieves the file path associated with the provided key by calling the `get_metadata` function. If the key does not exist (i.e., the file path is None), it raises an HTTPException with a 404 status code and the detail message "Key not found." It constructs the path based on the retrieved file path.

- If a new key is provided and it is different from the original key, it creates a new directory based on the new key and updates the metadata using the `create_image_metadata` function. It also copies the existing files from the old path to the new path using `shutil.copy2`. It checks for existing files in the new path with names starting with "encodedtxt." If existing files are found, it calculates the maximum index to use for naming the new files. If no existing files are found, it sets the maximum index to 0.

- It iterates over the provided encoded_content list, writing each item to a new file in the new path with names like "encodedtxt1.txt," "encodedtxt2.txt," etc. If the file update process is successful, it returns a JSON response with a success message. If any exception occurs during the file update process, it raises an HTTPException with a 500 status code and the details of the exception converted to a string.

**The Delete Function**

- Defines a DELETE endpoint at the "/delete/" URL path. It expects a key parameter in the request. It checks the path of the folder to be deleted based on the provided key.

- It attempts to delete the folder and its contents using `shutil.rmtree`, and also delete the content related to it from the database. If the folder is not found (raises `FileNotFoundError`), it raises an HTTPException with a 404 status code and the detail message "Folder not found." If any other exception occurs, it raises an HTTPException with a 500 status code and the details of the exception converted to a string. If the folder deletion process is successful, it returns a JSON response with a success message.

- The error is dumped respectively if there is an error deleting.

## Testing the Deployed Storage Service

To ensure that the deployed storage service functions as expected, you can run the provided tests using pytest. The tests are located in the "tests" directory within the "server" directory and are defined in the "test.py" file. Before running the tests, make sure that the storage service server is running.

### Steps to Run Tests:

1. **Navigate to the Tests Directory:**
   Open a terminal and change your current working directory to the "tests" directory within the "server" directory. Use the following command:

   ```bash
   cd path/to/your/server/tests
    ```
2. **Run Tests:**
    Execute the pytest command to run the tests. The tests will interact with the deployed storage service, making requests to various endpoints and asserting expected behavior.
    ```bash
    pytest test.py
    ```
3. **Review Test Results:**
    After the tests complete, review the output in the terminal. pytest will provide information about passed and failed tests, along with any error messages.

    Ensure that all tests pass without errors. If any tests fail, review the error messages to identify the issues.

---
---

## Deploying the Storage Service as a Container

To deploy the storage service as a container, follow these steps:

1. **Create a Dockerfile:**
    Create a file named Dockerfile in the root directory of your project and add the following content:
    ```docker
    # Use the latest version of Alpine as the base image
    FROM alpine:latest

    # Set the working directory inside the container
    WORKDIR /code

    # Copy the requirements file to the working directory
    COPY ./requirements.txt .

    # Copy the application files to the working directory
    COPY ./crud.py /code/
    COPY ./main.py /code/

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
2. **Build the Docker Image:**

    In the terminal, navigate to the directory containing the Dockerfile and run the following command to build the Docker image. Replace your_image_name:tag with a name and tag for your image.

    ```bash
    docker build -t your_image_name:tag .
     ```
3. **Upload the Docker Image to Docker Hub:**

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
4. **Pull and Deploy the Docker Image:**

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
    










