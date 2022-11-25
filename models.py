from datetime import datetime

from database import Base
from sqlalchemy import String, Integer, Boolean, Text, Column


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String, nullable=False, unique=True)
    is_blocked = Column(Boolean)
    faves_id_list = Column(String)
    date_created = datetime.datetime
    date_updated = datetime.datetime

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_nickname = Column(String, nullable=False, unique=True)
    date_created = datetime.date
    date_updated = datetime.date
    title = Column(String, nullable=False, unique=True)
    dish_type = Column(String, nullable=False)
    description = Column(Text)
    steps_to_complete = Column(Text)
    pictures = Column(String)
    likes = Column(Integer)
    tags = Column(String)
    is_blocked = Column(Boolean)