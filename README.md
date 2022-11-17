<h2>Проект "Телеграм-бот для получения последнего статуса домашней работы".</h2>

<h3>Как работает бот:</h3>
<ol>
    <li>Делает запрос к API раз в 20 минут.</li>
    <li>Проверяет статус отправленной на ревью домашней работы.</li>
    <li>Получает статус последней работы.</li>
    <li>Если статус изменился - отправляет сообщение в Telegram, в противном случае только логирует полученный статус.</li>
    <li>Логирует все действия и сообщает о важных проблемах сообщением в Telegram (если отправка сообщений возможна при такой проблеме):
    <li>отсутствует необходимая переменная окружения (уровень CRITICAL - программа останавливается);
        <ul>
            <li>недоступен эндпоинт (уровень ERROR);</li>
            <li>удачная отправка любого сообщения в Telegram (уровень INFO);</li>
            <li>сбой при отправке сообщения в Telegram (уровень ERROR);</li>
            <li>любые другие сбои при запросе к эндпоинту (уровень ERROR);</li>
            <li>отсутствие ожидаемых ключей в ответе API (уровень ERROR);</li>
            <li>недокументированный статус домашней работы, обнаруженный в ответе API (уровень ERROR);</li>
            <li>отсутствие в ответе новых статусов (уровень DEBUG).</li>
        </ul>
    </li>
</ol>

<ul>
    <li>Функция check_tokens() проверяет доступность переменных окружения, которые необходимы для работы программы. Если отсутствует хотя бы одна переменная окружения — функция должна вернуть False, иначе — True.</li>
    <li>Функция get_api_answer() делает запрос к единственному эндпоинту API-сервиса. В качестве параметра функция получает временную метку. В случае успешного запроса должна вернуть ответ API, преобразовав его из формата JSON к типам данных Python.</li>
    <li>Функция check_response() проверяет ответ API на корректность. В качестве параметра функция получает ответ API, приведенный к типам данных Python. Если ответ API соответствует ожиданиям, то функция должна вернуть список домашних работ (он может быть и пустым), доступный в ответе API по ключу 'homeworks'.</li>
    <li>Функция parse_status() извлекает из информации о конкретной домашней работе статус этой работы. В качестве параметра функция получает только один элемент из списка домашних работ. В случае успеха, функция возвращает подготовленную для отправки в Telegram строку, содержащую один из вердиктов словаря HOMEWORK_STATUSES.</li>
    <li>Функция main(): в ней описана основная логика работы программы. Все остальные функции должны запускаться из неё.</li>
    <li>Функция send_message() отправляет сообщение в Telegram чат, определяемый переменной окружения TELEGRAM_CHAT_ID. Принимает на вход два параметра: экземпляр класса Bot и строку с текстом сообщения.</li>
</ul>