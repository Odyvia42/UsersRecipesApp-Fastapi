

from fastapi import FastAPI
from pydantic import BaseModel



from starlette.responses import HTMLResponse

app = FastAPI()

class Author(BaseModel):
    id: int
    nickname: str
    is_blocked: bool
    faves_id_list: str
    date_created: str
    date_updated: str

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
    is_blocked: bool

    class Config:
        orm_mode = True


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