# DAVID

Author: balobin.p@mail.ru
Version 0.8.0.dev
Date 31.05.20

************************************************************************************************************************
Checkout list:
************************************************************************************************************************

1. Записать изменения в README.md в секцию "Изменения версий и процедуры"
2. Занести изменения в документацию "README.docx"
3. Изменить версию в скриптах микроконтроллеров (если были изменения)
4. Сохранить изменения в Git

************************************************************************************************************************
To Do list:
************************************************************************************************************************

Уровень идей:
1. Сделать словарь английского языка для детей на основе nltk.corpus.wordnet.
2. Добавить модуль диагностики состояния датчиков и базы данных. Модуль должен запускаться по голосовому сигналу и предоставлять голосовой отчет.
3. Модуль. Таймер. Создавать голосом задачу на установку таймера.
4. Модуль. Список покупок.
5. Модуль. Каша.
10. Сделать приветствие при получении сигнала с датчика открывания двери.
13. Добавить интеграцию с сайтом погоды и добавить воозможность запрашивать погоду голосом.
14. Установить датчик движения в коридор для определения когда кто-то пришел с улицы для приветствия.
18. Установить Splunk для контроля состояния по данным файлов логов.
23. Добавить возможность выполнения API запросов из внешней сети (либо запросов по WA).
25. Сделать базу данных по категориям для детей на сайте, чтобы дети могли собирать материал по исследовательским темам.
27. Добавить камеру на базе ESP32-CAM к системе датчиков входной двери.
28. Сделать модуль "Здоровье", который будет каждый день осведомляться о здоровье и записывать в базу. Таким образом, будет собрана база самочуствия.
29. Сделать распознавание лиц на камере входной двери.

Главный Компьютер и общие замечания:
1. Добавить обработку get запроса от контроллера NodeMcu02Gas о стоящей на газу посуде.
2. Добавить API на базе flask и flask_sqlalchemy для получения данных из базы данных.
3. Настроить звук и колонки
4. Все процедуры установки перенести в doc из README_CHANGE_HISTORY

Модуль Django:
1. Упростить пароли
4. Решить проблему с первым входом на страницу Math, когда у пользователя нет ни одной решенной задачи в task02.

Модуль david_web_server:
1. Переделать, чтобы web server слушал не 80 порт а другой, в противном случае не запустить apach.

Модуль climate_check:
1. 

Модуль david_gas_check:
1. 

Модуль david_currency_check:
1. 

Модуль david_unittest:
1. 

Модуль david_healthcheck:
2. Доделать информирование пользователя.

Модуль david_user_interface:
1. 

Микроконтроллер NodeMcu01BedRoom:
1. Добавить sensor ID на экран при первичном подключении.
3. Добавить сохранение данных в файл в случае недоступности сервера с выгрузкой на сервер после появления сервера.
4. На корпусе на ножках крепления дисплея добавить уголки на широких поддержках, чтобы зафиксировать дисплей.

Микроконтроллер NodeMcu02Gas:
3. Добавить датчик освещенности.
4. Добавить отображения кол-ва секунд до выключения освещения согласно схеме дисплея.
5. Сделать пересчет уровня газа в проценты по формуле.
7. Увеличить отверстие для провода в корпусе с дисплеем.
9. Добавить точку на дисплей в случае успешной отправки данных по газу на сервер согласно схеме дисплея.
10. Строку инициализации дисплея в boot.py обернуть в try "oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)"
11. Заменить на схемах выход управления реле с D4 на D0, а buzzer наоборот.
13. ID сенсора движения вывести в переменную.
15. Убрать столбики из модели DhtMqCover. Для фиксации датчиков сделать упоры по краям. Добавить уши для крепления Stand
16. Сделать отдельные корпуса для датчиков газа и температуры (т.к. датчик газа сильно греется)
17. Заменить датчик температуры на DHT22 и в последствии на Dallas. Измерение влажности убрать.

Микроконтроллер NodeMcu03Door (датчик между входными дверями)
1. Увеличить таймер выключения света до 30 секунд.
3. В http запрос connect добавить версию прошивки.
4. Сделать переход на MicroPython.
5. В http запрос connect добавить версию прошивки (Ver.1).

Микроконтроллер NodeMcu04Entrance (датчик в коридоре)
1. Разработать.

Микроконтроллер NodeMcu01cChildrenRoom:
1. Выполнить переход на Ver.02 (MicroPython)

************************************************************************************************************************
Изменения версий и процедуры
************************************************************************************************************************

------------------------------------
Version 0.8.0.dev change list and installation procedure:
------------------------------------

Главный Компьютер:
1. david_web_server.py отправка нотификации по мэйлу только для sensor_id == '3': # NodeMcu03Door

Микроконтроллер NodeMcu02Gas:
1. Добавлена отправка оповещения на Главный компьютер о движении.
2. Выход управления реле заменен с D4 на D0
3. Удален buzzer (200606)
4. Добавлен gc.collect() (200606)

Version installation procedure:
