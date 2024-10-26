import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'util'))
import requests
from typing import List
from util.flatbuffer.flatbuffer_handler import create_flatbuffer, parse_flatbuffer
import config
from typing import List, Optional

class Ciaos:
    def __init__(self):
        """
        Initialize Ciaos client with configuration parameters.
        API URL and user ID are imported from config

        config.API_URL = "<server url>"
        config.user.id = "your_user_id"
        """

        # Get user ID from config
        try:
            self.user_id = config.user_id
            if not self.user_id:
                raise ValueError("User ID must be set in config.user.id")
        except AttributeError:
            raise ValueError("config.user.id must be defined")

        self.headers = {
            "User": self.user_id,
        }

    def put(self, key: Optional[str] = None, file_path: Optional[str] = None):
        """
        Uploads files to the server with flexible input options.

        Args:
            key (Optional[str]): Unique key for the upload. If None and file_path provided, 
                            uses filename as key.
            file_path (Optional[str]): Path to file to upload. If provided, reads file data.
            data_list (Optional[List[bytes]]): List of file data in bytes. Used if file_path 
                                            not provided.

        Returns:
            requests.Response or None: The server's response or None if an error occurs.
        """
        try:
            # Handle file path only case
            if file_path:
                try:
                    with open(file_path, 'rb') as file:
                        file_data = file.read()
                        data_list = [file_data]
                    
                    # If key not provided, use filename from path
                    if key is None:
                        key = os.path.basename(file_path)
                except IOError as e:
                    print(f"Error reading file {file_path}: {e}")
                    return None
            
            # Validate required parameters when file_path is not given
            if key is None:
                print("Error: key is required when file_path is not provided")
                return None
            
            if data_list is None:
                print("Error: file in file_path is empty")
                return None

            # Create and send flatbuffer data
            flatbuffer_data = create_flatbuffer(data_list)
            if flatbuffer_data is None:
                print("Failed to create FlatBuffers data.")
                return None

            response = requests.post(
                f"{config.api_url}/put/{key}", 
                data=flatbuffer_data, 
                headers=self.headers
            )

            if response.status_code == 200:
                print("Upload successful:", response.text)
            else:
                print("Error during upload:", response.text)
            return response

        except requests.RequestException as e:
            print("HTTPError during upload:", e)
            return None
    
    def put_binary(self, key: str, data_list: List[bytes]):
        try:
            flatbuffer_data = create_flatbuffer(data_list)
            if flatbuffer_data is None:
                print("Failed to create FlatBuffers data.")
                return None


            response = requests.post(
                f"{API_URL}/put/{key}", 
                data=flatbuffer_data, 
                headers=self.headers
            )

            if response.status_code == 200:
                print("Upload successful:", response.text)
            else:
                print("Error during upload:", response.text)
            return response
        except requests.RequestException as e:
            print("HTTPError during upload:", e)
            return None

    def update_key(self, old_key: str, new_key: str):
        """
        Updates the key identifier for existing data.

        Args:
            old_key (str): The current key.
            new_key (str): The new key to update to.

        Returns:
            str or None: Server response text or None if an error occurs.
        """
        try:
            response = requests.put(
                f"{config.api_url}/update_key/{old_key}/{new_key}", 
                headers=self.headers
            )
            if response.status_code == 200:
                print("Key update successful:", response.text)
            else:
                print("Error updating key:", response.text)
            return response.text
        except requests.RequestException as e:
            print("HTTPError during key update:", e)
            return None

    def update(self, key: str, data_list: List[bytes]):
        """
        Updates existing files with new data under the given key.

        Args:
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

            response = requests.post(
                f"{config.api_url}/update/{key}", 
                data=flatbuffer_data, 
                headers=self.headers
            )

            if response.status_code == 200:
                print("Data update successful:", response.text)
            else:
                print("Error during data update:", response.text)
            return response
        except requests.RequestException as e:
            print("HTTPError during data update:", e)
            return None

    def append(self, key: str, data_list: List[bytes]):
        """
        Appends new files to existing data under the given key.

        Args:
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

            response = requests.post(
                f"{config.api_url}/append/{key}", 
                data=flatbuffer_data_append, 
                headers=self.headers
            )
            if response.status_code == 200:
                print("Append successful:", response.text)
            else:
                print("Error during append:", response.text)
            return response.text
        except requests.RequestException as e:
            print("HTTPError during append:", e)
            return None

    def delete(self, key: str):
        """
        Deletes data associated with a key.

        Args:
            key (str): Key identifying the data to delete.

        Returns:
            str or None: Server response text or None if an error occurs.
        """
        try:
            response = requests.delete(
                f"{config.api_url}/delete/{key}", 
                headers=self.headers
            )
            if response.status_code == 200:
                print("Delete successful:", response.text)
            else:
                print("Error during delete:", response.text)
            return response.text
        except requests.RequestException as e:
            print("HTTPError during delete:", e)
            return None

    def get(self, key: str):
        """
        Retrieves files associated with a key.

        Args:
            key (str): Key identifying the data to retrieve.

        Returns:
            List[bytes] or None: List of file data in bytes if successful, else None.
        """
        try:
            response = requests.get(
                f"{config.api_url}/get/{key}", 
                headers=self.headers
            )
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