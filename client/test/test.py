#import the module here
#define tha path to the test files below to encode and push to API server
import base64
import os
import requests

#to Test retrieve fucntion
def get_file(key):
    try:
        directory_key = f"./{key}_new"
        os.makedirs(directory_key , exist_ok=True)
        files = retreieve(key)
        for index, file in enumerate(files):
        
            decoded_data = base64.b64decode(file)
            filename = f"file_{index}.jpg"
            output_file_path = os.path.join(directory_key, filename)
            with open(output_file_path, "wb") as output_file:
                output_file.write(decoded_data)
            print(f"File {index} written to {output_file_path}")
    except Exception as e:
        print("Error:", e)
#MODIFY THE BELOW PARAMETERS TO TEST retrieve FUCNTION 
'''key="test1"
get_file(key)'''


#to Test save fucntion
def encode_and_store_files(directory_path):
    encoded_content = []
    API_URL = "http://127.0.0.1:8000"
    key = "string_test2"

    try:
        # Iterate over each file in the specified directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            if os.path.isfile(file_path):
                # Read the content of the file
                with open(file_path, 'rb') as file:
                    file_content = file.read()

                # Encode the file content to base64
                encoded_file_content = base64.b64encode(file_content)

                # Append the encoded content to the list
                encoded_content.append(encoded_file_content)

        # Pass the list of encoded content to the next file
        save(API_URL, key,encoded_content)
    
    except Exception as e:
        print(f"Error: {e}")

#MODIFY THE BELOW PARAMETERS TO TEST UPLOAD FUCNTION 
'''if __name__ == "__main__":
    directory_path = 'Path to directory of files'
    encode_and_store_files(directory_path)'''

#to Test the update fucntion 

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
        print("Error:", e)\
#MODIFY THE BELOW PARAMETERS TO TEST UPDATE FUCNTION 
'''
new_key="Enter new key value or None if no new Key value"
key="Enter the key value"
API_URL = "API_URL_SERVER"
directory_path = r"Directory Path"
'''