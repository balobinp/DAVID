# DAVID

Author: balobin.p@mail.ru
Version 0.2.0.dev
Date 04.05.19

**************************************************************************************************************************************************
To Do list:
**************************************************************************************************************************************************

Главный Компьютер:
1. Сделать словарь английского языка для детей на основе nltk.corpus.wordnet.
2. Добавить модуль диагностики состояния датчиков и базы данных. Модуль должен запускаться по голосовому сигналу и предоставлять голосовой отчет.
3. Модуль. Таймер. Создавать голосом задачу на установку таймера.
4. Модуль. Список покупок.
5. Модуль. Каша.
10. Сделать приветствие при получении сигнала с датчика открывания двери.
12. Добавить в автозагрузку.
13. Добавить интеграцию с сайтом погоды и добавить воозможность запрашивать погоду голосом.
14. Установить датчик движения в коридор для определения когда кто-то пришел с улицы для приветствия.
18. Установить Splunk для контроля состояния по данным файлов логов.
19. Добавить watchdog контроля запущеных скринов с перезапуском в случае остановки.
20. Добавить секунды в VIEW V_MOTION_SENSORS и V_CLIMATE_SENSORS.
22. Информирование по WA в случае срабатывания датчика движения входной двери.
23. Добавить возможность выполнения API запросов из внешней сети (либо запросов по WA).
24. Решить проблему с зависанием WA twilio.

Модуль david_web_server:
1. В случае отсутствия файлов базы данных или логов добавлять их.

Модуль climate_check:
1. Отслеживать динамику изменения температуры и при резком похолодании сообщать: "В спальне становиться прохладно".
2. Вынести пороги температуры срабатывания в david_lib

Модуль david_gas_check:
1. Написать модуль.

Модуль david_currency_check:
1. 

Модуль david_unittest:
1. 

Микроконтроллер NodeMcu01BedRoom:
1. Реализовать подключение к WiFi модулей ESP в цикле только для передачи информации, чтобы устранить лишнее излучение (???).
2. Добавить Deep sleep для модулей ESP с делью экономии энергии и устранения излучения (???).
3. Заменить датчик DHT11 на DHT22.
4. Вынести номер сенсора и IP главного компютрера в переменные.

Микроконтроллер NodeMcu02Gas:
1. Сделать.

Микроконтроллер NodeMcu03Door (датчик между входными дверями)
1. Заменить датчик движения.

Микроконтроллер NodeMcu04Entrance (датчик в коридоре)
1. Заменить датчик движения.

**************************************************************************************************************************************************
Изменения версий и процедуры
**************************************************************************************************************************************************

------------------------------------
Version 0.2.0.dev change list and instalation procedure:
------------------------------------

Главный Компьютер:

Модуль david_web_server:
1. Добавлен обработчик событий от Микроконтроллера NodeMcu02Gas.

Микроконтроллер NodeMcu02Gas:
1. 

Version 0.2.0 change procedure:

1. Войти в виртуальное окружение для программы.
source /home/david/env/bin/activate
python --version

2. Поместить в директорию /home/david файлы:
david_unittest.py
david_lib.py
david_db_create.py
david_web_server.py

3. Сделать backup базы данных и обновить ее запустив скрипт:
python /home/david/david_db_create.py

4. Переименоват копию backup базы данных (т.к. unittest перезапишет копию).

5. Перезапустить сервис david_web_server
systemctl stop david.service
systemctl start david.service
systemctl status david.service

6. Выполнить unit тестирование
python /home/david/david_unittest.py

------------------------------------
Version 0.0.2 change list and instalation procedure:
------------------------------------

Главный Компьютер:
1. Добавлен модуль david_currency_check.
2. Модуль david_web_server переведен на Flast-RESTful.
4. logger переписан на собственный файл.

Модуль climate_check:
1. Имена файлов вынесены в модуль david_lib.py.
2. logger переписан на собственный файл.
3. Запуск файла переписан на crone.
4. Добавлена проверка на низкую температуру с оповещением.

Version 0.0.2.dev change procedure:

