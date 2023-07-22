import logging
import os

from telegram import ParseMode, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.update import Update

from exceptions import EmptySpeechError, SpeechRecognizeError
from question import Question
from settings import (ACTIONS, HOBBY_ANSWER, QR_CAPTION, START_MESSAGE,
                      TO_ACTIONS)
from utils import get_keyboard, speech_to_str


def actions_callback(update: Update, context: CallbackContext) -> None:
    text: str | None = update.message.text

    if (voice_file := update.message.voice) is not None:
        try:
            text: str = speech_to_str(bot=context.bot, voice_file=voice_file)
        except SpeechRecognizeError as error:
            logging.error('Speech wasn\'t recognized.')
            update.message.reply_text(text=str(error))
            return
        except EmptySpeechError as error:
            logging.info('Speech is empty.')
            update.message.reply_text(text=str(error))
            return
        else:
            logging.debug('Speech was recognized.')

    match text.lower():
        case Question.HOBBY:
            update.message.reply_text(text=HOBBY_ANSWER)
        case Question.LOVE_STORY:
            update.message.reply_text(text='love is..')
        case Question.SELFIE:
            update.message.reply_text(text='selfie..')
        case Question.SCHOOL_PHOTO:
            update.message.reply_text(text='school photo..')
        case Question.SQL_NOSQL | Question.SQL_ALIAS:
            update.message.reply_text(text='sql vs nosql..')
        case Question.GPT | Question.GPT_ALIAS:
            update.message.reply_text(text='GPT is..')
        case _:
            echo(context=context, update=update)


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text='Я не умею отвечать на такие сообщения :('
    )


def nextstep_callback(update: Update, context: CallbackContext) -> None:
    owner_id = os.getenv('OWNER_CHAT_ID')
    msg = update.message.text.removeprefix('/nextstep ')
    sender = update.message.from_user

    context.bot.send_message(
        chat_id=owner_id,
        text=f'Message from @{sender.username} ({sender.full_name})\n - {msg}'
    )
    update.message.reply_text(text='Сообщение доставлено автору!')


def repo_callback(update: Update, context: CallbackContext) -> None:
    file_path = os.path.join(os.getcwd(), 'media', 'clck.jpg')
    update.message.reply_photo(
        caption=QR_CAPTION.format(os.getenv('GITHUB_LINK')),
        parse_mode=ParseMode.HTML,
        photo=open(file=file_path, mode='rb')
    )


def start_callback(update: Update, context: CallbackContext) -> None:
    keyboard = ReplyKeyboardMarkup(
        keyboard=(
            (TO_ACTIONS,),
        ),
        resize_keyboard=True
    )
    update.message.reply_text(
        reply_markup=keyboard,
        text=START_MESSAGE.format(update.effective_chat.first_name)
    )


def to_actions_callback(update: Update, context: CallbackContext) -> None:
    keyboard = get_keyboard()
    update.message.reply_text(
        reply_markup=keyboard,
        text=ACTIONS
    )
