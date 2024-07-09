from sqlalchemy_utils import database_exists

from database.models import Base
from database.services import set_new_quiz
from database.settings import engine


def create_db(new_quiz: bool = False) -> None:
    if not database_exists(engine.url):
        Base.metadata.create_all(engine)
        set_new_quiz()
    elif new_quiz:
        set_new_quiz()
