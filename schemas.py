from pydantic import BaseModel, Field
import datetime


class Author(BaseModel):
    id: int
    nickname: str
    faves_id_list: str | None = None

    class Config:
        orm_mode = True


class AuthorIn(BaseModel):
    nickname: str
    password: str
    date_created: str = datetime.datetime.utcnow()
    faves_id_list: str | None = None


class Recipe(BaseModel):
    id: int
    author_nickname: str
    title: str
    dish_type: str
    description: str
    steps_to_complete: str
    pictures: str
    likes: int = 0
    tags: str

    class Config:
        orm_mode = True


class RecipeIn(BaseModel):
    author_nickname: str
    title: str
    dish_type: str
    description: str
    steps_to_complete: str
    pictures: str
    likes: int = 0
    tags: str
    date_created = datetime.datetime.utcnow()
    date_updated = datetime.datetime.utcnow()


class RecipeUpdate(BaseModel):
    title: str
    dish_type: str
    description: str
    steps_to_complete: str
    pictures: str
    tags: str
    date_updated = datetime.datetime.utcnow()


class RecipeOut(Recipe):
    date_created: str
    date_updated: str


class AdminSchema(BaseModel):
    username: str = Field(default=None)
    password: str = Field(default=None)

    class Config:
        the_schema = {
            "user_demo": {
                "name": "Bek",
                "password": "123"
            }
        }


class AdminLoginSchema(BaseModel):
    username: str = Field(default=None)
    password: str = Field(default=None)

    class Config:
        the_schema = {
            "user_demo": {
                "username": "help_bek",
                "password": "123"
            }
        }
