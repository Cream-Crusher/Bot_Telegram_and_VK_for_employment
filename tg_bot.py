import os
import logging
import telegram
import argparse

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, Updater, CommandHandler, MessageHandler, Filters
from dialogflow import authenticate_implicit_with_adc, get_detect_intent_message
from logging.handlers import RotatingFileHandler

load_dotenv()

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")


def submit_a_reply(update: Update, context: CallbackContext):
    user_message = update.message.text
    intent_text, query_result = get_detect_intent_message(project_id, session_id, user_message)
    update.message.reply_text(intent_text)


def get_args():
    parser = argparse.ArgumentParser(description='Запуск телегарм бота')
    parser.add_argument('--tg_token', default=os.environ["TG_TOKEN"], help='Введите TG_TOKEN')
    parser.add_argument('--project_id', default=os.environ["PROJECT_ID"], help='Введите PROJECT_ID')
    parser.add_argument('--session_id', default=os.environ["SESSION_ID"], help='Введите SESSION_ID')
    parser.add_argument('--tg_chat_id', default=os.environ["TG_CHAT_ID"], help='Введите TG_CHAT_ID') 
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    tg_token = args.tg_token
    project_id = args.project_id
    session_id = args.session_id
    tg_chat_id = args.tg_chat_id
    handler = RotatingFileHandler("logs/tg_log.log", maxBytes=20000, backupCount=2)
    tg_bot = telegram.Bot(tg_token)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_chat_id))
    authenticate_implicit_with_adc(project_id)
    updater = Updater(token=tg_token)
    dispatcher = updater.dispatcher
    try:
        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, submit_a_reply))
        updater.start_polling()

    except Exception as err:
        logger.exception(err)
