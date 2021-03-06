import logging
import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
import telegram
from environs import Env

from dialogflow import detect_intent_texts
from telegram_handlers import TelegramLogsHandler

logger = logging.getLogger('bot_logger')


def main():
    env = Env()
    env.read_env()

    bot = telegram.Bot(token=env('TELEGRAM_TOKEN'))

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    error_handler = TelegramLogsHandler(bot, env('TELEGRAM_ID'))
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)

    vk_session = vk.VkApi(token=env('VK_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        try:
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                session_id = f'vk-{event.text}'
                response = detect_intent_texts(
                    env('DIALOGFLOW_PROJECT_ID'),
                    session_id,
                    [event.text]
                )
                if not response.query_result.intent.is_fallback:
                    vk_api.messages.send(
                        user_id=event.user_id,
                        message=response.query_result.fulfillment_text,
                        random_id=random.randint(1, 1000)
                    )
                    logger.info('Message send')
        except Exception as err:
            logger.exception(err)


if __name__ == "__main__":
    main()
