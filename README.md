## Browse file system Using RESTapi
This is a RESTapi created using [FastAPI](https://fastapi.tiangolo.com/) because of it's handy Swagger documentation that helps to get things up and runnin smoothly and quickly. Along with [Uvicorn](https://www.uvicorn.org/) as the server host.
In this api you can
- Specify root directory on initial run
- List files and diresctories along with their permissions, names, owners and size
- Create new files and directories
- Update files by overwritting them or extending them
- delete files and directories
### Documentation
Static Swagger Documentation with endpoint and response schemas breakdowns can be found [here](https://jeterg.github.io/Browsable-Directory-RESTapi/), although currently the `try it out` will not work.
When the api is running with docker the interactive documentatoin  will be available at:
- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) 
### Application Architecture
The main additions necessary are Python, Docker 
Note: This was developed on a linux machine.

1 - Install Python:
 ```
 sudo apt-get install python3.8
 ```
2 - [Install Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)

### Building, and Running

The `ROOT_DIRECTORY` can be specified on each docker run. In order to deploy the docker image that will be hosting the restapi, you can run `startup_script.py` with replacing root_directory and in the commandline:
 ```py
 ROOT_DIRECTORY=`{root_directory}` python3 startup_script.py
 ```
 Example:
 ```py
ROOT_DIRECTORY="/home/my_user/otherstuff/foo/" python3 script.py
 ```
 <details>
 
 <summary>The result should then be the output of the image being built, the tests running and Uvicorn successfully running. </summary> 
  
 ```py
 ROOT_DIRECTORY="/home/my_user/otherstuff/foo/" python3 script.py
Sending build context to Docker daemon  129.3MB
Step 1/11 : FROM python:3.9
 ---> ab0d2f900193
Step 2/11 : WORKDIR /code
 ---> Using cache
 ---> af7a24b20f1a
Step 3/11 : COPY ./requirements.txt /code/requirements.txt
 ---> Using cache
 ---> 1d303e2d8a8f
Step 4/11 : RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
 ---> Using cache
 ---> abddb3243647
Step 5/11 : EXPOSE 8000:8000
 ---> Using cache
 ---> 3cacbd1d3c32
Step 6/11 : COPY ./app /code/app
 ---> Using cache
 ---> b80514c4912c
Step 7/11 : COPY ./data/home /home
 ---> Using cache
 ---> 23b9e352fe86
Step 8/11 : COPY ./test_directory /code/test_directory
 ---> Using cache
 ---> 81ad716c65c4
Step 9/11 : COPY ./test /code/test
 ---> 49e908e84f94
Step 10/11 : RUN ["pytest","-vv"]
 ---> Running in 9af9439c593c
============================= test session starts ==============================
platform linux -- Python 3.9.15, pytest-7.2.0, pluggy-1.0.0 -- /usr/local/bin/python
cachedir: .pytest_cache
rootdir: /code
plugins: anyio-3.6.2
collecting ... collected 19 items

test/test_main.py::test_main_route PASSED                                [  5%]
test/test_main.py::test_one_directory_deep PASSED                        [ 10%]
test/test_main.py::test_several_directories_deep PASSED                  [ 15%]
test/test_main.py::test_retrieve_file PASSED                             [ 21%]
test/test_main.py::test_list_hidden_file PASSED                          [ 26%]
test/test_main.py::test_main_route_not_found PASSED                      [ 31%]
test/test_main.py::test_create_directory PASSED                          [ 36%]
test/test_main.py::test_create_file PASSED                               [ 42%]
test/test_main.py::test_bad_create_file PASSED                           [ 47%]
test/test_main.py::test_bad_create_directory PASSED                      [ 52%]
test/test_main.py::test_bad_create_arguments PASSED                      [ 57%]
test/test_main.py::test_extend_file_contents PASSED                      [ 63%]
test/test_main.py::test_overwrite_file_contents PASSED                   [ 68%]
test/test_main.py::test_update_non_existing_file PASSED                  [ 73%]
test/test_main.py::test_bad_update_file_request PASSED                   [ 78%]
test/test_main.py::test_delete_file PASSED                               [ 84%]
test/test_main.py::test_bad_delete_file PASSED                           [ 89%]
test/test_main.py::test_delete_directory PASSED                          [ 94%]
test/test_main.py::test_bad_delete_directory PASSED                      [100%]

============================== 19 passed in 0.38s ==============================
Removing intermediate container 9af9439c593c
 ---> d1ced2bb9e7f
Step 11/11 : CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
 ---> Running in 628ba70b0d52
Removing intermediate container 628ba70b0d52
 ---> f75fc8a9efa3
Successfully built f75fc8a9efa3
Successfully tagged restapi:latest
INFO:     Will watch for changes in these directories: ['/code']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [1] using StatReload
INFO:     Started server process [7]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
 </details>

### Request Script
Once the server is live and running on the docker image, can start making requests to the api, there is another script with some requests that can be ran as well  by running the following on a different shell instance:
```py
python3 curling_script.py
```

<details>

<summary>It will make the requests using curl and print the curl command and the json_content response</summary>

```py

COMMAND:  curl -s 127.0.0.1:8000
{
   "Content" : [
      {
         "File_Name" : "foo2",
         "Owner" : "root",
         "Permissions" : "664",
         "Size" : 29,
         "Type" : "file"
      },
      {
         "File_Name" : "foo1",
         "Owner" : "root",
         "Permissions" : "664",
         "Size" : 29,
         "Type" : "file"
      },
      {
         "File_Name" : "bar",
         "Owner" : "root",
         "Permissions" : "775",
         "Size" : 4096,
         "Type" : "directory"
      }
   ],
   "Count" : 3,
   "ROOT_DIRECTORY" : "/home/my_user/otherstuff/foo/",
   "_link" : "http://127.0.0.1:8000/"
}


COMMAND:  curl -s 127.0.0.1:8000/bar
{
   "Content" : [
      {
         "File_Name" : "bar1",
         "Owner" : "root",
         "Permissions" : "664",
         "Size" : 30,
         "Type" : "file"
      },
      {
         "File_Name" : "baz",
         "Owner" : "root",
         "Permissions" : "775",
         "Size" : 4096,
         "Type" : "directory"
      }
   ],
   "Count" : 2,
   "ROOT_DIRECTORY" : "/home/my_user/otherstuff/foo/",
   "_link" : "http://127.0.0.1:8000/bar/"
}


COMMAND:  curl -s 127.0.0.1:8000/foo1
{
   "Content" : [
      {
         "Data" : "Contents found in file foo1!\n",
         "File_Name" : "foo1",
         "Owner" : "root",
         "Permissions" : "664",
         "Size" : 29,
         "Type" : "file"
      }
   ],
   "Count" : 1,
   "ROOT_DIRECTORY" : "/home/my_user/otherstuff/foo/",
   "_link" : "http://127.0.0.1:8000/foo1/"
}


COMMAND:  curl -s 127.0.0.1:8000/bar/bar1
{
   "Content" : [
      {
         "Data" : "Contents found in file bar 1!\n",
         "File_Name" : "bar1",
         "Owner" : "root",
         "Permissions" : "664",
         "Size" : 30,
         "Type" : "file"
      }
   ],
   "Count" : 1,
   "ROOT_DIRECTORY" : "/home/my_user/otherstuff/foo/",
   "_link" : "http://127.0.0.1:8000/bar/bar1/"
}


COMMAND:  curl -s -X POST 127.0.0.1:8000/post/new_directory
{
   "_link" : "http://127.0.0.1:8000/post/new_directory",
   "detail" : "Created directories /home/my_user/otherstuff/foo/new_directory"
}


COMMAND:  curl -s  -X POST '127.0.0.1:8000/post/new_directory/new_file.txt?file_or_directory=file&content=NEW%21%21'
{
   "_link" : "http://127.0.0.1:8000/post/new_directory/new_file.txt?file_or_directory=file&content=NEW%21%21",
   "detail" : "Created file at /home/my_user/otherstuff/foo/new_directory/new_file.txt"
}


COMMAND:  curl -s  -X PUT '127.0.0.1:8000/put/new_directory/new_file.txt?file_or_directory=file&content=Continued!'
{
   "_link" : "http://127.0.0.1:8000/put/new_directory/new_file.txt?file_or_directory=file&content=Continued!",
   "detail" : "Updated File /home/my_user/otherstuff/foo/new_directory/new_file.txt"
}


COMMAND:  curl -s 127.0.0.1:8000/new_directory/new_file.txt
{
   "Content" : [
      {
         "Data" : "NEW!!\nContinued!",
         "File_Name" : "new_file.txt",
         "Owner" : "root",
         "Permissions" : "644",
         "Size" : 16,
         "Type" : "file"
      }
   ],
   "Count" : 1,
   "ROOT_DIRECTORY" : "/home/my_user/otherstuff/foo/",
   "_link" : "http://127.0.0.1:8000/new_directory/new_file.txt/"
}


COMMAND:  curl -s  -X PUT '127.0.0.1:8000/put/new_directory/new_file.txt?file_or_directory=file&content=Overwritten!!&overwite=true'
{
   "_link" : "http://127.0.0.1:8000/put/new_directory/new_file.txt?file_or_directory=file&content=Overwritten!!&overwite=true",
   "detail" : "Updated File /home/my_user/otherstuff/foo/new_directory/new_file.txt"
}


COMMAND:  curl -s 127.0.0.1:8000/new_directory/new_file.txt
{
   "Content" : [
      {
         "Data" : "Overwritten!!",
         "File_Name" : "new_file.txt",
         "Owner" : "root",
         "Permissions" : "644",
         "Size" : 13,
         "Type" : "file"
      }
   ],
   "Count" : 1,
   "ROOT_DIRECTORY" : "/home/my_user/otherstuff/foo/",
   "_link" : "http://127.0.0.1:8000/new_directory/new_file.txt/"
}


COMMAND:  curl -s 127.0.0.1:8000/new_directory
{
   "Content" : [
      {
         "File_Name" : "new_file.txt",
         "Owner" : "root",
         "Permissions" : "644",
         "Size" : 13,
         "Type" : "file"
      }
   ],
   "Count" : 1,
   "ROOT_DIRECTORY" : "/home/my_user/otherstuff/foo/",
   "_link" : "http://127.0.0.1:8000/new_directory/"
}


COMMAND:  curl -s -X DELETE 127.0.0.1:8000/delete/new_directory/new_file.txt
{
   "_link" : "http://127.0.0.1:8000/delete/new_directory/new_file.txt",
   "detail" : "deleted /home/my_user/otherstuff/foo/new_directory/new_file.txt"
}


COMMAND:  curl -s 127.0.0.1:8000/new_directory
{
   "Content" : [],
   "Count" : 0,
   "ROOT_DIRECTORY" : "/home/my_user/otherstuff/foo/",
   "_link" : "http://127.0.0.1:8000/new_directory/"
}


COMMAND:  curl -s -X DELETE 127.0.0.1:8000/delete/new_directory
{
   "_link" : "http://127.0.0.1:8000/delete/new_directory",
   "detail" : "deleted /home/my_user/otherstuff/foo/new_directory"
}
```
</details>

#### Helm Chart Data

https://jeterg.github.io/public-Helm-charts-/index.yaml

https://jeterg.github.io/public-Helm-charts-/charts/Browsable-Directory-RESTapi/Chart.yaml
