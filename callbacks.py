import os

from telegram import ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.update import Update
from telegram import ParseMode

from settings import (ACTIONS, HELP_MESSAGE, SOURCE_CODE, SOURCE_CODE_ANSWER,
                      START_MESSAGE)


def start_callback(update: Update, context: CallbackContext) -> None:
    keyboard = ReplyKeyboardMarkup(
        keyboard=(
            (SOURCE_CODE, ACTIONS),
        ),
        resize_keyboard=True
    )
    update.message.reply_text(
        text=START_MESSAGE.format(update.effective_chat.first_name),
        reply_markup=keyboard
    )


def help_callback(update: Update, context: CallbackContext) -> None:
    # keyboard = ...
    update.message.reply_text(text=HELP_MESSAGE)


def text_callback(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text.lower()

    if user_text == SOURCE_CODE.lower():
        update.message.reply_text(
            text=SOURCE_CODE_ANSWER.format(os.getenv('GITHUB_LINK'))
        )
    elif user_text == ACTIONS.lower():
        text_answer = HELP_MESSAGE
        update.message.reply_text(
            text=text_answer,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    else:
        update.message.reply_text('unknown')
