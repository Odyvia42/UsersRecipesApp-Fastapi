from sqlalchemy import String, Integer, Boolean, Text, Column, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


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
