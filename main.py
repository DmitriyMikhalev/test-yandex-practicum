import os

from dotenv import load_dotenv
from telegram.ext import (CommandHandler, Dispatcher, Filters, MessageHandler,
                          Updater)

from callbacks import help_callback, start_callback, text_callback

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')


def main() -> None:
    bot = Updater(token=BOT_TOKEN)
    dispatcher: Dispatcher = bot.dispatcher

    dispatcher.add_handler(
        handler=CommandHandler(command='start', callback=start_callback)
    )

    dispatcher.add_handler(
        handler=CommandHandler(command='help', callback=help_callback)
    )

    # any text
    dispatcher.add_handler(
        handler=MessageHandler(filters=Filters.text, callback=text_callback)
    )

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
