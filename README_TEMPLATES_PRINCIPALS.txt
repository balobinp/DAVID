************************************************************************************************************************
Основные принципы
************************************************************************************************************************

Все модули должны быть покрыты тестами.

------------------------------------
Принцип наименования версий
------------------------------------

(снизу вверх)
Version 0.2.0.dev - Начало работы над новой версией.
Version 0.1.1 - Изменения ошибок версии, обнаруженных в продакшн после применения.
Version 0.1.0 - Версия, применяемая в продакшн. Выполняется миграция в ветку master.
190504 - Изменения в рамках работы над новой версией в ветке develop.
Version 0.1.0.dev - означает начало разработки новой версии. Работы ведутся в ветке develop.

Методика миграции в ветку master:
1. Изменить в README.md и david_lib.py версию на продакшн. Например: Version 0.1.0.dev -> Version 0.1.0
2. Поставит текущую дату в README.md. Например: Date 31.05.20
3. Проверить, что все изменения занесены в README.md в "Version 0.1.0.dev change list and installation procedure"
4. Выполнить сохранение версии в ветке develop:
git add .
git commit -m "201113"
git push origin develop
git diff --name-only master
git checkout master
git merge develop -m "Version 0.1.0"
git push origin master
git diff --name-only develop
git log --graph --all --decorate --oneline
git checkout develop
5. Перенести раздел "Version 0.1.0.dev change list and installation procedure" из README.md в README_CHANGE_HISTORY.txt
6. Создать новый раздел в README.md "Version 0.2.0.dev change list and installation procedure"
7. Сделать первый commit для новой версии
git add .
git commit -m "Version 0.2.0.dev"
git push origin develop

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
Принцип наименования и нумерации контроллеров и сенсоров
------------------------------------

Контроллеры именуются в Camel формате по принципу <Тип_контроллера><ID_контроллера><Комментарий>.
У контроллера может быть несколько подключенных датчиков и комбинированные датчики.
У контроллера есть главный сенсор. ID этого сенсора является ID контроллера.
Остальным сенсорам присваиваются собственные ID, уникальные во всем проекте.
Все ID сенсоров записаны в таблице SENSORS в базе данных. Также они записаны в разделе Sensors описания.

Пример:
Контроллер NodeMcu02Gas. Его ID = 2. Он указан в названии.
У контроллера NodeMcu02Gas есть три сенсора:
- MQ-4 - датчик газа (sendor_id = 2). Главный сенсор. Его ID является ID конотоллера.
- DHT22 - датчик температуры влажности (sendor_id = 5). Дополнительный сенсор.
- AM312 - датчик движения (sendor_id = 6). Дополнительный сенсор.
- DHT22 + AM312 - комбинированный датчик для детекции оставленной на плите посуды (sendor_id = 7).

------------------------------------
Принцип формирования get запросов
------------------------------------

Типы информации, передаваемой в get запросах с модулей NodeMCU:
1. Подключение.
2. Передача информации.

1. Подключение
http://<IP address>:80/connected;sensor=<sensor_num>&ip=<ip_address_of_the_module>&ver=<version>
Пример:
http://192.168.1.44:80/connected;sensor=1&ip=192.168.1.66&ver=190720

2. Передача информации
http://<IP address>:80/<information_type>;sensor=<sensor_num>&<key1>=<value1>&<key2>=<value2>...
http://192.168.1.44:80/climate;sensor=1&readattempt=0&temperature=25&humidity=30

Где sensor - уникальный номер датчика (а не контроллера).
Например, датчики температуры подключены к нескольким контроллерам или несколько датчиков подключено к одному и тому же контроллеру.
У каждого датчика свой уникальный номер.
Информация о датчике заносится в таблицу SENSORS, где SENSOR_ID - уникальный номер датчика.
