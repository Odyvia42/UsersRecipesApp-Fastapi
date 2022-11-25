import datetime
from typing import List

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from starlette.responses import HTMLResponse
from database import SessionLocal
import models

app = FastAPI()


class Author(BaseModel):
    id: int
    nickname: str
    is_blocked: bool = False
    faves_id_list: str = ''
    date_created: str = datetime.datetime.utcnow()
    date_updated: str = datetime.datetime.utcnow()

    class Config:
        orm_mode = True


class Recipe(BaseModel):
    id: int
    author_nickname: str
    date_created: str
    date_updated: str
    title: str
    dish_type: str
    description: str
    steps_to_complete: str
    pictures: str
    likes: int
    tags: str
    is_blocked: bool = False

    class Config:
        orm_mode = True


db = SessionLocal()


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <head>
            <title>Сервис пользовательских рецептов</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """


@app.get('/authors', response_model=List[Author], status_code=status.HTTP_200_OK)
async def get_all_authors():
    authors = db.query(models.Author).all()
    return authors


@app.get('/author/{author_id}', response_model=Author, status_code=status.HTTP_200_OK)
async def get_author(author_id: int):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    return author


@app.post('/authors', response_model=Author,
          status_code=status.HTTP_201_CREATED)
async def create_author(author: Author):
    db_author = db.query(models.Author).filter(models.Author.nickname == author.nickname).first()
    if db_author is not None:
        raise HTTPException(status_code=400, detail="This nickname already exists")

    new_author = models.Author(
        id=author.id,
        nickname=author.nickname,
        is_blocked=author.is_blocked,
        faves_id_list=author.faves_id_list,
        date_created=author.date_created,
        date_updated=author.date_updated,
    )

    db.add(new_author)
    db.commit()

    return new_author


@app.put('/author/{author_id}', response_model=Author, status_code=status.HTTP_200_OK)
async def update_author(author_id: int, author: Author):
    author_to_update = db.query(models.Author).filter(models.Author.id == author_id).first()
    author_to_update.nickname = author.nickname,
    author_to_update.faves_id_list = author.faves_id_list,
    author_to_update.date_created = author.date_created,
    author_to_update.date_updated = author.date_updated,

    db.commit()

    return author_to_update


@app.delete('/author/{author_id}')
async def delete_author(author_id: int):
    author_to_delete = db.query(models.Author).filter(models.Author.id == author_id).first()

    if author_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

    db.delete(author_to_delete)
    db.commit()

    return author_to_delete
