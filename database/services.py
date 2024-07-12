import quiz.config as cfg
from database.models import RightAnswer, Question, QuestionVariable
from database.settings import session


def set_new_quiz():
    """ Функция обновления БД для новой викторины """
    session.query(RightAnswer).delete()
    session.query(Question).delete()
    session.query(QuestionVariable).delete()
    session.commit()

    for _id in range(1, len(cfg.QUESTIONS) + 1):
        question_id = _id - 1

        current_question = cfg.QUESTIONS[question_id]['question']
        current_answer = cfg.QUESTIONS[question_id]['answer']
        
        right_answer = RightAnswer(right_answer=current_answer)
        question = Question(question=current_question, answer_id=_id)
        session.add(right_answer)
        session.add(question)
        session.commit()

        current_variables = cfg.QUESTIONS[question_id]['variables']
        for var in current_variables:
            session.add(QuestionVariable(variable=var, question_id=_id))
            session.commit()
