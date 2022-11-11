from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import app.helpers as helpers
import app.schemas as schemas
from pathlib import Path
import os

ROOT_DIRECTORY = os.environ.get("ROOT_DIRECTORY", str(Path().absolute())+"/")
# ROOT_DIRECTORY = "/home/my_user/otherstuff/foo/"
# ROOT_DIRECTORY = (
#     "/home/jeterg/Documents/GitHub/RestAPI/data/home/my_user/otherstuff/foo/"
# )
tools = helpers.Helper(ROOT_DIRECTORY)
main_route = "/{specified_path:path}"
tags_metadata = [{"name": main_route, "description": ""}]

app = FastAPI(version="0.0.1", openapi_tags=tags_metadata)


@app.get(main_route, status_code=200, responses={404: {"model": schemas.NotFound}})
def get_directory_or_file_contents(request: Request, specified_path: str = "/") -> dict:
    full_path = ROOT_DIRECTORY + specified_path
    if specified_path == "":
        specified_path = "/"
    url = str(request.url)
    if not url.endswith("/"):
        url = f"{url}/"
    base_json = {
        "_link": url,
        "ROOT_DIRECTORY": ROOT_DIRECTORY,
    }
    if os.path.exists(full_path):
        if os.path.isfile(full_path):
            file = open(full_path)
            file_name = specified_path.split("/")[-1]
            return {
                **base_json,
                "Count": 1,
                "Content": [
                    {
                        **tools.get_json_body(file_name, full_path),
                        "Data": file.read(),
                    }
                ],
            }
        content = [
            tools.get_json_body(file_name, full_path)
            for file_name in os.listdir(full_path)
        ]
        json_result = {"Content": content, "Count": len(content), **base_json}

        return json_result
    else:
        base_json["error"] = f"INVALID PATH: {specified_path}"
        return JSONResponse(status_code=404, content=base_json)


@app.post(
    "/post" + main_route,
    status_code=200,
    responses={400: {"model": schemas.BadRequest}},
)
def create_file_or_directory(
    request: Request,
    specified_path: str,
    file_or_directory: str = "d",
    content: str = "",
) -> dict:
    file_or_directory = file_or_directory.lower()
    full_path = ROOT_DIRECTORY + specified_path
    path = Path(full_path)
    base_json = {"_link": str(request.url)}
    creating_file = file_or_directory in ["f", "file"]
    creating_directory = file_or_directory in ["d", "directory"]
    if not (creating_file or creating_directory):
        return JSONResponse(
            status_code=400,
            content={
                "error": f"INVALID `file_or_directory` type: {file_or_directory}",
                **base_json,
            },
        )
    if path.exists():
        msg = f"{full_path} Already exists. "
        if creating_file:
            msg += f"Try endpoint `{ROOT_DIRECTORY}/put/` to update"
        return JSONResponse(status_code=400, content={"error": msg, **base_json})
    if creating_file:
        tools.create_new_file(file_path=specified_path, content=content)
        return {
            "detail": f"Created file at {ROOT_DIRECTORY}{specified_path}",
            **base_json,
        }
    elif creating_directory:
        tools.create_directory(full_path)
        return {"detail": f"Created directories {full_path}", **base_json}


@app.put(
    "/put" + main_route, status_code=200, responses={400: {"model": schemas.BadRequest}}
)
def update_file(
    request: Request, specified_path: str, content: str = "", overwite: bool = False
) -> dict:
    full_path = ROOT_DIRECTORY + specified_path
    path = Path(full_path)
    base_json = {"_link": str(request.url)}
    if not path.exists():
        raise HTTPException(
            status_code=400,
            detail={"error": f"{full_path} does not exist.", **base_json},
        )
    elif not path.is_file():
        raise HTTPException(
            status_code=400,
            detail={"error": f"{full_path} is not a File", **base_json},
        )
    if overwite:
        tools.overwrite_existing_file(specified_path, content)
    else:
        tools.extend_existing_file(specified_path, content)

    return {"detail": f"Updated File {full_path}", **base_json}


@app.delete(
    "/delete" + main_route,
    status_code=200,
    responses={400: {"model": schemas.BadRequest}},
)
def delete(request: Request, specified_path: str) -> dict:
    full_path = ROOT_DIRECTORY + specified_path
    base_json = {"_link": str(request.url)}
    if tools.delete_file_or_directory(full_path):
        return {"detail": f"deleted {full_path}", **base_json}
    return JSONResponse(
        status_code=400, content={"error": f"{full_path} does not exist.", **base_json}
    )

