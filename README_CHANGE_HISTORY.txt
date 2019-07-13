------------------------------------
Version 0.4.0.dev change list and installation procedure:
------------------------------------
Модуль david_user_interface:
1. Добавлена возможность отправки почты.

Модуль Django Математика:
1. Сделатн отчет по успешно сданным циклам.

Модуль david_healthcheck:
1. Реализована отправка данных по mail.

Модуль david_web_server:
1. Добавлена отправка сообщения при обнаружении движения

Version 0.4.0 change procedure:

1. Сделать полную копию папки проекта.

2. Войти в виртуальное окружение проекта, установить библиотеки и сохранить requirements.txt.
source /home/david/env/bin/activate
pip freeze --local > requirements.txt
python --version

3. Поместить в директорию /home/david файлы:
(см. git diff --name-only master)

4. Обновить базу данных:
source /home/david/env/bin/activate
python /home/david/david_db_create.py

5. Перезапустить сервис david_web_server
systemctl stop david.service
systemctl start david.service
systemctl status david.service

6.  Перезагрузить папку WEB_UI запустить сервер
Предварительно поменяв путь в файле settings.py
Если нужно, применить миграции и загрузить недостающие данные в базу данных.
./WEB_UI
sudo screen -ls
sudo screen -d -r  30158.david_climate_check # вернуть скрин на передний план
sudo screen -S david_web_server # создать скрин
cd /home/david/WEB_UI
source /home/david/env/bin/activate
python manage.py runserver 0.0.0.0:8000
Ctrl+A -> D
sudo screen -ls

7. Загрузить данные в таблицу children_math_contest01
sqlite3 david_db.sqlite
INSERT INTO children_math_contest01
(task_description, answers_options, answer)
VALUES('Папе, маме и дочке вместе 70 лет. Сколько лет им будет вместе через 4 года?', '-', '82');
...

8. Выполнить unit тестирование
python /home/david/david_unittest.py

------------------------------------
Version 0.3.3 change list and installation procedure:
------------------------------------
Модуль Django Математика:
1. Добавлено оформление сайта с помощью bootstrap
------------------------------------
Version 0.3.2 change list and installation procedure:
------------------------------------
Модуль Django Математика:
1. Сделан bulk_create для решения проблемы неодновременной записи решений в базу данных.
2. Добавлены view в базу данных для работы с результатами выполнения задач task01
------------------------------------
Version 0.3.1 change list and installation procedure:
------------------------------------
Модуль Django Математика:
1. Быстрый фикс для проблемы одновременной работы двух пользователей.

------------------------------------
Version 0.3.0 change list and installation procedure:
------------------------------------

Нерешенные проблемы:
1. Как выполнить импорт модуля, находящегося в другой директории из файла в проекте Django?
import david_lib
Вариант решения:
https://stackoverflow.com/questions/24868733/how-to-access-a-module-from-outside-your-file-folder-in-python

Version 0.3.0 change procedure:

1. Войти в виртуальное окружение для программы и установить библиотеки.
source /home/david/env/bin/activate
pip install Django
pip install pandas
pip install numpy
pip install lxml
pip list
pip freeze --local > requirements.txt
python --version

2. Поместить в директорию /home/david файлы:
david_lib.py
david_user_interface.py
requirements.txt
test.py

3. Обновить базу данных:
python /home/david/david_db_create.py

4. Перезапустить сервис david_web_server
systemctl stop david.service
systemctl start david.service
systemctl status david.service

5. Создать Django проект и запустить сервер
5.1. Загрузить папку WEB_UI
./WEB_UI
5.2. Выполнить миграции
python manage.py migrate
5.3. Создать пользователя
python manage.py createsuperuser
5.4. Запустить проект
sudo screen -ls
sudo screen -d -r  30158.david_climate_check # вернуть скрин на передний план
Ctrl+C
exit
sudo screen -d -r 30137.david_web_server
sudo screen -S david_web_server
cd /home/david/WEB_UI
source /home/david/env/bin/activate
python manage.py runserver 0.0.0.0:8000
Ctrl+A -> D
sudo screen -ls

6. Выполнить unit тестирование
python /home/david/david_unittest.py

------------------------------------
Version 0.2.0 change list and installation procedure:
------------------------------------

Главный Компьютер:
1. Добавлены секунды в VIEW V_MOTION_SENSORS и V_CLIMATE_SENSORS.
2. Частично решена проблема с зависанием WA twilio использованием templates.
3. Добавлен UNIQUE для SENSOR_ID в таблицу SENSORS.

Модуль david_web_server:
1. Добавлен обработчик событий от Микроконтроллера NodeMcu02Gas.

Модуль david_healthcheck:
1. Дописать модуль.

Модуль climate_check:
1. Вынесены пороги температуры срабатывания в david_lib

Модуль NodeMcu02Gas:
1. Написать модуль.

Микроконтроллер NodeMcu02Gas
1. Сделана прошивка микроконтроллера.
2. Усиаерволен микроконтроллер NodeMcu02Gas

Version 0.2.0 change procedure:

0. Проверить, что все обновляемые скрипты имеют актуальные версии в заголовках.

1. Войти в виртуальное окружение для программы и установить библиотеки.
source /home/david/env/bin/activate
pip install psutil
pip list
pip freeze --local > requirements.txt
python --version

2. Поместить в директорию /home/david файлы:
david_unittest.py
david_lib.py
david_db_create.py
david_web_server.py
david_gas_check.py
david_healthcheck.py
david_currency_check.py
./VOICE_SAMPLES/gas_danger.mp3

3. Сделать backup базы данных и обновить ее запустив скрипт:
python /home/david/david_db_create.py

4. Переименоват копию backup базы данных (т.к. unittest перезапишет копию).

5. Перезапустить сервис david_web_server
systemctl stop david.service
systemctl start david.service
systemctl status david.service

6. Выполнить unit тестирование
python /home/david/david_unittest.py

7. Добавить модуль david_gas_check.py в crontab
crontab -e
*/15 * * * * /home/david/env/bin/python /home/david/david_gas_check.py

------------------------------------
Version 0.0.2 change list and installation procedure:
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
deactivate

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
Version 0.0.1 change list and installation procedure:
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

------------------------------------
Initial installation procedure:
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
pip install psutil
pip list
pip freeze --local > requirements.txt
deactivate

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

5.  Перезагрузить папку WEB_UI запустить сервер
Предварительно поменяв путь в файле settings.py
Если нужно, применить миграции и загрузить недостающие данные в базу данных.
python manage.py migrate
./WEB_UI
sudo screen -ls
sudo screen -d -r  30158.david_climate_check # вернуть скрин на передний план
sudo screen -S david_web_server # создать скрин
cd /home/david/WEB_UI
source /home/david/env/bin/activate
python manage.py runserver 0.0.0.0:8000
Ctrl+A -> D
sudo screen -ls

7. Загрузить данные в таблицу children_math_contest01
sqlite3 david_db.sqlite
INSERT INTO children_math_contest01
(task_description, answers_options, answer)
VALUES('Папе, маме и дочке вместе 70 лет. Сколько лет им будет вместе через 4 года?', '-', '82');
...

7. Добавить модули david_currency_check.py, david_healthcheck.py и david_climate_check.py в crontab
crontab -e
*/15 * * * * /home/david/env/bin/python /home/david/david_climate_check.py
0 17 */1 * 1-5 /home/david/env/bin/python /home/david/david_currency_check.py
0 18 */1 * * /home/david/env/bin/python /home/david/david_healthcheck.py

7. Выполнить unit тестирование
sudo python /home/david/david_unittest.py