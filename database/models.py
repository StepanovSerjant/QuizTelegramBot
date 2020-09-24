from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Player(Base):
    """ Таблица игроков """
    __tablename__ = 'Players'

    tg_id = Column(Integer, unique=True, primary_key=True, nullable=True)
    name = Column(String(80), nullable=True)
    current_q_id = Column(Integer, default=1)  
    is_finished = Column(Boolean, default=False)

    def __repr__(self):
        return "<User(tg_id='%s', name='%s', current_q_id='%s, is_finished='%s')>" % (self.tg_id, self.name, self.current_q_id, self.is_finished)


class RightAnswer(Base):
    """ Таблица правильных ответов """
    __tablename__ = 'RightAnswers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    right_answer = Column(String, nullable=False)

    def __repr__(self):
        return "<RightAnswer(right_answer='%s')>" % (self.right_answer)


class Question(Base):
    """ Таблица вопросов """
    __tablename__ = 'Questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String, nullable=False)

    answer_id = Column(Integer, ForeignKey('RightAnswers.id'), nullable=False)
    answer = relationship('RightAnswer', backref=backref('answers', lazy=True))

    def __repr__(self):
        return "<Question(question='%s')>" % (self.question)


class QuestionVariable(Base):
    """ Таблица вариантов ответа """
    __tablename__ = 'QuestionAnswers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    variable = Column(String, nullable=False)

    q_id = Column(Integer, ForeignKey('Questions.id'), unique=False)
    q = relationship('Question', backref=backref('questions', lazy=True))

    def __repr__(self):
        return "<Question(variable='%s')>" % (self.variable)


class PlayerAnswer(Base):
    """ Таблица ответов игрока """
    __tablename__ = 'PlayersAnswers'

    id = Column(Integer, primary_key=True)

    player_id = Column(Integer, ForeignKey('Players.tg_id'), nullable=False)
    player = relationship('Player', backref=backref('players', lazy=True))

    answer_id = Column(Integer, ForeignKey('QuestionAnswers.id'), nullable=False)
    answer = relationship('QuestionVariable', backref=backref('variables', lazy=True))

    q_id = Column(Integer, ForeignKey('Questions.id'), nullable=False)
    q = relationship('Question', backref=backref('questionss', lazy=True))
