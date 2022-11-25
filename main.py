from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import text
import datetime

app = FastAPI()

class Author(BaseModel):
    id: int
    nickname: str
    is_blocked: bool
    faves_id_list: list
    date_created: datetime.datetime
    date_updated: datetime.datetime

class Recipe(BaseModel):
    id: int
    author_nickname: str
    date_created: datetime.datetime
    date_updated: datetime.datetime
    title: str
    dish_type: str
    description: text
    steps_to_complete: text
    pictures: str
    likes: int
    tags: str
    is_blocked: bool