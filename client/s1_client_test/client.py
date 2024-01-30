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