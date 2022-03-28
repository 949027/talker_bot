import logging
import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env

from dialogflow import detect_intent_texts


def main():
    env = Env()
    env.read_env()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    vk_session = vk.VkApi(token=env('VK_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            response = detect_intent_texts(
                env('DIALOGFLOW_PROJECT_ID'),
                event.user_id,
                [event.text]
            )
            if not response.query_result.intent.is_fallback:
                vk_api.messages.send(
                    user_id=event.user_id,
                    message=response.query_result.fulfillment_text,
                    random_id=random.randint(1, 1000)
                )
                logging.info('Message send')


if __name__ == "__main__":
    main()
