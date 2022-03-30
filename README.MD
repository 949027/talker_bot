# Боты-помощники
отвечают пользователю на распространенные вопросы в телеграме и вконтакте 

### Что необходимо
1. Python3 должен быть уже установлен. 
2. Рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html) для изоляции проекта.
3. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```python
pip install -r requirements.txt
```
4. Создайте файл `.env` и пропишите в нем переменные окружения:
- `TELEGRAM_ID` - id пользователя в телеграме, которому направлять логи;
- `TELEGRAM_TOKEN`- токен для телеграм-бота (получить у `@BotFather` в Телеграме);
- `VK_TOKEN` - токен для группы Вконтакте (получить в разделе "Работа с API" настроек Вконтакте);
- `DIALOGFLOW_PROJECT_ID` - id проекта на DIALOGFLOW (как создать проект [см. здесь](https://cloud.google.com/dialogflow/es/docs/quick/setup));
- `GOOGLE_APPLICATION_CREDENTIALS`- путь к файлу с ключами (как получить ключи [см. здесь](https://cloud.google.com/docs/authentication/getting-started)).
### Телеграм-бот
Запустите бота командой:
```python
python tg_bot.py
```
### Вконтакте-бот
Запустите бота командой:
```python
python vk_bot.py
```
### Как добавить тренировочные фразы
Запустите скрипт командой:
```python
python dialogflow.py {путь к json-файлу с фразами}
```
