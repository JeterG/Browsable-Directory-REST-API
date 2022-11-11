from typing import Optional
from pydantic import BaseModel


class BadRequest(BaseModel):
    error: str


class NotFound(BaseModel):
    error: str
    link: str
    ROOT_DIRECTORY: str