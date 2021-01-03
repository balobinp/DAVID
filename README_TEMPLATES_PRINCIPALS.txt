************************************************************************************************************************
Основные принципы
************************************************************************************************************************

------------------------------------------------------------------------
Принцип наименования версий
------------------------------------------------------------------------

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
git commit -m "YYMMDD"
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
7. Сделать первый commit для новой версии. Например: Version 0.2.0.dev
git add .
git commit -m "Version 0.2.0.dev"
git push origin develop
8. Выполнить deploy в Jenkins.

------------------------------------------------------------------------
Принцип формирования To do листа
------------------------------------------------------------------------

Все идеи и действия записыать в README.md
Расширенные списки действий записывать в README.docx в раздел "Сделать" для соответствующих модулей.

------------------------------------------------------------------------
Принцип логирования
------------------------------------------------------------------------

При использовании предложенного принципа можно строить очтеты по регулярным событиям.
Можно отслеживать пропадание регулярного события.
Можно искать в логах события типа Error для генерации аварий.

На примере программы david_climate_check.py:

Название логгера и название файла лога соответсвует названию модуля без префикса david.
Например, для модуля david_climate_check.py название логгера будет climate_check, а название файла climate_check.log.

1. Определить основные действия модуля или программы в разделе "Действия (для логирования)"

Например:
а. Читает файлы.
б. Читает базу данных.
в. Проигрывает звуковой файл.

2. Задать названия для сообщения Massage по каждому типу действия.
Названия формируются в нижнем регистре через подчеркивание.

Например:
а. check_file
б. db_connect
в. playing_file

3. Для каждого типа действий установить уровни и записать в Logger examples

Уровни в порядке значимости:
debug
info
warning
error
critical

Например:
а. check_file
climate_check.info(f'Message=check_file;File={file_name};Result=exists')
climate_check.error(f'Message=check_file;File={file_name};Result=does_not_exist')

б. db_connect
climate_check.debug(f'Message=db_connect;DB={file_sqlite_db};Result=OK')
climate_check.error(f'Message=db_connect;DB={file_sqlite_db};Result={e}')

в. playing_file
climate_check.debug(f'Message=playing_file;File={file_climate_hot_bedroom};Result=OK')
climate_check.error(f'Message=playing_file;File={file_climate_hot_bedroom};Result={e}')

------------------------------------------------------------------------
Принцип документирования
------------------------------------------------------------------------

Для документирования использовать reStructured Text

Пример:

def person(name: str, age: int) -> str:
    """
    **Description**

    Description of function 'person'

    :param name: Name of the person
    :param age: Age of the person
    :return: Description of the person

    :raise NotImplementedError: If no name is set.

    **Notes**

    Some notes

    **Examples**

    >>>person('Pavel', 40)

    """
    if name is None:
        raise NotImplementedError("No name")

    return f'Name: {name}, age: {age}'

------------------------------------------------------------------------
Принцип наименования и нумерации контроллеров и сенсоров
------------------------------------------------------------------------

Контроллеры именуются в Camel формате по принципу <Тип_контроллера><ID_контроллера><Комментарий>.
У контроллера может быть несколько подключенных датчиков и комбинированные датчики.
У контроллера есть главный сенсор. ID этого сенсора является ID контроллера.
Остальным сенсорам присваиваются собственные ID, уникальные во всем проекте.
Все ID сенсоров записаны в таблице SENSORS в базе данных. Также они записаны в разделе Sensors README.docx.

Пример:
Контроллер NodeMcu02Gas. Его ID = 2. Он указан в названии.
У контроллера NodeMcu02Gas есть три сенсора:
- MQ-4 - датчик газа (sendor_id = 2). Главный сенсор. Его ID является ID конотоллера.
- DHT22 - датчик температуры влажности (sendor_id = 5). Дополнительный сенсор.
- AM312 - датчик движения (sendor_id = 6). Дополнительный сенсор.
- DHT22 + AM312 - виртуальный, комбинированный датчик для детекции оставленной на плите посуды (sendor_id = 7).

------------------------------------------------------------------------
Принцип формирования get запросов
------------------------------------------------------------------------

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

------------------------------------------------------------------------
Принцип сохранения версий PCB и корпусов
------------------------------------------------------------------------

Файлы PCB и корпусов имеют название в Camel формате типа <Тип_контроллера><Наименование><ID_контроллера>RevYYMMDD
Например: EspGas2Rev210103
На платах и корпусах печатать отдельно название и версию. Версию указывать через точку.
Например: EspGas2 Rev.210103

