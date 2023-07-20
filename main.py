import os

from dotenv import load_dotenv
from telegram.ext import CallbackContext, CommandHandler, Updater
from telegram.update import Update

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')


def echo(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='echo'
    )


def main() -> None:
    bot = Updater(token=BOT_TOKEN)
    bot.dispatcher.add_handler(
        handler=CommandHandler(command='start', callback=echo)
    )

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
