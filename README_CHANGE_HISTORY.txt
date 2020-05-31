------------------------------------
Version 0.7.0.dev change list and installation procedure:
------------------------------------

Главный Компьютер:
1. Добавлены VIEW для неправильных глаговов в базу данных.
2. Добавлена информация о прогрессе выполнения задания для неправильных глаголов.
3. Добавлено измерение температуры процессора Raspberry Pi в david_healthcheck.py
4. Добавлены бэкапы базы данных на ftp сервер.
5. Все модули из Cron переведены на systemd
6. Все пароли в david_pass.json
7. WEB_UI переведен на systemd

Модуль david_healthcheck:
1. Исправлена дату с учетом часового пояса для "Motion detected".

Микроконтроллер NodeMcu01BedRoom:
1. Выполнен перевод на MicroPython с добавлением дисплея (Ver.02)
2. Сделана поправка температуры -3.6 С.

Микроконтроллер NodeMcu02Gas:
1. Выполнен перевод на MicroPython с добавлением дисплея и дополнительных датчиков (Ver.02)
2. Сделана поправка температуры -2 С

Version installation procedure:
1. Указать юзернейм и пароль ftp сервера в david_pass.json
2. Указать ftp ip адрес в david_lib.py
3. Сделать прошивку модуля NodeMcu01BedRoom
4. Обновить psutil from 5.6.2 to 5.6.6
5. Обновить werkzeug from 0.15.2 to 0.15.3
6. Upgrade urllib3 to version 1.24.2

------------------------------------
Version 0.6.0.dev change list and installation procedure:
------------------------------------

Модуль david_gas_check:
1. В логгере заменен t на GasSensorValue

Модуль david_healthcheck:
1. Реализована проверка двух и более датчиков температуры.

Модуль Django:
1. Добавлены неправильные глаголы

Installation procedure:
cd ./WEB_UI
python manage.py makemigrations english
python manage.py sqlmigrate english 0001
python manage.py migrate english

INSERT INTO english_irregularverbs
(infinitive, past, participle, "translation")
VALUES
('get', 'got', 'gotten', 'получать'),
('take', 'took', 'taken', 'брать'),
('go', 'went', 'gone', 'идти'),
('sit', 'sat', 'sat', 'сидеть'),
('spend', 'spent', 'spent', 'тратить');

------------------------------------
Version 0.5.0 change list and installation procedure:
------------------------------------

Модуль david_web_server:
1. Сделана обработка получения версии прошивки от датчиков
2. Сделана обработка получения аварийных сообщений от датчика газа с оповещением по мэйлу.

Модуль david_user_interface:
1. Пароль от почты вынесен во внешний json файл
2. Добавлена возможность отправки html в майл.

Микроконтроллер NodeMcu01BedRoom:
1. Заменен датчик DHT11 на DHT22.
2. Вынесены номер сенсора и IP главного компютрера в переменные.
3. В http запрос connect добавлена версия прошивки.

Микроконтроллер NodeMcu02Gas:
1. Добавлена отправки аварийных сообщений и поддержка светодиодов
2. Вынесены номер сенсора и IP главного компютрера в переменные.
3. В http запрос connect добавлена версия прошивки.

Модуль Django:
1. Добавлено тестирование для children_math и mainpage
/david/WEB_UI>python manage.py test children_math.tests
/david/WEB_UI>python manage.py test mainpage.tests
2. Исправлена проблема с неправильным отображением прогресса выполнения задач Math task
3. Добавлено умножение в math_task01

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
Main Version change procedure
------------------------------------

0. Проверить, что все обновляемые скрипты имеют актуальные версии в заголовках.
README.md
david_lib.py

1. Сделать полную копию папки проекта.

2. Войти в виртуальное окружение проекта, установить библиотеки и сохранить requirements.txt.
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
Предварительно поменяв путь в файле settings.py
Если нужно, применить миграции и загрузить недостающие данные в базу данных.
cd ./WEB_UI
sudo screen -ls
sudo screen -d -r 4932.david_web_server # вернуть скрин на передний план
sudo screen -S david_web_server # создать скрин, если нужно
cd /home/david/WEB_UI
Остановить Django
Перезагрузить папку ./WEB_UI
Выполнить миграции:
python manage.py makemigrations english
python manage.py sqlmigrate english 0001
python manage.py migrate english
source /home/david/env/bin/activate
python manage.py runserver 0.0.0.0:8000
Ctrl+A -> D
sudo screen -ls

7. Загрузить данные в таблицы, если нужно
sqlite3 david_db.sqlite
INSERT INTO children_math_contest01
(task_description, answers_options, answer)
VALUES('Папе, маме и дочке вместе 70 лет. Сколько лет им будет вместе через 4 года?', '-', '82');

7. Добавить модули в crontab
crontab -e
*/15 * * * * /home/david/env/bin/python /home/david/david_climate_check.py
0 17 */1 * 1-5 /home/david/env/bin/python /home/david/david_currency_check.py
*/15 * * * * /home/david/env/bin/python /home/david/david_gas_check.py
0 18 */1 * * /home/david/env/bin/python /home/david/david_healthcheck.py

8. Выполнить unit тестирование
python /home/david/david_unittest.py
cd /home/david/WEB_UI
python manage.py test children_math.tests
python manage.py test mainpage.tests

9. Завершить
deactivate
exit

------------------------------------
Main initial installation procedure:
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
systemctl start david.service
systemctl status david.service

Проверить, что сервер слушает порт:
(env) david@david:~$ sudo netstat -ltnp | grep :80
tcp        0      0 0.0.0.0:8000            0.0.0.0:*               LISTEN      3570/python
tcp        0      0 192.168.1.44:80         0.0.0.0:*               LISTEN      3794/python

9. Запустить сервис для david_climate_check.py

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
sudo python /home/david/david_unittest.py
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
