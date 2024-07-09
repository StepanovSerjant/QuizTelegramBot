def create_db(new_quiz: bool = False) -> None:
    if not database_exists(engine.url):
        Base.metadata.create_all(engine)
        set_new_quiz()
    elif new_quiz:
        set_new_quiz()
