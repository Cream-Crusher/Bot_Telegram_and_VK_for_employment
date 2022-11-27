import os
import vk_api
import random
import logging

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from dialogflow import get_detect_intent_message
from logging.handlers import RotatingFileHandler

load_dotenv()
vk_token = os.environ['VK_TOKEN']
project_id = os.environ['PROJECT_ID']
session_id = os.environ['SESSION_ID']
vk_session = vk_api.VkApi(token=vk_token)

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


if __name__ == '__main__':
    handler = RotatingFileHandler("app_log.log", maxBytes=20000, backupCount=2)
    logger.addHandler(handler)
    logger.info('Лог(и): vk\n'+'='*20)
    longpoll = VkLongPoll(vk_session)
    vk_api = vk_session.get_api()
    interception_of_messages(longpoll)
