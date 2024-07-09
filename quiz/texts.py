from quiz.config import QUESTIONS, START, RESTART
from quiz.services import get_all_variables

INFO_MESSAGE = [
    'Этот бот создан для того, чтоб узнать твои познания в области космонавтики.',
    f'Напиши мне слово <b>{START.capitalize()}</b>, и мы начнем :)',
    f'После прохождения викторины её можно начать заново с помощью команды - <b>{RESTART.capitalize()}</b>.'
]
ALL_VARIABLES = get_all_variables(QUESTIONS)
