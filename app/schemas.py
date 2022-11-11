from pydantic import BaseModel
from typing import List, Union


class BadRequest(BaseModel):
    error: str = "error"


class NotFound(BaseModel):
    error: str = "INVALID PATH: failed"
    link: str = "http://127.0.0.1:8000/failed"
    ROOT_DIRECTORY: str = "/home/my_user/otherstuff/foo/"


class DirectoryDescriptions(BaseModel):

    File_name: str = "foo"
    Owner: str = "user"
    Size: int = 5000
    Permissions: int = 664
    Type: str = "file"


class FileContent(DirectoryDescriptions):
    """Adding File Content when Request is directly a file path"""

    Data: str = "Content Data!!"


class DirectoryContents(BaseModel):
    """Listing Contents of Directory Path"""

    Content: List[Union[DirectoryDescriptions, FileContent]] = [
        {
            "File_Name": "foo2",
            "Owner": "user_name",
            "Size": 29,
            "Permissions": "664",
            "Type": "file",
        },
        {
            "File_Name": "foo1",
            "Owner": "user_name",
            "Size": 29,
            "Permissions": "664",
            "Type": "file",
        },
        {
            "File_Name": "bar",
            "Owner": "user_name",
            "Size": 4096,
            "Permissions": "775",
            "Type": "directory",
        },
    ]
    Count: int = 3
    ROOT_DIRECTORY: str = "/home/my_user/otherstuff/foo/"
    link: str = "http://127.0.0.1:8000/"


class SuccessfulDelete(BaseModel):
    """200 response for Delete endpoint"""

    detail: str = "deleted /home/my_user/otherstuff/foo/lost_file.txt"
    ROOT_DIRECTORY: str = "/home/my_user/otherstuff/foo/"
    link: str = "http://127.0.0.1:8000/delete/lost_file.txt"


class SuccessfulPut(BaseModel):
    """200 response for Put endpoint/ updating files"""

    detail: str = "Updated File /home/my_user/otherstuff/foo/lost_file.txt"
    ROOT_DIRECTORY: str = "/home/my_user/otherstuff/foo/"
    link: str = "http://127.0.0.1:8000/put/lost_file.txt"


class SuccessfulPost(BaseModel):
    """200 response for Put endpoint/ creating files or directories"""

    detail: str = "Created file at /home/my_user/otherstuff/foo/new_file.txt"
    ROOT_DIRECTORY: str = "/home/my_user/otherstuff/foo/"
    link: str = "http://127.0.0.1:8000/post/new_file.txt"
