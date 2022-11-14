import logging
import os
import signal
import sys
import time
from http import HTTPStatus

import requests

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError
import telegram
from dotenv import load_dotenv
from telegram.error import TelegramError
from telegram.ext import Updater

import exceptions
from endpoints import ENDPOINT

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HEADERS = {"Authorization": f"OAuth {PRACTICUM_TOKEN}"}
TELEGRAM_RETRY_TIME = 600
HOMEWORK_VERDICTS = {
    "approved": "Работа проверена: ревьюеру всё понравилось. Ура!",
    "reviewing": "Работа взята на проверку ревьюером.",
    "rejected": "Работа проверена: у ревьюера есть замечания.",
}


def send_message(bot, message):
    """Старт отправки сообщения в Telegram-чат."""
    logging.info("Старт отправки сообщения в Telegram-чат.")
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.info(f"В чат {TELEGRAM_CHAT_ID} отправлено сообщение: "
                     "{message}.")
    except (TelegramError, ConnectionResetError):
        logging.error(f"В чат {TELEGRAM_CHAT_ID} не удалось отправить "
                      "сообщение.", exc_info=True)
        raise SystemError("Ошибка отправки сообщения в Telegram-чат.")


def get_api_answer(current_timestamp):
    """Получение статуса домашней работы."""
    logging.info("Старт получения статуса домашней работы.")
    timestamp = current_timestamp or int(time.time())
    params = {"from_date": timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except Exception as e:
        raise Exception(f"Ошибка запроса: {e}")
    if response.status_code != HTTPStatus.OK:
        logging.error(f"URL-адрес {ENDPOINT} недоступен или использован "
                      "невалидный токен.", exc_info=True)
        raise exceptions.StatusCodeIsNotOK(response.status_code)
    try:
        homeworks = response.json()
    except JSONDecodeError:
        logging.error("Не получилось преобразовать ответ в JSON.",
                      exc_info=True)
        raise Exception("Не получилось преобразовать ответ в JSON.")
    return homeworks


def check_response(response):
    """Проверка корректности ответа."""
    logging.info("Старт проверки ответа сервера.")
    if not isinstance(response, dict):
        logging.error("Ответ не является словарем.")
        raise TypeError("Ответ не является словарем.")
    if "homeworks" not in response:
        logging.error("В полученном словаре отсутствует ключ homeworks.")
        raise KeyError("В полученном словаре отсутствует ключ homeworks.")
    homeworks = response.get("homeworks")
    if not isinstance(homeworks, list):
        logging.error("Ответ не является списком.")
        raise TypeError("Ответ не является списком.")
    return homeworks


def parse_status(homework):
    """Формирование сообщения для отправки в Telegram-чат."""
    logging.info("Старт формирования сообщения для отправки в чат.",
                 exc_info=True)
    if "homework_name" not in homework:
        logging.error("В полученном списке нет ключа homework_name.")
        raise KeyError("В полученном списке нет ключа homework_name.")
    if "status" not in homework:
        logging.error("В полученном списке нет ключа status.")
        raise KeyError("В полученном списке нет ключа status.")
    homework_name = homework.get("homework_name")
    homework_status = homework.get("status")
    if homework_status not in HOMEWORK_VERDICTS:
        logging.error(f"Неизвестный статус домашней работы: "
                      f"{homework_status}")
        raise Exception(f"Неизвестный статус домашней работы: "
                        f"{homework_status}")
    verdict = HOMEWORK_VERDICTS[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка доступности переменных окружения."""
    logging.info("Старт проверки доступности переменных окружения.")
    return all((PRACTICUM_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))


def main():
    """Основная логика работы бота."""
    logging.info("Старт программы.")
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    updater = Updater(token=TELEGRAM_TOKEN)
    updater.start_polling(TELEGRAM_RETRY_TIME)
    current_timestamp = int(time.time())

    if not check_tokens():
        logging.critical("Отсутствует обязательная переменная окружения.")
        sys.exit(0)
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
            time.sleep(TELEGRAM_RETRY_TIME)


if __name__ == "__main__":
    def signal_handler(signal, frame):
        """Обработка ошибки KeyboardInterrupt."""
        logging.info("Работа программы остановлена вручную нажатием Ctrl+C.")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    print('Нажмите Ctrl+C чтобы завершить выполнение программы.')

    logging.basicConfig(
        level=logging.INFO,
        handlers=[logging.StreamHandler(sys.stdout)],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    logger = logging.getLogger(__name__)
    main()