0. Войти в виртуальное окружение для программы и установить библиотеки.
source /home/david/env/bin/activate
python --version
pip install Flask
pip install Flask-RESTful
pip install twilio
pip list
pip freeze --local > requirements.txt
# deactivate

1. Поместить в директорию /home/david файлы:
david_currency_check.py
david_unittest.py
david_lib.py
david_db_create.py
david_web_server.py
climate_check.py
./VOICE_SAMPLES/climate_cold_bedroom.mp3

2. Сделать backup базы данных и обновить ее запустив скрипт:
python /home/david/david_db_create.py

3. Переименоват копию backup базы данных (т.к. unittest перезапишет копию).

4. Создать файл лога
/home/david/log/currency_check.log

0. Перезапустить скрин david_web_server и остановить david_climate_check
sudo screen -ls
sudo screen -d -r  30158.david_climate_check # вернуть скрин на передний план
Ctrl+C
exit
sudo screen -d -r 30137.david_web_server
sudo screen -S david_web_server
cd /home/david
source /home/david/env/bin/activate
python /home/david/david_web_server.py
Ctrl+A -> D
sudo screen -ls

6. Выполнить unit тестирование
python /home/david/david_unittest.py

7. Добавить модули david_currency_check.py и david_climate_check.py в crontab
crontab -e
*/15 * * * * /home/david/env/bin/python /home/david/david_climate_check.py
0 17 */1 * 1-5 /home/david/env/bin/python /home/david/david_currency_check.py

------------------------------------
Version 0.0.1 change list and instalation procedure:
------------------------------------

Главный Компьютер:
1. Добавлены таблицы SENSORS и MOTION_SENSORS в базу данных.
2. Добавлены VIEW, V_MOTION_SENSORS и V_CLIMATE_SENSORS.
3. Сделано виртуальное окружение и создана отдельная папка для проекта /home/user/david/

Модуль david_web_server:
1. Добавлено логирование событий в файл для модуля david_web_server. В том числе логирование событий подключения Микроконтроллеров NodeMcu01BedRoom и NodeMcu03Door.
2. Сделаны абсолютные пути к файлам, чтобы можно было запускать из любого места файловой системы.
3. Сделан перенос программы в собственный каталог под собственным пользователем david.
4. Добавлен обработчик событий от Микроконтроллера NodeMcu03Door.

Модуль climate_check:
1. Добавлено логирование событий в файл для модуля climate_check.

Микроконтроллер NodeMcu01BedRoom:
1. Изменен формат http get запроса при подключении.

Микроконтроллер NodeMcu03Door
1. Прошить и установить.

Version 0.0.1.dev change procedure:
0. Остановить скрины.
1. Создать пользователя david и директорию /home/david
su
adduser david
usermod -aG sudo david
cd /home
mkdir ./david

2. Настроить виртуальное окружение для программы.
sudo pip3.6 install virtualenv
virtualenv env
source /home/david/env/bin/activate
python --version
pip install requests
pip list
pip freeze --local > requirements.txt
#deactivate

3. Создать директорию /home/david/log
mkdir ./log

3. Перенести базу данных в /home/david/david_db.sqlite
sudo cp /home/pavel/david/david_db.sqlite /home/david/david_db.sqlite
sudo chown david:david /home/david/david_db.sqlite

4. Обновить базу данных запустив скрипт david_db_create.py
python /home/david/david_db_create.py

5. Поместить в директорию /home/david файлы:
david_lib.py
david_web_server.py
david_unittest.py
david_climate_check.py

6. Поместить файл голосового сэмпла в /home/pavel/david/VOICE_SAMPLES
mkdir ./VOICE_SAMPLES
cp /home/pavel/david/VOICE_SAMPLES/climate_hot_bedroom.mp3 /home/david/VOICE_SAMPLES/climate_hot_bedroom.mp3

7. Выполнить unit тестирование
python /home/david/david_unittest.py

8. Обновить прошивку NodeMcu01BedRoom.

9. Запустить скрин для david_web_server.py и climate_check.py
sudo screen -S david_web_server
cd /home/david
source /home/david/env/bin/activate
python /home/david/david_web_server.py
Ctrl+A -> D
sudo screen -ls

