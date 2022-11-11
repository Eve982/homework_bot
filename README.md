# homework_bot
python telegram bot

<!-- Последовательность действий бота должна быть примерно такой:
1. Делать запрос к API раз в 10 минут 
2. Проверить статус отправленной на ревью домашней работы;
3. Если есть обновления статуса — получить статус работы из обновления и отправить сообщение в Telegram.
Подождать некоторое время и сделать новый запрос.
4. Логировать свою работу и сообщать вам о важных проблемах сообщением в Telegram.
5. Докстринги в коде — это признак хорошего тона и профессионализма. Будьте профессиональны, не забудьте про них при написании функций. 

- Функция check_tokens() проверяет доступность переменных окружения, которые необходимы для работы программы. Если отсутствует хотя бы одна переменная окружения — функция должна вернуть False, иначе — True.
- Функция get_api_answer() делает запрос к единственному эндпоинту API-сервиса. В качестве параметра функция получает временную метку. В случае успешного запроса должна вернуть ответ API, преобразовав его из формата JSON к типам данных Python.
- Функция check_response() проверяет ответ API на корректность. В качестве параметра функция получает ответ API, приведенный к типам данных Python. Если ответ API соответствует ожиданиям, то функция должна вернуть список домашних работ (он может быть и пустым), доступный в ответе API по ключу 'homeworks'.
- Функция parse_status() извлекает из информации о конкретной домашней работе статус этой работы. В качестве параметра функция получает только один элемент из списка домашних работ. В случае успеха, функция возвращает подготовленную для отправки в Telegram строку, содержащую один из вердиктов словаря HOMEWORK_STATUSES.
- Функция main(): в ней описана основная логика работы программы. Все остальные функции должны запускаться из неё.
- Функция send_message() отправляет сообщение в Telegram чат, определяемый переменной окружения TELEGRAM_CHAT_ID. Принимает на вход два параметра: экземпляр класса Bot и строку с текстом сообщения.
Логирование
Каждое сообщение в журнале логов должно состоять как минимум из:
- даты и времени события,
- уровня важности события,
- описания события.
Например:
2021-10-09 15:34:45,150 [ERROR] Сбой в работе программы: Эндпоинт https://practicum.yandex.ru/api/user_api/homework_statuses/111 недоступен. Код ответа API: 404
2021-10-09 15:34:45,355 [INFO] Бот отправил сообщение "Сбой в работе программы: Эндпоинт [https://practicum.yandex.ru/api/user_api/homework_statuses/](https://practicum.yandex.ru/api/user_api/homework_statuses/) недоступен. Код ответа API: 404" 
или
2021-10-09 16:19:13,149 [CRITICAL] Отсутствует обязательная переменная окружения: 'TELEGRAM_CHAT_ID'
Программа принудительно остановлена.

Обязательно должны логироваться такие события:
- отсутствие обязательных переменных окружения во время запуска бота (уровень CRITICAL).
- недоступность эндпоинта https://practicum.yandex.ru/api/user_api/homework_statuses/ (уровень ERROR);
- удачная отправка любого сообщения в Telegram (уровень INFO);
- сбой при отправке сообщения в Telegram (уровень ERROR);
- любые другие сбои при запросе к эндпоинту (уровень ERROR);
- отсутствие ожидаемых ключей в ответе API (уровень ERROR);
- недокументированный статус домашней работы, обнаруженный в ответе API (уровень ERROR);
- отсутствие в ответе новых статусов (уровень DEBUG).
Если считаете нужным — добавьте логирование каких-то ещё событий, не ограничивайтесь предложенным списком.

Подсказки
Краткая документация к API-сервису и примеры запросов доступны в шпаргалке «API сервиса Практикум.Домашка».
Для отладки бота можно запрашивать домашку за какое-нибудь определённое время, скажем «месяц назад», чтобы в ответ прилетала информация о какой-нибудь старой домашней работе.
Если установить параметр from_date равным нулю — API вернёт статусы домашек за всё время.
Логины, пароли, токены и другие конфиденциальные данные храните в переменных окружения. В случае отсутствия хотя бы одной из обязательных переменных окружения при запуске бота, его работу нужно принудительно остановить;
Не изменяйте в прекоде имена переменных окружения PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, иначе ваша домашняя работа не пройдёт тесты перед ревью.
Хорошей практикой считается создавать и использовать свои собственные исключения там, где они необходимы. Собственные исключения принято хранить в отдельном файле exceptions.py.

События уровня ERROR нужно не только логировать, но и пересылать информацию о них в ваш Telegram в тех случаях, когда это технически возможно (если API Telegram перестанет отвечать или при старте программы не окажется нужной переменной окружения — ничего отправить не получится).
Если при каждой попытке бота получить и обработать информацию от API ошибка повторяется — не нужно повторно отправлять сообщение о ней в Telegram: о такой ошибке должно быть отправлено лишь одно сообщение. При этом в логи нужно записывать информацию о каждой неудачной попытке.
В уроке «KittyBot: журнал ошибок» вы познакомились с некоторыми хэндлерами. Для работы с логами проекта примените обработчик StreamHandler, логи выводите в стандартный поток sys.stdout.
-->
Бот на старт!
Теперь приложение можно запустить. Перейдите во вкладку Resources и активируйте переключатель напротив строки worker python homework.py. Для этого нажмите на пиктограмму с карандашом справа от переключателя, активируйте переключатель и подтвердите действие, нажав на появившуюся кнопку Confirm.

Логирование на сервисе Heroku
По умолчанию Heroku показывает логи в собственном веб-интерфейсе: More → View Logs. Чтобы логи вашего приложения сохранялись и показывались в Heroku, их следует отправлять в стандартные потоки stdout и stderr. Более детальный рассказ о настройке логов есть в документации Heroku.
