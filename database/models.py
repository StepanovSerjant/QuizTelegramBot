from sqlalchemy import Boolean, Column, ForeignKey, String, Integer
from sqlalchemy.orm import backref, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Player(Base):
    __tablename__ = 'players'

    tg_id = Column(Integer, unique=True, primary_key=True, nullable=False)
    name = Column(String(80), nullable=True)
    current_question_id = Column(Integer, default=1)
    is_finished = Column(Boolean, default=False)

    def __str__(self) -> str:
        return f"<User(tg_id='{self.tg_id}', name='{self.name}', current_q_id='{self.current_q_id}', is_finished='{self.is_finished}')>"


class RightAnswer(Base):
    __tablename__ = 'right_answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    right_answer = Column(String, nullable=False)

    def __str__(self) -> str:
        return f"<RightAnswer(right_answer='{self.right_answer}')>"


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String, nullable=False)

    answer_id = Column(Integer, ForeignKey('right_answers.id'), nullable=False)
    answer = relationship('RightAnswer', backref=backref('answers', lazy=True))

    def __str__(self) -> str:
        return f"<Question(question='{self.question}')>"


class QuestionVariable(Base):
    __tablename__ = 'question_answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    variable = Column(String, nullable=False)

    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship('Question', backref=backref('questions', lazy=True))

    def __str__(self) -> str:
        return f"<Question(variable='{self.variable}')>"


class PlayerAnswer(Base):
    __tablename__ = 'players_answers'

    id = Column(Integer, primary_key=True, autoincrement=True)

    player_id = Column(Integer, ForeignKey('players.tg_id'), nullable=False)
    player = relationship('Player', backref=backref('players', lazy=True))

    answer_id = Column(Integer, ForeignKey('question_answers.id'), nullable=False)
    answer = relationship('QuestionVariable', backref=backref('variables', lazy=True))

    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    question = relationship('Question', backref=backref('questionss', lazy=True))

    def __str__(self) -> str:
        return f"<PlayerAnswer(player_id='{self.player_id}', answer='{self.answer}')>"