sudo screen -S david_climate_check
cd /home/david
source /home/david/env/bin/activate
python /home/david/david_climate_check.py
Ctrl+A -> D
sudo screen -ls

Default version change procedure:

------------------------------------
Initial instalation procedure:
------------------------------------

1. Создать пользователя david и директорию /home/david
su
adduser david
usermod -aG sudo david
exit
su david
cd /home
mkdir ./david

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
pip list
pip freeze --local > requirements.txt
#deactivate

3. Создать директорию /home/david/log
mkdir ./log

4. Создать базу данных запустив скрипт david_db_create.py
python /home/david/david_db_create.py

5. Поместить в директорию /home/david файлы:
david_lib.py
david_web_server.py
david_unittest.py
david_climate_check.py
./VOICE_SAMPLES/

Пример для ubuntu win10
cp /mnt/c/Users/balob/Documents/DAVID/david_unittest.py /home/david/david_unittest.py

9. Запустить сервис для david_web_server.py
Поместить /etc/systemd/system/david.service
sudo systemctl daemon-reload
sudo systemctl enable foo.service
systemctl start david.service
systemctl status david.service

7. Добавить модули david_currency_check.py и david_climate_check.py в crontab
crontab -e
*/15 * * * * /home/david/env/bin/python /home/david/david_climate_check.py
0 17 */1 * 1-5 /home/david/env/bin/python /home/david/david_currency_check.py

7. Выполнить unit тестирование
sudo python /home/david/david_unittest.py


ps -aux | grep david_web_server
sudo screen -S climate_check
sudo python3.6 ./david/climate_check.py

**************************************************************************************************************************************************
Описание проекта (скрипты и контроллеры)
**************************************************************************************************************************************************

------------------------------------
Main server
------------------------------------

Рабочие (основные) модули Главного Компьютера
------------------------------------

Модуль david_web_server:
-----------------
Файл: david_web_server.py
Задача:
1. Принимает http запросы от микроконтроллеров.
2. Сохраняет полученные данные в базу данных.
3. Логирует события в файл.

Модуль climate_check
-----------------
Файл: climate_check.py
Задача:
1. Запрашивает климатические данные из базы данных david_db.sqlite.
2. Проигрывает голосовое оповещение в случае превышения заданных порогов.
3. Логирует события в файл.

Действия (для логирования):
а. Читает файлы.
б. Читает базу данных.
в. Проигрывает звуковой файл.

Модуль david_currency_check
-----------------
Файл: david_currency_check.py
Логика:
Если новое значение в процентном отношении больше предыдущего
или новое значение выходит за границы нормальных значений, идет информирование во WA.

Метод запуска:
crontab

Задача:
1. Получает курс валют с сайта ЦБРФ.
2. Записывает полученный курс в базу данных.
3. Проверяет изменения курса валют.
4. Информирует пользователя по WA об изменениях.

Действия (для логирования):
а. Выполняет http запрос.
б. Записывает в базу данных.
в. Читает базу данных. Выполняет проверку полученных данных.
г. Отправляет сообщение в WA.

Модуль "Список покупок" (проект)
-----------------
Модуль анализа речи подает сигнал на GPIO порт главного компьютера.
При получении сигнала с GPIO порта активируется программа, которая дает отклик, например: "Слушаю".
Далее по команде "Запиши в список покупок" переключается в подпрограмму записи покупок и выдает ответ: "Записываю".
Далее дается наименование товара.
Модуль произносит услашанное и ждет подтверждения.
Если подтверждение получено, наименование записывается в базу с датой создания и идентификатором списка покупок.
Должна быть реализована возможность закрывать список покупок и получать список покупок в виде речи и в виде сообщения в WhatsApp.

Вспомогательные модули Главного Компьютера
------------------------------------
Модуль david_unittest
-----------------
Файл: david_unittest.py

Метод запуска:
Ручной запуск

Задача:
1. Делает бэкап базы данных.
2. Выполняет тесты.
3. Восстанавливает базу данных из бэкапа.

