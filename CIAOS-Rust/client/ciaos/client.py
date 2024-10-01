# client.py

from Store import FileData, FileDataList  # Ensure 'Store' is generated from your .fbs file
import flatbuffers
import requests

def create_flatbuffer(data_list):
    """
    Serializes a list of byte arrays into FlatBuffers binary format.

    Args:
        data_list (List[bytes]): List of file data in bytes.

    Returns:
        bytes: Serialized FlatBuffers data, or None if an error occurs.
    """
    try:
        builder = flatbuffers.Builder(1024)
        file_data_offsets = []
        for data in data_list:
            data_offset = builder.CreateByteVector(data)

            # Create FileData
            FileData.FileDataStart(builder)
            FileData.FileDataAddData(builder, data_offset)
            file_data_offset = FileData.FileDataEnd(builder)
            file_data_offsets.append(file_data_offset)

        # Create vector of FileData
        FileDataList.FileDataListStartFilesVector(builder, len(file_data_offsets))
        for fd_offset in reversed(file_data_offsets):
            builder.PrependUOffsetTRelative(fd_offset)
        files_vector = builder.EndVector(len(file_data_offsets))

        # Create the FileDataList
        FileDataList.FileDataListStart(builder)
        FileDataList.FileDataListAddFiles(builder, files_vector)
        file_data_list_offset = FileDataList.FileDataListEnd(builder)

        builder.Finish(file_data_list_offset)

        buf = builder.Output()
        return buf
    except Exception as e:
        print("Error creating FlatBuffers data:", e)
        return None

def get_data_vector(file_data_fb_obj):
    """
    Extracts the byte array from a FileData FlatBuffer object.

    Args:
        file_data_fb_obj: A FileData FlatBuffer object.

    Returns:
        bytes or None: The extracted byte array or None if not present.
    """
    try:
        o = file_data_fb_obj._tab.Offset(4)
        if o != 0:
            data_length = file_data_fb_obj.DataLength()
            data_start = file_data_fb_obj._tab.Vector(o)
            data_bytes = file_data_fb_obj._tab.Bytes[data_start : data_start + data_length]
            return data_bytes
        return None
    except Exception as e:
        print(f"Error extracting data vector: {e}")
        return None

def parse_flatbuffer(flatbuffer_data):
    """
    Deserializes FlatBuffers data and extracts file byte arrays.

    Args:
        flatbuffer_data (bytes): Serialized FlatBuffers data.

    Returns:
        List[bytes]: List of file data in bytes.
    """
    try:
        file_data_list = []
        buf = bytearray(flatbuffer_data)

        # Get root object
        file_data_list_fb = FileDataList.FileDataList.GetRootAsFileDataList(buf, 0)
        num_files = file_data_list_fb.FilesLength()
        print(f"Number of files: {num_files}")

        for i in range(num_files):
            file_data_fb_obj = file_data_list_fb.Files(i)
            data_bytes = get_data_vector(file_data_fb_obj)
            if data_bytes is None:
                print(f"No data for file {i}")
                continue
            file_data_list.append(data_bytes)
            print(f"Retrieved file {i}, size {len(data_bytes)} bytes")

        print(f"Parsed {len(file_data_list)} files from FlatBuffer.")
        return file_data_list
    except Exception as e:
        print("Error parsing FlatBuffers data:", e)
        return []

def save(api_url, key, data_list):
    """
    Uploads new files to the server under a unique key.

    Args:
        api_url (str): Base URL of the API.
        key (str): Unique key for the upload.
        data_list (List[bytes]): List of file data in bytes.

    Returns:
        requests.Response or None: The server's response or None if an error occurs.
    """
    try:
        flatbuffer_data = create_flatbuffer(data_list)
        if flatbuffer_data is None:
            print("Failed to create FlatBuffers data.")
            return None

        headers = {'Content-Type': 'application/octet-stream'}
        response = requests.post(f"{api_url}/upload/{key}", data=flatbuffer_data, headers=headers)

        if response.status_code == 200:
            print("Upload successful:", response.text)
        else:
            print("Error during upload:", response.text)
        return response
    except requests.RequestException as e:
        print("HTTPError during upload:", e)
        return None

def update_key(api_url, old_key, new_key):
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
        response = requests.put(f"{api_url}/update/{old_key}/{new_key}")
        if response.status_code == 200:
            print("Key update successful:", response.text)
            return response.text
        else:
            print("Error updating key:", response.text)
            return response.text
    except requests.RequestException as e:
        print("HTTPError during key update:", e)
        return None

def update_data(api_url, key, data_list):
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

        headers = {'Content-Type': 'application/octet-stream'}
        response = requests.post(f"{api_url}/update_data/{key}", data=flatbuffer_data, headers=headers)

        if response.status_code == 200:
            print("Data update successful:", response.text)
        else:
            print("Error during data update:", response.text)
        return response
    except requests.RequestException as e:
        print("HTTPError during data update:", e)
        return None

def append(api_url, key, data_list):
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

        headers = {'Content-Type': 'application/octet-stream'}
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

def delete_key(api_url, key):
    """
    Deletes data associated with a key.

    Args:
        api_url (str): Base URL of the API.
        key (str): Key identifying the data to delete.

    Returns:
        str or None: Server response text or None if an error occurs.
    """
    try:
        response = requests.delete(f"{api_url}/delete/{key}")
        if response.status_code == 200:
            print("Delete successful:", response.text)
            return response.text
        else:
            print("Error during delete:", response.text)
            return response.text
    except requests.RequestException as e:
        print("HTTPError during delete:", e)
        return None

def get(api_url, key):
    """
    Retrieves files associated with a key.

    Args:
        api_url (str): Base URL of the API.
        key (str): Key identifying the data to retrieve.

    Returns:
        List[bytes] or None: List of file data in bytes if successful, else None.
    """
    try:
        response = requests.get(f"{api_url}/get/{key}")
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

