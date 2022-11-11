import logging
import os
import sys
import requests
import time
import exceptions
import telegram
from telegram.ext import Updater
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
RETRY_TIME = 600
ENDPOINT = "https://practicum.yandex.ru/api/user_api/homework_statuses/"
HEADERS = {"Authorization": f"OAuth {PRACTICUM_TOKEN}"}


HOMEWORK_STATUSES = {
    "approved": "Работа проверена: ревьюеру всё понравилось. Ура!",
    "reviewing": "Работа взята на проверку ревьюером.",
    "rejected": "Работа проверена: у ревьюера есть замечания.",
}


def send_message(bot, message):
    """Отправление сообщения в Telegram-чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.info(f"В чат {TELEGRAM_CHAT_ID} отправлено сообщение: "
                     "{message}.")
    except Exception as error:
        logging.error(f"В чат {TELEGRAM_CHAT_ID} не удалось отправить "
                      "сообщение.")
        raise SystemError("Ошибка отправки сообщения в Telegram.") from error


def get_api_answer(current_timestamp):
    """Получение статуса домашней работы."""
    timestamp = current_timestamp or int(time.time())
    params = {"from_date": timestamp}
    response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    if response.status_code != 200:
        logging.error(f"URL-адрес {ENDPOINT} недоступен или использован "
                      "невалидный токен.")
        raise exceptions.StatuCodeIsNotOK(response.status_code)
    homeworks = response.json()
    return homeworks


def check_response(response):
    """Проверка корректности ответа."""
    logging.info("Проверка ответа.")
    if not isinstance(response, dict):
        logging.error("Ответ не является словарем.", exc_info=True)
        raise TypeError("Ответ не является словарем.")
    if "homeworks" not in response:
        logging.error("В полученном словаре отсутствует ключ homeworks.",
                      exc_info=True)
        raise KeyError("В полученном словаре отсутствует ключ homeworks.")
    homeworks = response["homeworks"]
    if not isinstance(homeworks, list):
        logging.error("Ответ не является списком.", exc_info=True)
        raise TypeError("Ответ не является списком.")
    return homeworks


def parse_status(homework):
    """Формирование сообщения для отправки в Telegram-чат."""
    if "homework_name" not in homework:
        logging.error("В полученном списке нет ключа homework_name.",
                      exc_info=True)
        raise KeyError("В полученном списке нет ключа homework_name.")
    if "status" not in homework:
        logging.error("В полученном списке нет ключа status.",
                      exc_info=True)
        raise KeyError("В полученном списке нет ключа status.")
    homework_name = homework["homework_name"]
    homework_status = homework["status"]
    if homework_status not in HOMEWORK_STATUSES:
        logging.error(f"Неизвестный статус домашней работы: "
                      f"{homework_status}", exc_info=True)
        raise Exception(f"Неизвестный статус домашней работы: "
                        f"{homework_status}")
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка доступности переменных окружения."""
    if all((PRACTICUM_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)):
        return bool


def main():
    """Основная логика работы бота."""
    logging.basicConfig(
        level=logging.INFO,
        handlers=[logging.StreamHandler(sys.stdout)],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    logger = logging.getLogger(__name__)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    logger.addHandler(stream_handler)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    updater = Updater(token=TELEGRAM_TOKEN)
    updater.start_polling(RETRY_TIME)
    current_timestamp = int(time.time())

    if not check_tokens():
        logging.critical("Отсутствует обязательная переменная окружения: "
                         "{}.")
        sys.exit('Программа принудительно остановлена.')
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks_list = check_response(response)
            if homeworks_list:
                send_message(bot, parse_status(homeworks_list[0]))
                current_timestamp = response.get("current_date")
            else:
                logger.debug("Новые статусы проверки отсутствуют.")
                send_message(bot, "Новые статусы проверки отсутствуют.")
        except Exception as error:
            logger.error(error)
            message = f"Сбой в работе программы: {error}"
            send_message(bot, message)
        finally:
            time.sleep(RETRY_TIME)


if __name__ == "__main__":
    main()
