import logging
import os

from dotenv import load_dotenv
from telegram.ext import (CommandHandler, Dispatcher, Filters, MessageHandler,
                          Updater)

from callbacks import (actions_callback, echo, nextstep_callback,
                       repo_callback, start_callback, to_actions_callback)
from exceptions import NoTokenError
from settings import TO_ACTIONS
from utils import check_tokens

env_file = os.path.join(os.getcwd(), 'infra', '.env')

load_dotenv(dotenv_path=env_file)

API_KEY = os.getenv(key='API_KEY', default='')
BOT_TOKEN = os.getenv(key='BOT_TOKEN', default='')
GITHUB_LINK = os.getenv(key='GITHUB_LINK', default='')
OWNER_CHAT_ID = os.getenv(key='OWNER_CHAT_ID', default='')

tokens = {
    'API_KEY': API_KEY,
    'BOT_TOKEN': BOT_TOKEN,
    'GITHUB_LINK': GITHUB_LINK,
    'OWNER_CHAT_ID': OWNER_CHAT_ID
}

logging.basicConfig(
    encoding='utf-8',
    filemode='w',
    filename='bot.log',
    format='{levelname} | {asctime} | {message} | {module} | {lineno}',
    level=logging.INFO,
    style='{'
)


def main() -> None:
    check_tokens(tokens)

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
            filters=Filters.regex(pattern=r'/nextstep[.]*'),
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
    except NoTokenError as error:
        logging.error(msg=str(error))
    except Exception as error:
        logging.error(msg=f'Unexpected error: {error}')
