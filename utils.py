import logging
import os
import time

import requests
from telegram import Bot, File, ReplyKeyboardMarkup, Voice

from exceptions import EmptySpeechError, SpeechRecognizeError
from settings import GPT, HOBBY, LOVE_STORY, SCHOOL_PHOTO, SELFIE, SQL_NOSQL


def check_tokens(tokens: dict[str, str]) -> bool:
    for name, token in tokens.items():
        if not token:
            logging.ERROR(f'Token {name} is empty.')
            return False

    return True


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
    secret_key = os.getenv('SPEECH_KEY')

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


def speech_to_str(
    bot: Bot,
    voice_file: Voice
) -> str:
    file: File = bot.get_file(voice_file.file_id)
    speech_bytes: bytes = file.download_as_bytearray()
    result: dict = recognize_speech(speech=speech_bytes)

    if result.get('status', 'failed') == 'failed':
        raise SpeechRecognizeError('Не удалось распознать речь.')

    # empty speech message
    if not (text := result.get('results', {}).get('transcript', '')):
        raise EmptySpeechError('Пустое голосовое сообщение.')

    return text
