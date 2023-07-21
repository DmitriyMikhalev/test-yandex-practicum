import logging
import os
import time

import requests
from telegram import ReplyKeyboardMarkup

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


def get_results(options):
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
    secret_key = os.getenv('SPEECH_KEY')
    endpoint = 'https://api.speechtext.ai/recognize?'
    headers = {'Content-Type': 'application/octet-stream'}

    options = {
        'key': secret_key,
        'language': 'ru-RU',
        'format': 'ogg'
    }
    response = requests.post(
        endpoint,
        headers=headers,
        params=options,
        data=speech
    ).json()

    options = {
        'key': secret_key,
        'task': response['id'],
        'max_keywords': 10
    }

    return get_results(options)
