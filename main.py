import datetime
from typing import List
from fastapi import FastAPI, status, HTTPException, Request, Form, Depends, Body
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from starlette.responses import HTMLResponse

from app.auth.jwt_bearer import jwtBearer
from app.auth.jwt_handler import signJWT
from database import SessionLocal
import models
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


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
    date_created: str = datetime.datetime.utcnow()
    date_updated: str = datetime.datetime.utcnow()
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

admins = [{
      "username": "alexander_laggard",
      "password": "cookedallthemdishes"
    }]

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )


@app.get('/authors', response_model=List[Author], status_code=status.HTTP_200_OK)
async def get_all_authors():
    authors = db.query(models.Author).all()
    return authors


@app.get('/authors/{author_id}', response_model=Author, status_code=status.HTTP_200_OK)
async def get_author_by_id(author_id: int):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    return author



@app.post('/authors', response_model=Author,
          status_code=status.HTTP_201_CREATED)
async def create_author(author: AuthorIn):
    db_author = db.query(models.Author).filter(models.Author.nickname == author.nickname).first()
    if db_author is not None:
        raise HTTPException(status_code=400, detail="This nickname already exists")

    new_author = models.Author(

        nickname=author.nickname,
        password=author.password,

    )

    db.add(new_author)
    db.commit()

    return new_author


@app.put('/authors/{author_id}', response_model=Author, status_code=status.HTTP_200_OK)
async def update_author(author_id: int, author: AuthorIn):
    author_to_update = db.query(models.Author).filter(models.Author.id == author_id).first()
    author_to_update.nickname = author.nickname,
    author_to_update.password = author.password
    author_to_update.faves_id_list = author.faves_id_list,


    db.commit()

    return author_to_update


@app.delete('/authors/{author_id}', dependencies=[Depends(jwtBearer())])
async def delete_author(author_id: int):
    author_to_delete = db.query(models.Author).filter(models.Author.id == author_id).first()

    if author_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

    db.delete(author_to_delete)
    db.commit()

    return author_to_delete


@app.get('/recipes', response_model=List[Recipe], status_code=status.HTTP_200_OK)
async def get_all_recipes():
    recipes = db.query(models.Recipe).all()
    return recipes


@app.get('/recipes/{recipe_id}', response_model=Recipe, status_code=status.HTTP_200_OK)
async def get_recipe(recipe_id: int):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    return recipe


@app.post('/recipes', response_model=Recipe,
          status_code=status.HTTP_201_CREATED)
async def create_recipe(recipe: Recipe):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.title == recipe.title).first()
    if db_recipe is not None:
        raise HTTPException(status_code=400, detail="This recipe already exists")

    new_recipe = models.Recipe(
        id=recipe.id,
        author_nickname=recipe.author_nickname,
        date_created=recipe.date_created,
        date_updated=recipe.date_updated,
        title=recipe.title,
        dish_type=recipe.dish_type,
        description=recipe.description,
        steps_to_complete=recipe.steps_to_complete,
        pictures=recipe.pictures,
        likes=recipe.likes,
        tags=recipe.tags,
        is_blocked=recipe.is_blocked,

    )

    db.add(new_recipe)
    db.commit()

    return new_recipe


@app.put('/recipes/{recipe_id}', response_model=Recipe, status_code=status.HTTP_200_OK)
async def update_recipe(recipe_id: int, recipe: Recipe):
    recipe_to_update = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    recipe_to_update.author_nickname = recipe.author_nickname,
    recipe_to_update.date_updated = recipe.date_updated,
    recipe_to_update.title = recipe.title,
    recipe_to_update.dish_type = recipe.dish_type,
    recipe_to_update.description = recipe.description,
    recipe_to_update.steps_to_complete = recipe.steps_to_complete,
    recipe_to_update.pictures = recipe.pictures,
    recipe_to_update.likes = recipe.likes,
    recipe_to_update.tags = recipe.tags,

    db.commit()

    return recipe_to_update


@app.delete('/recipes/{recipe_id}')
async def delete_recipe(recipe_id: int):
    recipe_to_delete = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

    if recipe_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe Not Found")

    db.delete(recipe_to_delete)
    db.commit()

    return recipe_to_delete


@app.post('/posts', dependencies=[Depends(jwtBearer())], tags=['posts'])
def add_post(post: models.PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "info": "Post Added!"
    }


@app.post('/user/signup', tags=['user'])
def user_signup(user: models.AdminSchema = Body(default=None)):
    admins.append(user)
    return signJWT(user.email), admins

def check_user(data: models.AdminLoginSchema):
    for user in admins:
        if user.get("username") == data.username and user.get("password") == data.password:
            return True
        return False


@app.post('/user/login', tags=['user'])
def user_login(user: models.AdminLoginSchema = Body(default=None)):
    print(admins)
    if check_user(user):
        return signJWT(user.username)
    else:
        return {
            "error": "Invalid login details!"
        }
