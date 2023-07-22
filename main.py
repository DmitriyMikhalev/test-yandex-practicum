import logging
import os

from dotenv import load_dotenv
from telegram.ext import (CommandHandler, Dispatcher, Filters, MessageHandler,
                          Updater)

from callbacks import (actions_callback, echo, nextstep_callback,
                       repo_callback, start_callback, to_actions_callback)
from settings import TO_ACTIONS
from utils import check_tokens

load_dotenv()

BOT_TOKEN = os.getenv(key='BOT_TOKEN', default='')

logging.basicConfig(
    encoding='utf-8',
    filemode='w',
    filename='bot.log',
    format='{levelname} | {asctime} | {message} | {module} | {lineno}',
    level=logging.INFO,
    style='{'
)


def main() -> None:
    if not check_tokens({'bot': BOT_TOKEN}):
        raise Exception('Tokens are not passed.')

    bot = Updater(token=BOT_TOKEN)
    dispatcher: Dispatcher = bot.dispatcher

    dispatcher.add_handler(
        handler=CommandHandler(command='start', callback=start_callback)
    )
    dispatcher.add_handler(
        handler=CommandHandler(command='repo', callback=repo_callback)
    )
    dispatcher.add_handler(
        handler=MessageHandler(
            filters=Filters.regex(pattern=r'^/nextstep .+'),
            callback=nextstep_callback
        )
    )
    dispatcher.add_handler(
        handler=MessageHandler(
            filters=Filters.regex(pattern=TO_ACTIONS),
            callback=to_actions_callback
        )
    )
    dispatcher.add_handler(
        handler=MessageHandler(
            filters=Filters.text | Filters.voice,
            callback=actions_callback
        )
    )

    # unsupported messages including media, polls and other
    dispatcher.add_handler(
        handler=MessageHandler(filters=Filters.all, callback=echo)
    )

    bot.start_polling()
    logging.info('Bot has been started.')
    bot.idle()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(str(e) + '\nApp was closed.')
