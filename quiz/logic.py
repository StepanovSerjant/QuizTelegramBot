from aiogram import types

import database.models as models
from database.settings import session
from quiz.config import FOR_RESULTS, RESTART


class Player:

    def __init__(self, tg_id):
        self.player_id = tg_id

    def add_answer(self, answer):
        """ Добавить ответ игрока в таблицу ответов всех игроков"""
        player_q_id = self.get_q_id()
        answer_q_id = session.query(models.QuestionVariable).filter_by(variable=answer).with_entities(models.QuestionVariable.q_id).all()
        answer_q_id = answer_q_id[0][0]

        if player_q_id == 1 or player_q_id == answer_q_id:
            answer_choice_id = session.query(models.QuestionVariable).filter_by(variable=answer).first()
            answer_choice_id = answer_choice_id.id

            answer = models.PlayerAnswer(player_id=self.player_id, answer_id=answer_choice_id, q_id=player_q_id)
            session.add(answer)
            session.commit()
            return True
        return False

    def all_answers(self):
        """ Получение всех ответов игрока """
        player_answers = session.query(models.PlayerAnswer).filter_by(player_id=self.player_id).all()
        player_answers = [player_answer.answer.variable for player_answer in player_answers]
        return player_answers

    def get_q_id(self, add=False):
        """ Получение айди вопроса, на котором остановился игрок """
 
        # player_q_id = session.query(models.Player).with_entities(models.Player.current_q_id).filter_by(tg_id=self.player_id).all()
        player_q_id = session.query(models.Player).with_entities(models.Player.current_q_id).filter_by(tg_id=self.player_id).all()
        player_q_id = player_q_id[0][0]

        if add:
            player_q_id += 1
            session.query(models.Player).filter_by(tg_id=self.player_id).update({'current_q_id': player_q_id})
            session.commit()
        return player_q_id


class Game:

    def check_player(self, id):
        """ Проверка существования игрока """
        player = session.query(models.Player).filter_by(tg_id=id).all()
        if not player:
            return False
        return True

    def create_player(self, id, name=None):
        """ Создание игрока """
        if name != None:
            new_player = models.Player(tg_id=id, name=name)
        else:
            new_player = models.Player(tg_id=id)
        session.add(new_player)
        session.commit()

    def set_finish_status(self, id, is_finished=True):
        """ Установка игроку значение поля finished """
        session.query(models.Player).filter_by(tg_id=id).update({'is_finished': is_finished})
        session.commit()

    def restart_player(self, id):
        """ Рестарт игрока """
        player_answers = session.query(models.PlayerAnswer).filter_by(player_id=id).all()
        for answer in player_answers:
            session.delete(answer)
        self.set_finish_status(id, False)
        session.query(models.Player).filter_by(tg_id=id).update({'current_q_id': 1})
        session.commit()


class Quiz(Game):

    def get_question(self, q_id):
        """ Получение текста текущего вопроса """
        question = session.query(models.Question).filter_by(id=q_id).all()
        return question[0].question

    def get_question_variables(self, q_id):
        """ Получение вариантов ответа для текущего вопроса """
        variables = session.query(models.QuestionVariable).filter_by(q_id=q_id).all()
        variables = [variable.variable for variable in variables]
        return variables

    def get_questions_count(self):
        """ Получение общего числа всех вопросов """
        questions = session.query(models.Question).all()
        return len(questions)

    def get_right_answers(self):
        """ Получение всех правильных ответов викторины """
        right_answers = session.query(models.RightAnswer).all()
        return [right_answer.right_answer for right_answer in right_answers]

    def get_quiz_results(self, answs):
        """ Получение процента правильных ответов и соответствующего текста """
        right_answers = self.get_right_answers()
        player_answers = len(right_answers) - len(list(set(right_answers) - set(answs)))
        percent = (player_answers / len(right_answers)) * 100

        if percent >= 90:
            text_result = FOR_RESULTS[0]
        elif percent >= 70:
            text_result = FOR_RESULTS[1]
        elif percent >= 50:
            text_result = FOR_RESULTS[2]
        else:
            text_result = FOR_RESULTS[3]

        return (percent, text_result)

    def make_keyboard(self, question_id):
        """ Функция генерации клавиатуры для ответа пользователю """
        buttons = []
        for variable in self.get_question_variables(question_id):
            button = [{
                'text': variable,
                'callback_data': variable
            }]
            buttons.append(button)

        inline_keyboard = {'inline_keyboard': buttons}
        return inline_keyboard

    def create_buttons(self, question_id):
        keyboard = self.make_keyboard(question_id)
        buttons = types.InlineKeyboardMarkup()
        for button in keyboard['inline_keyboard']:
            buttons.add(
                types.InlineKeyboardButton(button[0]['text'],
                callback_data = button[0]['callback_data'])
            )
        return buttons

    def result_answer(self, result_list):
        """ Функция формирования текста результатов для ответа пользователю """
        percent, text_result = result_list
        text = [
            '<i>Викторина окончена :(</i>',
            f'Процент правильных ответов: <b>{percent}%</b>',
            f'<strong>{text_result}</strong>',
            'Кстати, мы можем начать сначала, если хочешь :)',
            f'Напиши мне: <em>"{RESTART.capitalize()}"</em>!'
        ]
        return '\n'.join(text)
