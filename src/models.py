
from pydantic import BaseModel, Field
from pydantic import ValidationError
from datetime import date
from starlette.datastructures import UploadFile

class Category(BaseModel):
    title : str
    description : str

class Blog(BaseModel):
    title: str
    desciption: str = None
    author : str
    tags : str = None
    created_date : date = None
