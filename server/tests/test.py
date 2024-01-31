import base64
import os
import requests

new_key="Enter new key or None if no value provided"
key="Enter the key"
API_URL = "API_URL_SERVER"
directory_path = r"Directory_path"


def encode_and_store_files(directory_path):
    encoded_content = []
    try:

        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            if os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    file_content = file.read()

                encoded_file_content = base64.b64encode(file_content)
                encoded_content.append(encoded_file_content)

        try:
            data = {"key": key, "encoded_content": encoded_content}
            response = requests.post(f"{API_URL}/upload/", data=data)

            if response.status_code == 200:
                print("Update successful:", response.json())
            else:
                raise requests.HTTPError(response.text)

        except requests.HTTPError as e:
            print("Error:", e)


    except Exception as e:
        print(f"Error: {e}")


def get_file(key):
    try:

        directory_key = f"./{key}_new"
        os.makedirs(directory_key , exist_ok=True)
        try:

            response= requests.get(f"{API_URL}/retrieve/{key}")
            if response.status_code == 200:
                print("Update successful:", response.json())
                return response.json()
            else:
                raise requests.HTTPError(response.text)

        except requests.HTTPError as e:
            print("Error:", e)


        for index, file in enumerate(response):

            decoded_data = base64.b64decode(file)
            filename = f"file_{index}.jpg"
            output_file_path = os.path.join(directory_key, filename)

            with open(output_file_path, "wb") as output_file:
                output_file.write(decoded_data)

            print(f"File {index} written to {output_file_path}")

    except Exception as e:
        print("Error:", e)

def update(API_URL, key,directory_path, new_key=None):
    try:
        encoded_content = []

        try:

            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)

                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as file:
                        file_content = file.read()

                    encoded_file_content = base64.b64encode(file_content)
                    encoded_content.append(encoded_file_content)

        except Exception as e:
            print(f"Error: {e}")

        data = {"new_key":new_key,"encoded_content": encoded_content}
        response = requests.put(f"{API_URL}/update/?key={key}", data=data)

        if response.status_code == 200:
            print("Update successful:", response.json())
        else:
            raise requests.HTTPError(response.text)

    except requests.HTTPError as e:
        print("Error:", e)

def delete(API_URL, key):
    try:
        response = requests.delete(f"{API_URL}/delete/?key={key}")

        if response.status_code == 200:
            print("Update successful:", response.json())
        else:
            raise requests.HTTPError(response.text)

    except requests.HTTPError as e:
        print("Error:", e)


# encode_and_store_files(directory_path)
# get_file(key)
# update(API_URL,key,directory_path,new_key)
# delete(API_URL,key)