В проект сохраняются только те версии, которые были заказаны или напечатаны.

************************************************************************************************************************
Основные процедуры
************************************************************************************************************************

------------------------------------------------------------------------
Main Version change procedure
------------------------------------------------------------------------

1. Проверить, что все обновляемые скрипты имеют актуальные версии в заголовках.
README.md
david_lib.py
Скрипты микроконтроллеров

1. Сделать копию файлов проекта на сервере.
david_*
WEB_UI/*

2. Войти в виртуальное окружение проекта, установить библиотеки и сохранить requirements.txt.
sudo apt-get update
sudo apt-get upgrade
sudo apt-get clean
source /home/david/env/bin/activate
pip freeze --local > requirements.txt
python --version

3. Поместить в директорию /home/david файлы с новыми версиями файлы:
(см. git diff --name-only master)

4. Обновить базу данных:
source /home/david/env/bin/activate
python /home/david/david_db_create.py

5. Перезапустить сервис david_web_server
sudo systemctl stop david.service
sudo systemctl start david.service
sudo systemctl status david.service

6.  Перезапустить Web сервер django
Выполнить миграции:
python manage.py makemigrations english
python manage.py sqlmigrate english 0001
python manage.py migrate english

sudo systemctl restart david_web_ui.service
sudo systemctl -l status david_web_ui.service

8. Выполнить unit тестирование
pytest /home/david/david_unittest.py -v -W ignore::DeprecationWarning
cd /home/david/WEB_UI
python manage.py test children_math.tests
python manage.py test mainpage.tests

9. Завершить
deactivate
exit

------------------------------------
Main initial installation procedure:
------------------------------------

Главный Компьютер
------------------------------------

1. Создать пользователя david и директорию /home/david
su
adduser david
usermod -aG sudo david
exit
su david
cd /home
mkdir ./david
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
sudo apt-get clean

2. Настроить виртуальное окружение для программы.
sudo apt-get install python3-pip
sudo pip3 install virtualenv
cd /home/david
virtualenv env
source /home/david/env/bin/activate
python --version
pip install requests
pip install Flask
pip install Flask-RESTful
pip install twilio
pip install psutil
pip list
pip freeze --local > requirements.txt
deactivate

3. Создать директорию /home/david/log
mkdir ./log

4. Поместить в директорию /home/david файлы:
david_*
./VOICE_SAMPLES/

Пример для ubuntu win10
cp /mnt/c/Users/balob/Documents/DAVID/david_web_server.py /home/david/david_web_server.py
cp /mnt/c/Users/balob/Documents/DAVID/david_climate_check.py /home/david/david_climate_check.py
cp /mnt/c/Users/balob/Documents/DAVID/david_currency_check.py /home/david/david_currency_check.py
cp /mnt/c/Users/balob/Documents/DAVID/david_db.sqlite /home/david/david_db.sqlite
cp /mnt/c/Users/balob/Documents/DAVID/david_db_create.py /home/david/david_db_create.py
cp /mnt/c/Users/balob/Documents/DAVID/david_gas_check.py /home/david/david_gas_check.py
cp /mnt/c/Users/balob/Documents/DAVID/david_healthcheck.py /home/david/david_healthcheck.py
cp /mnt/c/Users/balob/Documents/DAVID/david_lib.py /home/david/david_lib.py
cp /mnt/c/Users/balob/Documents/DAVID/david_unittest.py /home/david/david_unittest.py
cp /mnt/c/Users/balob/Documents/DAVID/david_user_interface.py /home/david/david_user_interface.py
cp /mnt/c/Users/balob/Documents/DAVID/david_pass.json /home/david/david_pass.json

5. Создать базу данных запустив скрипт david_db_create.py
python /home/david/david_db_create.py

9. Запустить сервис для david_web_server.py
Поместить /etc/systemd/system/david.service
cp /mnt/c/Users/balob/Documents/DAVID/david.service /etc/systemd/system/david.service

sudo systemctl daemon-reload
sudo systemctl enable david.service
sudo systemctl start david.service
sudo systemctl status david.service

Проверить, что сервер слушает порт:
(env) david@david:~$ sudo netstat -ltnp | grep :80
tcp        0      0 0.0.0.0:8000            0.0.0.0:*               LISTEN      3570/python
tcp        0      0 192.168.1.44:80         0.0.0.0:*               LISTEN      3794/python

9. Запустить сервисы для david_climate_check / david_currency_check / david_healthcheck

Поместить в папку /home/david файлы:
david_climate_check.timer
david_climate_check.service
david_currency_check.timer
david_currency_check.service
david_healthcheck.timer
david_healthcheck.service

Переместить эти файлы в /etc/systemd/system
sudo mv /home/david/david_climate_check.timer /etc/systemd/system/david_climate_check.timer
sudo mv /home/david/david_climate_check.service /etc/systemd/system/david_climate_check.service
sudo mv /home/david/david_currency_check.timer /etc/systemd/system/david_currency_check.timer
sudo mv /home/david/david_currency_check.service /etc/systemd/system/david_currency_check.service
sudo mv /home/david/david_healthcheck.timer /etc/systemd/system/david_healthcheck.timer
sudo mv /home/david/david_healthcheck.service /etc/systemd/system/david_healthcheck.service

sudo systemctl status david_climate_check.service
sudo systemctl start david_climate_check.service

sudo systemctl status david_currency_check.service
sudo systemctl start david_currency_check.service

sudo systemctl status david_healthcheck.service
sudo systemctl start david_healthcheck.service

sudo systemctl start david_climate_check.timer
sudo systemctl enable david_climate_check.timer # для того, чтобы сервис стартовал при старте системы
sudo systemctl start david_currency_check.timer
sudo systemctl enable david_currency_check.timer
sudo systemctl start david_healthcheck.timer
sudo systemctl enable david_healthcheck.timer

Проверить выполнение
systemctl list-timers
sudo journalctl -u david_climate_check.service  # view the logs for a specific service

5. Перезагрузить папку WEB_UI запустить сервер
Предварительно поменяв путь в файле settings.py
Если нужно, применить миграции и загрузить недостающие данные в базу данных.
python manage.py migrate

Поместить /etc/systemd/system/david_web_ui.service
sudo mv david_web_ui.service /etc/systemd/system/david_web_ui.service

sudo systemctl daemon-reload
sudo systemctl enable david_web_ui.service

sudo systemctl start david_web_ui.service
sudo systemctl -l status david_web_ui.service

7. Загрузить данные в таблицу children_math_contest01
sqlite3 david_db.sqlite
INSERT INTO children_math_contest01
(task_description, answers_options, answer)
VALUES('Папе, маме и дочке вместе 70 лет. Сколько лет им будет вместе через 4 года?', '-', '82');
...

9. Добавить права на запись для файлов логов
sudo chmod 666 /home/david/log/climate_check.log
sudo chmod 666 /home/david/log/currency_check.log
sudo chmod 666 /home/david/log/david_web_server.log
sudo chmod 666 /home/david/log/gas_check.log
sudo chmod 666 /home/david/log/healthcheck.log
sudo chmod 666 /home/david/log/user_interface.log

7. Установить часовой пояс в системе

8. Создать директорию на ftp сервере для загрузки бэкапов базы данных
IP адрес и путь должен быть записан в david_lib.py в переменных:
ftp_ip_addr = '192.168.1.1'
ftp_db_backup_dir = 'Transcend/david/db_backup'

Пароль и юзер для доступа по ftp должен быть записан в david_pass.json в переменных
ftp_user
ftp_pass

7. Выполнить unit тестирование
sudo pytest /home/david/david_unittest.py -v -W ignore::DeprecationWarning
cd /home/david/WEB_UI
python manage.py test children_math.tests
python manage.py test mainpage.tests

Known issues
-------------------
1. Проблема с numpy
Original error was: libf77blas.so.3: cannot open shared object file: No such file or directory

Решение:
sudo apt-get install libatlas-base-dev
(https://github.com/numpy/numpy/issues/14772)

NodeMcu02Gas
------------------------------------

esptool --chip esp8266 --port COM9 erase_flash
esptool --chip esp8266 --port COM9 --baud 115200 write_flash --flash_size=detect 0 c:\Users\balobin.p\Downloads\MicroPython\esp8266-20191220-v1.12.bin

import esp
esp.check_fw()

rshell
connect serial COM9 115200
ls /pyboard
cp ./Downloads/MicroPython/ftp.py /pyboard/ftp.py
cp ./Downloads/MicroPython/david_pass.json /pyboard/david_pass.json
cp ./Downloads/MicroPython/main.py /pyboard/main.py
cp ./Downloads/MicroPython/boot.py /pyboard/boot.py
cp ./Downloads/MicroPython/ssd1306.py /pyboard/ssd1306.py
cp ./Downloads/MicroPython/upysh.py /pyboard/upysh.py

repl

import webrepl_setup
# Выбрать E и установить пароль
import webrepl
webrepl.start()

from upysh import *
ls
