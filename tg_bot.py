import logging
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from environs import Env

from dialogflow import detect_intent_texts

env = Env()
env.read_env()


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет, я бот! Поговори со мной!"
    )


def to_answer(update: Update, context: CallbackContext):
    project_id = env('DIALOGFLOW_PROJECT_ID')
    chat_id = update.effective_chat.id
    user_text = update.message.text
    response = detect_intent_texts(project_id, chat_id, [user_text])
    context.bot.send_message(
        chat_id=chat_id,
        text=response.query_result.fulfillment_text,
    )
    logging.info('Message send')


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    updater = Updater(token=env('TELEGRAM_TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    answer_handler = MessageHandler(
        Filters.text & (~Filters.command),
        to_answer,
    )
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(answer_handler)

    updater.start_polling()


if __name__ == "__main__":
    main()
