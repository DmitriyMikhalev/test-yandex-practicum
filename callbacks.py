import os

from telegram import ParseMode, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.update import Update

from settings import (GPT, HOBBY, HOBBY_ANSWER, LOVE_STORY, GPT_ALIAS,
                      SCHOOL_PHOTO, SELFIE, SQL_NOSQL, SQL_ALIAS,
                      TO_ACTIONS, ACTIONS, QR_CAPTION, START_MESSAGE)
from utils import get_keyboard, recognize_speech


def actions_callback(update: Update, context: CallbackContext) -> None:
    text = update.message.text

    if text is None:
        file = context.bot.get_file(update.message.voice.file_id)
        speech_bytes: bytes = file.download_as_bytearray()
        result = recognize_speech(speech=speech_bytes)

        if result.get('status', 'failed') == 'failed':
            update.message.reply_text(
                text='К сожалению, я не смог распознать речь :('
            )
            return

        text = result.get('results', {}).get('transcript', {})

    if text.lower() == HOBBY.lower():
        update.message.reply_text(
            text=HOBBY_ANSWER
        )
    elif text.lower() == LOVE_STORY.lower():
        update.message.reply_text(
            text='love is..'
        )
    elif text.lower() in (SQL_NOSQL.lower(), SQL_ALIAS):
        update.message.reply_text(
            text='sql vs nosql..'
        )
    elif text.lower() in (GPT.lower(), GPT_ALIAS):
        update.message.reply_text(
            text='GPT is..'
        )
    elif text.lower() == SELFIE.lower():
        update.message.reply_text(
            text='selfie..'
        )
    elif text.lower() == SCHOOL_PHOTO.lower():
        update.message.reply_text(
            text='school photo..'
        )


def to_actions_callback(update: Update, context: CallbackContext) -> None:
    keyboard = get_keyboard()
    update.message.reply_text(
        text=ACTIONS,
        reply_markup=keyboard
    )


def start_callback(update: Update, context: CallbackContext) -> None:
    keyboard = ReplyKeyboardMarkup(
        keyboard=(
            (TO_ACTIONS,),
        ),
        resize_keyboard=True
    )
    update.message.reply_text(
        text=START_MESSAGE.format(update.effective_chat.first_name),
        reply_markup=keyboard
    )


def repo_callback(update: Update, context: CallbackContext) -> None:
    file_path = os.path.join(os.getcwd(), 'media', 'clck.jpg')
    update.message.reply_photo(
        photo=open(file=file_path, mode='rb'),
        caption=QR_CAPTION.format(os.getenv('GITHUB_LINK')),
        parse_mode=ParseMode.HTML
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


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text='uknown')
