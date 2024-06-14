Описание работы

wsgi приложение (веб приложение использующее интерфейс wsgi для ответа клиенту) реализующее аналог сервиса time.is и предоставляющее работу с временными зонами на базе библиотеки tz

по запросу GET / отдает текущее время в запрошенной зоне в формате html. может быть пустым - тогда в GMT
по запросу POST /api/v1/convert - преобразует дату/время из одного часового пояса в другой
принимает: параметр date - json формата {“date”:“12.20.2021 22:21:05”, “tz”: “EST”} и target_tz - строку с определением зоны
по запросу POST /api/v1/datediff- отдает число секунд между между двумя датами из параметра data (json формат {“first_date”:“12.06.2024 22:21:05”, “first_tz”: “EST”, “second_date”:“12:30pm 2024-02-01”, “second_tz”: “Europe/Moscow”})
Структура файлов

app2.pу - Файл содержащий код WSGI сервера unit_tests.py - Файл содержащий unit тесты

Тесты Postman

Тесты Postman размещены по ссылке:

https://www.postman.com/poopshitkal/workspace/vladislav/collection/36175477-61b1890f-4e4a-4045-9e2d-1c9e61732bcd?action=share&creator=36175477