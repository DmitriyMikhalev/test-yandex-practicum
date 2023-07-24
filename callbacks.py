import os

from telegram import ParseMode, ReplyKeyboardMarkup, User
from telegram.ext import CallbackContext
from telegram.update import Update

from decorators import log_callback
from question import Question
from settings import (ACTIONS, HOBBY_ANSWER, LOG_USER, QR_CAPTION,
                      START_MESSAGE, TO_ACTIONS)
from utils import get_keyboard, speech_to_str, get_file_bytes


@log_callback
def actions_callback(update: Update, context: CallbackContext) -> None:
    msg: str | None = update.message.text

    if update.message.voice is not None:
        if (msg := speech_to_str(context=context, update=update)) is None:
            return

    match msg.lower():
        case Question.HOBBY:
            update.message.reply_text(text=HOBBY_ANSWER)
        case Question.LOVE_STORY:
            audio = get_file_bytes(filename='love.ogg')
            update.message.reply_voice(voice=audio)
        case Question.SELFIE:
            photo = get_file_bytes(filename='selfie.jpg')
            update.message.reply_photo(photo=photo)
        case Question.SCHOOL_PHOTO:
            photo = get_file_bytes(filename='high-school.jpg')
            update.message.reply_photo(photo=photo)
        case Question.SQL_NOSQL | Question.SQL_ALIAS:
            audio = get_file_bytes(filename='sql-nosql.ogg')
            update.message.reply_voice(voice=audio)
        case Question.GPT | Question.GPT_ALIAS:
            audio = get_file_bytes(filename='gpt.ogg')
            update.message.reply_voice(voice=audio)
        case _:
            if msg.startswith('/nextstep'):
                nextstep_callback(context=context, update=update)
            else:
                echo(context=context, update=update)


@log_callback
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text='Я не умею отвечать на такие сообщения :('
    )


@log_callback
def nextstep_callback(update: Update, context: CallbackContext) -> None:
    owner_id = os.getenv('OWNER_CHAT_ID')
    msg: str = update.message.text.removeprefix('/nextstep')
    sender: User = update.message.from_user

    # empty message
    if msg == '':
        return echo(context=context, update=update)

    context.bot.send_message(
        chat_id=owner_id,
        text='Message from ' +
             LOG_USER.format(sender.username, sender.id) +
             f'\n -{msg}'
    )
    update.message.reply_text(text='Сообщение доставлено автору!')


@log_callback
def repo_callback(update: Update, context: CallbackContext) -> None:
    file_path = os.path.join(os.getcwd(), 'media', 'clck.jpg')
    update.message.reply_photo(
        caption=QR_CAPTION.format(os.getenv('GITHUB_LINK')),
        parse_mode=ParseMode.HTML,
        photo=open(file=file_path, mode='rb')
    )


@log_callback
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


@log_callback
def to_actions_callback(update: Update, context: CallbackContext) -> None:
    keyboard: ReplyKeyboardMarkup = get_keyboard()
    update.message.reply_text(
        reply_markup=keyboard,
        text=ACTIONS
    )
