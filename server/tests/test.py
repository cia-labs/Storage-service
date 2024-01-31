#import the module here
#define tha path to the test files below to encode and push to API server
#Note see to that u modify the API_URL to the fastapi server 
 
import base64
import os
import requests


#Moodify URL if u need to


API_URL = "http://127.0.0.1:8000"


#to check retrieve fucntion
#Note the below retrieve fucntion is expecting to recieve a Image type / so if u plan on chnaging the type of file to recieve modify the extension in the variable name "filename"

key="enter the key to test"

def get_file(key):
    try:
        
        directory_key = f"./{key}_new"
        os.makedirs(directory_key , exist_ok=True)
        try:
            response= requests.get(f"{API_URL}/retrieve/{key}")
            if response.status_code == 200:
                return response.json()
                print("Update successful:", response.json())
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
get_file(key)

#to check save fucntion
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

# Example usage
if __name__ == "__main__":
    directory_path = 'Path to directory of files'
    encode_and_store_files(directory_path)
