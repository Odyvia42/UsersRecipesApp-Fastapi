
from pydantic import Field, EmailStr, BaseModel

from database import Base
from sqlalchemy import String, Integer, Boolean, Text, Column, ForeignKey
from sqlalchemy.orm import relationship

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String, nullable=False, unique=True)
    password = Column(String)
    is_blocked = Column(Boolean)
    faves_id_list = Column(String)
    date_created = Column(String)
    date_updated = Column(String)
    is_logged_in = Column(Boolean)
    recipes = relationship('Recipe', back_populates='author')


class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_nickname = Column(String, ForeignKey('authors.nickname'))
    date_created = Column(String)
    date_updated = Column(String)
    title = Column(String, nullable=False, unique=True)
    dish_type = Column(String, nullable=False)
    description = Column(Text)
    steps_to_complete = Column(Text)
    pictures = Column(String)
    likes = Column(Integer)
    tags = Column(String)
    is_blocked = Column(Boolean)

    author = relationship(Author, back_populates='recipes')




class PostSchema(BaseModel):
    id : int = Field(default=None)
    title : str = Field(default=None)
    content : str = Field(default=None)
    class Config:
        schema_extra = {
            "post_demo" : {
                "title" : "some title about animals",
                "content" : "some content about animals"
            }
        }

class UserSchema(BaseModel):
    username : str = Field(default=None)
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)
    class Config:
        the_schema = {
            "user_demo": {
                "name": "Bek",
                "email": "help@bekbrace.com",
                "password": "123"
            }
        }

class UserLoginSchema(BaseModel):
    username: str = Field(default=None)
    password : str = Field(default=None)
    class Config:
        the_schema = {
            "user_demo": {
                "email": "help@bekbrace.com",
                "password": "123"
            }
        }