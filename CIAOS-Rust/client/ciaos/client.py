# client.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'util'))
import requests
from typing import List
from util.flatbuffer.flatbuffer_handler import create_flatbuffer, parse_flatbuffer


def put(user: str, api_url: str, key: str, data_list: List[bytes]):
    """
    Uploads new files to the server under a unique key.

    Args:
        api_url (str): Base URL of the API.
        key (str): Unique key for the upload.
        data_list (List[bytes]): List of file data in bytes.
        user str will be the user 

    Returns:
        requests.Response or None: The server's response or None if an error occurs.
    """
    try:
        flatbuffer_data = create_flatbuffer(data_list)
        if flatbuffer_data is None:
            print("Failed to create FlatBuffers data.")
            return None

        headers = {
            'User': user
        }
        response = requests.post(f"{api_url}/put/{key}", data=flatbuffer_data, headers=headers)

        if response.status_code == 200:
            print("Upload successful:", response.text)
        else:
            print("Error during upload:", response.text)
        return response
    except requests.RequestException as e:
        print("HTTPError during upload:", e)
        return None

def update_key(user: str,api_url: str, old_key: str, new_key: str):
    """
    Updates the key identifier for existing data.

    Args:
        api_url (str): Base URL of the API.
        old_key (str): The current key.
        new_key (str): The new key to update to.

    Returns:
        str or None: Server response text or None if an error occurs.
    """
    try:
        headers = {'User': user}
        response = requests.put(f"{api_url}/update_key/{old_key}/{new_key}", headers=headers)        
        if response.status_code == 200:
            print("Key update successful:", response.text)
            return response.text
        else:
            print("Error updating key:", response.text)
            return response.text
    except requests.RequestException as e:
        print("HTTPError during key update:", e)
        return None

def update(user: str, api_url: str, key: str, data_list: List[bytes]):
    """
    Updates existing files with new data under the given key.

    Args:
        api_url (str): Base URL of the API.
        key (str): Key identifying the data to update.
        data_list (List[bytes]): New list of file data in bytes.

    Returns:
        requests.Response or None: The server's response or None if an error occurs.
    """
    try:
        flatbuffer_data = create_flatbuffer(data_list)
        if flatbuffer_data is None:
            print("Failed to create FlatBuffers data for update.")
            return None

        headers = {
            'User': user
        }
        response = requests.post(f"{api_url}/update/{key}", data=flatbuffer_data, headers=headers)

        if response.status_code == 200:
            print("Data update successful:", response.text)
        else:
            print("Error during data update:", response.text)
        return response
    except requests.RequestException as e:
        print("HTTPError during data update:", e)
        return None

def append(user: str, api_url: str, key: str, data_list: List[bytes]):
    """
    Appends new files to existing data under the given key.

    Args:
        api_url (str): Base URL of the API.
        key (str): Key identifying the data to append to.
        data_list (List[bytes]): List of file data to append.

    Returns:
        str or None: Server response text or None if an error occurs.
    """
    try:
        flatbuffer_data_append = create_flatbuffer(data_list)
        if flatbuffer_data_append is None:
            print("Failed to create FlatBuffers data for append.")
            return None

        headers = {
            'User': user
        }
        response = requests.post(f"{api_url}/append/{key}", data=flatbuffer_data_append, headers=headers)
        if response.status_code == 200:
            print("Append successful:", response.text)
            return response.text
        else:
            print("Error during append:", response.text)
            return response.text
    except requests.RequestException as e:
        print("HTTPError during append:", e)
        return None

def delete(user: str, api_url: str, key: str):
    """
    Deletes data associated with a key.

    Args:
        api_url (str): Base URL of the API.
        key (str): Key identifying the data to delete.

    Returns:
        str or None: Server response text or None if an error occurs.
    """
    try:
        headers = {'User': user}
        response = requests.delete(f"{api_url}/delete/{key}", headers=headers)
        if response.status_code == 200:
            print("Delete successful:", response.text)
            return response.text
        else:
            print("Error during delete:", response.text)
            return response.text
    except requests.RequestException as e:
        print("HTTPError during delete:", e)
        return None

def get(user: str, api_url: str, key: str):
    """
    Retrieves files associated with a key.

    Args:
        api_url (str): Base URL of the API.
        key (str): Key identifying the data to retrieve.

    Returns:
        List[bytes] or None: List of file data in bytes if successful, else None.
    """
    try:
        headers = {'User': user}
        response = requests.get(f"{api_url}/get/{key}", headers=headers)
        if response.status_code == 200:
            flatbuffer_data = response.content
            # Parse the Flatbuffer and extract files
            file_data_list = parse_flatbuffer(flatbuffer_data)
            print("Retrieve successful")
            return file_data_list
        else:
            print("Error during retrieval:", response.text)
            return None
    except requests.RequestException as e:
        print("HTTPError during retrieval:", e)
        return None

