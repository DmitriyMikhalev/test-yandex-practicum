import logging

from telegram import Update
from telegram.ext import CallbackContext

from settings import LOG_USER


def log_callback(callable):
    def _wrapper(update: Update, context: CallbackContext):
        user = update.message.from_user
        logging.info(
            'Start dialog with' +
            LOG_USER.format(user.username, user.id) +
            f'using {callable.__name__}.'
        )
        return callable(context=context, update=update)
    return _wrapper
