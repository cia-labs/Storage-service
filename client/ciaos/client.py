import requests


def save(API_URL, key, value):
    try:
        data = {"key": key, "encoded_content": value}
        response = requests.post(f"{API_URL}/upload/", data=data)

        if response.status_code == 200:
            print("Update successful:", response.json())
        else:
            raise requests.HTTPError(response.text)

    except requests.HTTPError as e:
        print("Error:", e)

def retreieve(API_URL, key):
    try:
        response= requests.get(f"{API_URL}/retrieve/{key}")
        if response.status_code == 200:
            return response.json()
            print("Update successful:", response.json())
        else:
            raise requests.HTTPError(response.text)

    except requests.HTTPError as e:
        print("Error:", e)


def update(API_URL,key,value,new_key=None):
    try:
        data = {"new_key": new_key, "encoded_content": value}
        response = requests.put(f"{API_URL}/update/?key={key}", data=data)

        if response.status_code == 200:
            print("Update successful:", response.json())
        else:
            raise requests.HTTPError(response.text)

    except requests.HTTPError as e:
        print("Error:", e)


def delete(API_URL,key):
    try:
        response = requests.delete(f"{API_URL}/delete/?key={key}")

        if response.status_code == 200:
            print("Update successful:", response.json())
        else:
            raise requests.HTTPError(response.text)

    except requests.HTTPError as e:
        print("Error:", e)