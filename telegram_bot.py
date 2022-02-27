import requests
import telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

from config import HOME_PAGE

# TOKEN = '5000025980:AAEd8VB5A30jAC48vIaYQJIg3zup9q2GbqM'  # - old
TOKEN = '5157669737:AAFMJcwpoL_QM7LN5_RY8UaPPbr1TYiPzPk'    # new
bot = telegram.Bot(token=TOKEN)


# Define a few command handlers
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hello {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )
    update.message.reply_text("Welcome to smart polling\nPlease choose one of the options:")
    update.message.reply_text(
        "/register <user-name> - Register to start answer polls via telegram"
        "\n<user-name> in smart polling system"
        "\n"
        "\n/remove <user-name> - To stop getting polls queries"
        "\n<user-name> in smart polling system"
        "\n"
        "\n/start - Use start anytime to see this menu again"
    )


def register(update: Update, context: CallbackContext) -> None:
    msg = update.message
    if len(msg.text.split(' ')) == 1:
        msg.reply_text("You need to provide the username to register")
        return
    response = requests.get(
        url=HOME_PAGE + 'register',
        params={
            'username': msg.text.split(' ')[1],
            'chat_id': msg.chat.id
        }
    )
    update.message.reply_text(response.text)


def remove(update: Update, context: CallbackContext) -> None:
    msg = update.message
    if len(msg.text.split(' ')) == 1:
        msg.reply_text("You need to provide the username to remove")
        return
    response = requests.get(
        url=HOME_PAGE + 'remove',
        params={
            'username': msg.text.split(' ')[1],
            'chat_id': msg.chat.id
        }
    )
    update.message.reply_text(response.text)


def broadcast_poll(recipients: list, poll_id, poll_content, poll_answers):
    for recip in recipients:

        bot.sendPoll(chat_id=recip, id=poll_id, question=poll_content, options=poll_answers,
                     allows_multiple_answers=False, type=telegram.constants.POLL_REGULAR, )


def invalid_message(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('This option is not valid.\n'
                              'use /start to see the option menu.')


def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()
    if len(query.split(' ')) < 3:
        update.message.reply_text("You need to specify an answer and a poll")
        return
    response = requests.get(
        url=HOME_PAGE + 'answer',
        params={
            'answer': query.split(' ')[1],
            'poll': query.split(' ')[2],
            'chat_id': update.effective_chat.id
        }
    )
    update.effective_message.reply_text(response.text)


def run_telegram_bot() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Command handlers i.e. '/start'
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("register", register))
    dispatcher.add_handler(CommandHandler("remove", remove))

    dispatcher.add_handler(CallbackQueryHandler(queryHandler))

    # Message handlers
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, invalid_message))

    # Start the Bot
    updater.start_polling()


if __name__ == '__main__':
    run_telegram_bot()
