import logging

from google.cloud import dialogflow, storage

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


def authenticate_implicit_with_adc(project_id):
    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()
    for bucket in buckets:
        logger.info(bucket.name)
    logger.info("Listed all storage buckets.")


def get_detect_intent_message(project_id, session_id, user_message, language_code='ru'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=user_message, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text, response.query_result.intent.is_fallback
