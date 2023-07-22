import logging
import os
import time

import requests
from telegram import File, ReplyKeyboardMarkup, Update, User
from telegram.ext import CallbackContext

from exceptions import EmptySpeechError, NoTokenError, SpeechRecognizeError
from settings import (GPT, HOBBY, LOG_USER, LOVE_STORY, SCHOOL_PHOTO, SELFIE,
                      SQL_NOSQL)


def check_tokens(tokens: dict[str, dict]) -> None:
    for name, token in tokens.items():
        if not token:
            raise NoTokenError(f'{name} is not passed.')


def get_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=(
            (HOBBY, GPT),
            (SQL_NOSQL, LOVE_STORY),
            (SELFIE, SCHOOL_PHOTO)
        ),
        resize_keyboard=True
    )


def get_results(options: dict[str, str | int]) -> dict:
    endpoint = 'https://api.speechtext.ai/results?'

    while True:
        results = requests.get(endpoint, params=options).json()
        if results['status'] == 'failed':
            logging.warning('Speech wasn\'t recognized')
            break
        if results['status'] == 'finished':
            logging.info('Speech was recognized')
            break
        time.sleep(3)

    return results


def recognize_speech(speech: bytes) -> dict:
    endpoint = 'https://api.speechtext.ai/recognize?'
    headers = {'Content-Type': 'application/octet-stream'}
    secret_key = os.getenv('API_KEY')

    options = {
        'key': secret_key,
        'language': 'ru-RU',
        'format': 'ogg'
    }
    response = requests.post(
        data=speech,
        headers=headers,
        params=options,
        url=endpoint
    ).json()

    options = {
        'key': secret_key,
        'task': response['id'],
        'max_keywords': 10
    }

    return get_results(options)


def speech_to_str(update: Update, context: CallbackContext) -> str | None:
    """Returns None if message is empty or unknown, else returns message."""
    try:
        text: None | str = None
        user: User = update.message.from_user
        file: File = context.bot.get_file(update.message.voice.file_id)
        speech_bytes: bytes = file.download_as_bytearray()
        result: dict = recognize_speech(speech=speech_bytes)
        user_log = LOG_USER.format(user.username, user.id)

        if result.get('status', 'failed') == 'failed':
            raise SpeechRecognizeError('Не удалось распознать речь.')
        if not result.get('results', {}).get('transcript', ''):
            raise EmptySpeechError('Пустое голосовое сообщение.')
    except SpeechRecognizeError as error:
        logging.info(user_log + '\'s speech wasn\'t recognized.')
        update.message.reply_text(text=str(error))
    except EmptySpeechError as error:
        logging.info(user_log + '\'s speech is empty.')
        update.message.reply_text(text=str(error))
    else:
        logging.info(user_log + '\'s speech was recognized.')
    finally:
        return text
