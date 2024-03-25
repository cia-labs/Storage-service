from fastapi.testclient import TestClient
import pydantic
import os
import sys

pydantic_version = '.'.join(pydantic.__version__.split('.')[:2])

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.join(current_dir, '..')  # Go up two levels to reach /Ciaos/server/
sys.path.append(parent_path)
from main import app

client = TestClient(app)

def test_upload_retrieve():
    #test for upload sucess
    key = None  
    encoded_content = ["encoded_content_1", "encoded_content_2"]
    
    response = client.post("/upload/", data={"key": key, "encoded_content": encoded_content})

    assert response.status_code == 200

    response_data = response.json()
    generated_key = response_data.get("key", None)
    assert response_data == {"message": "File uploaded successfully", "key": generated_key}
    test_key = generated_key

    #test for failue of upload
    response = client.post(
        "/upload/",
        data={"key": "test", "encoded_content": []}
    )
    print(response.json())
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "encoded_content"],
                "msg": "Field required",
                "input": None,
                "url": f"https://errors.pydantic.dev/{pydantic_version}/v/missing"
            }
        ]
    }
    # test for retreive 
    key = generated_key

    response = client.get(f"/get/{key}")
    print(response.status_code)
    print(response.content)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

#test for failure of retrieve
    non_existent_key = "nonexistentkey"

    response = client.get(f"/get/{non_existent_key}")

    print(response.status_code)
    print(response.content)

    assert response.status_code == 500
    assert response.json() == {'detail': '404: Key not found'}
#test for update sucess
    key = "test_key"
    new_key = "new_test_key"
    encoded_content = ["encoded_content_3", "encoded_content_4"]

    response = client.put(f"/update/?key={key}&new_key={new_key}", data={"encoded_content": encoded_content})
    assert response.status_code == 200
    assert response.json() == {"message": "Files updated successfully"}
#test for failure of update
    key = "non_existent_key"
    new_key = "new_key"
    encoded_content = ["encoded_content_3", "encoded_content_4"]

    response = client.put(f"/update/?key={key}&new_key={new_key}", data={"encoded_content": encoded_content})
    assert response.status_code == 404
    assert response.json() == {"detail": "Key not found"}
#test for delete sucess
    key = "test_key"

    response = client.delete(f"/delete/?key={key}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Folder '{key}' and its contents deleted successfully"}
#test for failure of delete
    non_existent_key = "non_existent_key"

    response = client.delete(f"/delete/?key={non_existent_key}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Folder not found"}