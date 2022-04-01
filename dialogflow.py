import argparse
import logging
import json
from environs import Env
from google.cloud import dialogflow

logger = logging.getLogger('bot_logger')


def detect_intent_texts(project_id, session_id, texts, language_code='ru-RU'):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow.TextInput(
            text=text,
            language_code=language_code,
        )

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
    return response


def create_intent(project_id, display_name, training_phrases_parts, msg_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=msg_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main():
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(
        description='Загрузка тренировочных фраз для Dialogflow'
    )
    parser.add_argument('path', help='Путь к json-файлу')
    args = parser.parse_args()

    with open(args.path, 'r') as file:
        intents = json.load(file)

    for display_name, intent in intents.items():
        questions = intent['questions']
        answers = [intent['answer']]
        create_intent(
            env('DIALOGFLOW_PROJECT_ID'),
            display_name,
            questions,
            answers
        )


if __name__ == "__main__":
    main()
