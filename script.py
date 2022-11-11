import os
from pathlib import Path

ROOT_DIRECTORY = os.environ.get("ROOT_DIRECTORY", str(Path().absolute()) + "/")
os.system("docker build  --force-rm -t restapi  .")
os.system(
    f"docker run -e ROOT_DIRECTORY={ROOT_DIRECTORY} -p 8000:8000 -t -i restapi:restapi"
)
