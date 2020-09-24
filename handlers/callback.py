from aiogram import types
from aiogram.dispatcher.webhook import SendMessage

from loader import dp
from quiz.config import ALL_VARIABLES
from quiz.logic import Player, Quiz


@dp.callback_query_handler(lambda call: call.data in ALL_VARIABLES)
async def user_answer(call: types.CallbackQuery):
    """ Хендлер обработки нажатой кнопки """
    current_game = Quiz()
    current_player = Player(call.from_user.id)
    
    if len(current_player.all_answers()) == current_game.get_questions_count():
        result = current_game.get_quiz_results(current_player.all_answers())
        return SendMessage(call.from_user.id, current_game.result_answer(result))
        
    elif len(current_player.all_answers()) >= 0:
        if current_player.add_answer(call.data):
            q_id = current_player.get_q_id(add=True)
            text = current_game.get_question(q_id)
        else:
            q_id = current_player.get_q_id()
            text = '\n'.join([
                'Ая-яй! Вы уже ответили на этот вопрос :)',
                current_game.get_question(q_id)
            ])
        
        buttons = current_game.create_buttons(q_id)
        return SendMessage(
            call.from_user.id, text=text,
            reply_markup=buttons
        )