Модуль david_lib
-----------------
Файл: david_lib.py

Метод запуска:
Импортируемая библиотека.

Задача:
1. Содержит переменные и функции, используемые другими модулями.

Модуль david_db_create
-----------------
Файл: david_db_create.py
Задача:
1. Создает базу данных david_db.sqlite.
2. Пересоздает базу данных david_db.sqlite.

Модуль voice_recorder
-----------------
Файл: voice_recorder.py
Задача:
Запись голосовых сэмплов для проигрывания на Главном Компьютере.

------------------------------------
Микроконтроллер NodeMcu01BedRoom
------------------------------------
Файл: NodeMcu01BedRoom.pde

Задача:
1. Считывает данные с датчика DHT11
2. Отправляет данные на Главный Компютер посредством http get запроса.

Элементная база:
1. NodeMcu,
2. DHT11 датчик температуры и влажности.

Схема подключения:

------------------------------------
Микроконтроллер NodeMcu02Gas
------------------------------------
Файл: 

Логика:

Задача:
1. Считывает данные с датчика газа.
2. Отправляет данные на Главный Компьютер посредством http get запроса.
http://192.168.1.44:80/gas;sensor=2&sensorValue=666

Элементная база: 

Схема подключения:

------------------------------------
Микроконтроллер NodeMcu03Door
------------------------------------
Файл: NodeMcu03Door.pde

Задача:
1. Считывает данные с датчика движения.
2. Отправляет события на Главный Компьютер посредством http get запросов.
3. Включает освещение по событиям с датчика движения.

Элементная база:
1. NodeMcu,
2. Датчик движения HC-SR505,
3. Светодиод "желтая линза" 5 мм.,
4. Резистор 100 Ом (2 шт.),
5. Адаптер питания на 5 В.,
6. Блок питания с разъемом 5.5 х 2.1.

Схема подключения:
NodeNCU D2 <-> R 100 Ом. <-> HC-SR505 (средний выход)
NodeNCU D1 <-> R 100 Ом. <-> Светодиод <-> NodeNCU Ground
NodeNCU VIN <-> Блок питания + (5 В.)
NodeNCU G <-> Блок питания - (0 В.)

------------------------------------
Микроконтроллер NodeMcu04Entrance (проект)
------------------------------------
Файл: 

Логика:
Датчик установлен в коридоре. При обнаружении движения включается светодиод и отправляется сообщение на главный компьютер.
Данные записываются в базу данных и логируются.
Далее идет проверка было ли в пределах 15-ти секунд перед этим срабатывание датчика NodeMcu03Door.
Если было, то через 25 секунд проигрывается приветствие.
В приветсвие можно добавить информацию о состоянии системы, климатические данные в квартире и пр. информацию.

Задача:
1. 
2. 
3. 

Элементная база:
1. NodeMcu,
2. Датчик движения HC-SR501,
3. Светодиод "желтая линза" 5 мм.,
4. Резистор 100 Ом (2 шт.),
5. AC-DC преобразователь 5 В.,

Схема подключения:

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

------------------------------------
Модуль (программа) Template
------------------------------------
Модуль <name>
-----------------
Файл: <name.py>
Логика:

Метод запуска:

Задача:
1. 
2. 
3. 

Действия (для логирования):
а. 
б. 
в. 

**************************************************************************************************************************************************
Основные принципы
**************************************************************************************************************************************************
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

------------------------------------
For everyday use
------------------------------------

sudo screen -S david_web_server
cd /home/david
source /home/david/env/bin/activate
python /home/david/david_web_server.py
python --version
Ctrl+A -> D
sudo screen -ls

cp /mnt/c/Users/balob/Documents/DAVID/david_unittest.py /home/david/david_unittest.py
cp /mnt/c/Users/balob/Documents/DAVID/david_lib.py /home/david/david_lib.py
cp /mnt/c/Users/balob/Documents/DAVID/david_web_server.py /home/david/david_web_server.py
cp /mnt/c/Users/balob/Documents/DAVID/david_currency_check.py /home/david/david_currency_check.py
