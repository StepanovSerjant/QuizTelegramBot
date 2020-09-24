from aiogram import types
from aiogram.dispatcher.webhook import SendMessage

from loader import dp
from quiz.config import START, RESTART, INFO_MESSAGE
from quiz.logic import Player, Quiz


@dp.message_handler(commands=['start', 'help'])
async def quiz_info(message: types.Message):
    """ Обработка запроса на команды """
    # Regular request
    # await bot.send_message(message.chat.id, message.text)
    # or reply INTO webhook
    return SendMessage(message.chat.id, '\n'.join(INFO_MESSAGE))


@dp.message_handler(lambda message: message.text.lower() == RESTART)
async def quiz_restart(message: types.Message):
    """  Хендлер обработки запроса на рестарт викторины """
    current_game = Quiz()
    current_player = Player(message.chat.id)

    if current_game.check_player(message.chat.id):
        if len(current_player.all_answers()) != current_game.get_questions_count():
            text = 'Вы еще не завершили викторину, чтобы начать сначала :)'
            return SendMessage(message.chat.id, text)
        else:
            current_game.restart_player(message.chat.id) 
            q_id = current_player.get_q_id()
            buttons = current_game.create_buttons(q_id)
            return SendMessage(
                message.chat.id,
                current_game.get_question(q_id),
                reply_markup=buttons
            )
    else:
        text = [
            'Вы еще даже не проходили викторину.',
            'Как я начну еще раз?',
            f'<strong>Напишите мне лучше слово {start.capitalize()}!</strong>'
        ]
        return SendMessage(message.chat.id, '\n'.join(text))


@dp.message_handler(lambda message: message.text.lower() == START)
async def quiz_start(message: types.Message):
    """ Хендлер обработки запроса на старт викторины """
    current_game = Quiz()
    current_player = Player(message.chat.id)
    if not current_game.check_player(message.chat.id):
        current_game.create_player(message.chat.id)

    q_id = current_player.get_q_id()
    if q_id > current_game.get_questions_count():
        result = current_game.get_quiz_results(current_player.all_answers())
        return SendMessage(message.chat.id, current_game.result_answer(result))
        
    buttons = current_game.create_buttons(q_id)
    question = current_game.get_question(q_id)
    return SendMessage(
        message.chat.id, question,
        reply_markup=buttons
    )


@dp.message_handler(content_types=[
        types.ContentType.PHOTO,
        types.ContentType.DOCUMENT,
        types.ContentType.STICKER
    ])
async def quiz_file(message: types.Message):
    """ Хендлер обработки запроса с файлом """
    return SendMessage(message.chat.id, '\n'.join(INFO_MESSAGE))
