import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, Updater, CommandHandler, MessageHandler, Filters
from dialogflow import authenticate_implicit_with_adc, get_detect_intent_message
from logging.handlers import RotatingFileHandler

load_dotenv()
tg_token = os.environ['TG_TOKEN']
project_id = os.environ['PROJECT_ID']
session_id = os.environ['SESSION_ID']

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")


def submit_a_reply(update: Update, context: CallbackContext):
    user_message = update.message.text
    intent_text, query_result = get_detect_intent_message(project_id, session_id, user_message)
    update.message.reply_text(intent_text)
    logger.info('Бот отправил обработанный ответ')


if __name__ == '__main__':
    handler = RotatingFileHandler("app_log.log", maxBytes=20000, backupCount=2)
    logger.addHandler(handler)
    logger.info('Лог(и): tg\n'+'='*20)
    authenticate_implicit_with_adc(project_id)
    updater = Updater(token=tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, submit_a_reply))
    updater.start_polling()
