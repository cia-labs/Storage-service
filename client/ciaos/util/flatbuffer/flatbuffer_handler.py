#flatbuffer_handler.py
import flatbuffers
from util.flatbuffer import FileData, FileDataList


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
