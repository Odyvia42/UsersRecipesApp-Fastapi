from database import Base, engine
from models import Author, Recipe


Base.metadata.create_all(engine)
