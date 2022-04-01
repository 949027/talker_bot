import logging
import telegram
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from environs import Env

from dialogflow import detect_intent_texts

env = Env()
env.read_env()

logger = logging.getLogger('bot_logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет, я бот! Поговори со мной!"
    )


def reply_to_message(update: Update, context: CallbackContext):
    project_id = env('DIALOGFLOW_PROJECT_ID')
    chat_id = update.effective_chat.id
    user_text = update.message.text
    response = detect_intent_texts(project_id, chat_id, [user_text])
    context.bot.send_message(
        chat_id=chat_id,
        text=response.query_result.fulfillment_text,
    )
    logger.info('Message send')


def catch_error(update: Update, context: CallbackContext):
    username = update.message.chat.username
    logger.exception(f'Ошибка от пользователя {username}')


def main():
    bot = telegram.Bot(token=env('TELEGRAM_TOKEN'))

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    error_handler = TelegramLogsHandler(bot, env('TELEGRAM_ID'))
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)

    updater = Updater(token=env('TELEGRAM_TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    answer_handler = MessageHandler(
        Filters.text & (~Filters.command),
        reply_to_message,
    )
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(answer_handler)
    dispatcher.add_error_handler(catch_error)

    updater.start_polling()


if __name__ == "__main__":
    main()
