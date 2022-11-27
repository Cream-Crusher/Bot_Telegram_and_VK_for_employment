import os
import vk_api
import random
import logging
import argparse

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from dialogflow import get_detect_intent_message
from logging.handlers import RotatingFileHandler

load_dotenv()

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


def interception_of_messages(longpoll):

    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:
            logger.info('Новое сообщение:')

            if event.to_me:
                logger.info('Для меня от: {}'.format(event.peer_id))
                submit_a_reply(event, vk_api)
            else:
                logger.info('От меня для: {}'.format(event.peer_id))
            logger.info('Текст: {}'.format(event.text))


def submit_a_reply(event, vk_api):
    user_message = event.text
    intent_text, query_result = get_detect_intent_message(project_id, session_id, user_message)

    if query_result:
        logger.info('Требуется вмешательство поддержки. \nid пользователя: {}'.format(event.user_id))

    else:
        vk_api.messages.send(
            user_id=event.user_id,
            message=intent_text,
            random_id=random.randint(1, 1000)
        )


def get_args():
    parser = argparse.ArgumentParser(description='Запуск телегарм бота')
    parser.add_argument('--vk_token', default=os.environ["VK_TOKEN"], help='Введите VK_TOKEN')
    parser.add_argument('--project_id', default=os.environ["PROJECT_ID"], help='Введите PROJECT_ID')
    parser.add_argument('--session_id', default=os.environ["SESSION_ID"], help='Введите SESSION_ID')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    vk_token = args.vk_token
    project_id = args.project_id
    session_id = args.session_id
    vk_session = vk_api.VkApi(token=vk_token)
    handler = RotatingFileHandler("logs/vk_log.log", maxBytes=20000, backupCount=2)
    logger.addHandler(handler)
    longpoll = VkLongPoll(vk_session)
    vk_api = vk_session.get_api()
    try:
        interception_of_messages(longpoll)

    except Exception as err:
        logger.exception(err)
