import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = '5000025980:AAEd8VB5A30jAC48vIaYQJIg3zup9q2GbqM'

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    # TODO: Add the option menu
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def register(update: Update, context: CallbackContext) -> None:
    """"""
    update.message.reply_text('register!')


def remove(update: Update, context: CallbackContext) -> None:
    """"""
    update.message.reply_text('remove!')


def invalid_message(update: Update, context: CallbackContext) -> None:
    """"""
    update.message.reply_text('This option is not valid, use /start to see the option menu.')


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Command handlers i.e. '/start'
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("register", register))
    dispatcher.add_handler(CommandHandler("remove", remove))

    # Message handlers
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, invalid_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()