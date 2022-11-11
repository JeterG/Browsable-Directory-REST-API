from fastapi.testclient import TestClient
import os
from pathlib import Path

os.environ["ROOT_DIRECTORY"] = str(Path().absolute()) + "/test_directory/"
from app.main import app

test_client = TestClient(app)


def test_main_route():
    response = test_client.get("/")
    json_resp = response.json()
    print(json_resp)
    assert json_resp["Count"] == 1
    assert json_resp["Content"][0]["File_Name"] == "home"
    assert json_resp["_link"] == "http://testserver/"


def test_one_directory_deep():
    response = test_client.get("/home")
    json_resp = response.json()
    print(json_resp)
    assert json_resp["Count"] == 1
    assert json_resp["Content"][0]["File_Name"] == "my_user"
    assert json_resp["_link"] == "http://testserver/home/"


def test_several_directories_deep():
    response = test_client.get("/home/my_user/otherstuff/foo")
    json_resp = response.json()
    assert json_resp["Count"] == 3
    assert json_resp["_link"] == "http://testserver/home/my_user/otherstuff/foo/"


def test_retrieve_file():
    response = test_client.get("/home/my_user/otherstuff/foo/foo1")
    json_resp = response.json()
    assert json_resp["Count"] == 1
    assert json_resp["Content"][0]["Data"] == "Contents found in file foo1!\n"


def test_list_hidden_file():
    response = test_client.get("/home/my_user/otherstuff/hidden_files")
    json_resp = response.json()
    print(json_resp)
    names = {obj["File_Name"] for obj in json_resp["Content"]}
    assert json_resp["Count"] == 2
    assert names == {"not_hidden_file", ".hidden_file"}


def test_main_route_not_found():
    response = test_client.get("ShouldFail")
    assert response.status_code == 404
    assert response.json()["error"] == "INVALID PATH: ShouldFail"


def test_create_directory():
    response = test_client.post("post/new_directory?file_or_directory=d")
    assert "Created directories" in response.json()["detail"]
    response = test_client.get("new_directory")
    assert response.status_code == 200
    assert response.json()["Content"] == []


def test_create_file():
    response = test_client.post(
        "post/new_directory/new_file.txt?file_or_directory=f&content=Look a new file!"
    )
    assert response.status_code == 200
    assert "Created file" in response.json()["detail"]
    response = test_client.get("new_directory/new_file.txt")
    assert response.json()["Content"][0]["Data"] == "Look a new file!"


def test_bad_create_file():
    response = test_client.post("post/new_directory/new_file.txt?file_or_directory=f")
    assert "Already exists" in response.json()["error"]
    assert response.status_code == 400


def test_bad_create_directory():
    response = test_client.post("post/new_directory?file_or_directory=d")
    assert "Already exists" in response.json()["error"]
    assert response.status_code == 400


def test_bad_create_arguments():
    response = test_client.post("post/new_directory?file_or_directory=text_file")
    assert "INVALID" in response.json()["error"]
    assert response.status_code == 400


def test_extend_file_contents():
    response = test_client.put(
        "/put/new_directory/new_file.txt?content=NEW!!!&overwite=false"
    )
    assert "Updated" in response.json()["detail"]
    response = test_client.get("/new_directory/new_file.txt")
    assert response.json()["Content"][0]["Data"] == "Look a new file!\nNEW!!!"


def test_overwrite_file_contents():
    response = test_client.put(
        "/put/new_directory/new_file.txt?content=Overwritten!&overwite=true"
    )
    assert "Updated" in response.json()["detail"]
    response = test_client.get("/new_directory/new_file.txt")
    assert response.json()["Content"][0]["Data"] == "Overwritten!"


def test_update_non_existing_file():
    response = test_client.put(
        "/put/new_directory/ghost_file.txt?content=Overwritten!&overwite=true"
    )
    assert "does not exist" in response.json()["detail"]["error"]
    assert response.status_code == 400


def test_bad_update_file_request():
    response = test_client.put("/put/new_directory?content=Overwritten!&overwite=true")
    assert "is not a File" in response.json()["detail"]["error"]
    assert response.status_code == 400


def test_delete_file():
    response = test_client.delete("/delete/new_directory/new_file.txt")
    assert "deleted" in response.json()["detail"]
    assert response.status_code == 200


def test_bad_delete_file():
    response = test_client.delete("/delete/new_directory/new_file.txt")
    assert "does not exist" in response.json()["error"]
    assert response.status_code == 400


def test_delete_directory():
    response = test_client.delete("/delete/new_directory")
    assert "deleted" in response.json()["detail"]
    assert response.status_code == 200


def test_bad_delete_directory():
    response = test_client.delete("/delete/new_directory")
    assert "does not exist" in response.json()["error"]
    assert response.status_code == 400
