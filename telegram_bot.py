import requests
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from config import HOME_PAGE

TOKEN = '5000025980:AAEd8VB5A30jAC48vIaYQJIg3zup9q2GbqM'


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
        "\n<user-name> in smart pooling system"
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


def answer(update: Update, context: CallbackContext) -> None:
    msg = update.message
    if len(msg.text.split(' ')) < 3:
        msg.reply_text("You need to specify an answer and a poll")
        return
    response = requests.get(
        url=HOME_PAGE + 'answer',
        params={
            'answer': msg.text.split(' ')[1],
            'poll': msg.text.split(' ')[2],
            'chat_id': msg.chat.id
        }
    )
    update.message.reply_text(response.text)


def broadcast_poll(recipients: list, poll_content, poll_answers):
    for recip in recipients:
        send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' \
                                                + recip + '&parse_mode=Markdown&text=' + poll_content + poll_answers
        requests.get(send_text)


def invalid_message(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('This option is not valid.\n'
                              'use /start to see the option menu.')


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

    dispatcher.add_handler(CommandHandler("answer", answer))

    # Message handlers
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, invalid_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # TODO: maybe fix it
    # updater.idle()


if __name__ == '__main__':
    run_telegram_bot()
