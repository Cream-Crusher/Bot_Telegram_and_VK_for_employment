import os
import json
import logging

from google.cloud import dialogflow
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv()
project_id = os.environ['PROJECT_ID']

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []

    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    logger.info("Intent created: {}".format(response))


def get_content(file_path):
    with open(file_path, 'r') as my_file:

        return json.loads(my_file.read())


if __name__ == '__main__':
    handler = RotatingFileHandler("app_log.log", maxBytes=20000, backupCount=2)
    logger.addHandler(handler)
    logger.info('Лог(и): create_intent\n'+'='*20)
    file_path = 'questions.json'
    intents = get_content(file_path)

    for display_name in intents:
        message_texts = []
        training_phrases_parts = intents[display_name]['questions']
        message_texts.append(intents[display_name]['answer'])
        create_intent(project_id, display_name, training_phrases_parts, message_texts)
