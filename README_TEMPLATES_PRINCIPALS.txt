------------------------------------
Микроконтроллер Template
------------------------------------
Файл:

Логика:

Задача:
1.
2.
3.

Элементная база:

Схема подключения:
http://asciiflow.com/

------------------------------------
Модуль (программа) Template
------------------------------------
Модуль <name>
-----------------
Файл: <name.py>
User Story:
Кто? Что делает? Зачем?
Use Case
Main success scenario
Extensions - сценарии ошибок.
Variations - варианты успешных сценариев.

Метод запуска:

Задача:
1.
2.
3.

Действия (для логирования):
а.
б.
в.

************************************************************************************************************************
Основные принципы
************************************************************************************************************************
------------------------------------
Принцип наименования версий (снизу вверх)
------------------------------------

Version 0.2.0.dev - Начало работы над новой версией.
Version 0.1.1 - Изменения ошибок версии, обнаруженных в продакшн после применения.
Version 0.1.0 - Версия, применяемая в продакшн. Выполняется миграция в ветку master.
190504 - Изменения в рамках работы над новой версией в ветке develop.
Version 0.1.0.dev - означает начало разработки новой версии. Работы ведутся в ветке develop.

------------------------------------
Принцип логирования
------------------------------------

При использовании предложенного принципа можно строить очтеты по регулярным событиям и отслеживать пропадание регулярного события.
Можно искать в логах события типа Error для генерации аварий.

На примере программы david_climate_check.py:

Название логгера и название файла лога соответсвует названию модуля без префикса david.
Для модуля david_climate_check.py название логгера будет climate_check, а название файла climate_check.log.

1. Определить основные действия модуля или программы

а. Читает файлы.
б. Читает базу данных.
в. Проигрывает звуковой файл.

2. Задать названия для сообщения Massage по каждому типу действия.
Названия формируются по принципу name_name

а. check_file
б. db_connect
в. playing_file

3. Для каждого типа действий придумать сообщения по уровням

Уровни в порядке значимости:
debug
info
warning
error
critical

а. check_file
climate_check.info(f'Message=check_file;File={file_name};Result=exists')
climate_check.error(f'Message=check_file;File={file_name};Result=does_not_exist')

б. db_connect
climate_check.debug(f'Message=db_connect;DB={file_sqlite_db};Result=OK')
climate_check.error(f'Message=db_connect;DB={file_sqlite_db};Result={e}')

в. playing_file
climate_check.debug(f'Message=playing_file;File={file_climate_hot_bedroom};Result=OK')
climate_check.error(f'Message=playing_file;File={file_climate_hot_bedroom};Result={e}')

------------------------------------
Принцип формирования get запросов
------------------------------------

Типы информации, передаваемой в get запросах с модулей NodeMCU:
1. Подключение.
2. Передача информации.

1. Подключение
http://<IP address>:80/connected;sensor=<sensor_num>&ip=<ip_address_of_the_module>
Пример:
http://192.168.1.44:80/connected;sensor=1&ip=192.168.1.66

2. Передача информации
http://<IP address>:80/<information_type>;sensor=<sensor_num>&<key1>=<value1>&<key2>=<value2>...
http://192.168.1.44:80/climate;sensor=1&readattempt=0&temperature=25&humidity=30

Где sensor - уникальный номер датчика (а не контроллера).
Например, датчики температуры подключены к нескольким контроллерам или несколько датчиков подключено к одному и тому же контроллеру.
У каждого датчика свой уникальный номер.
Информация о датчике заносится в таблицу SENSORS, где SENSOR_ID - уникальный номер датчика.