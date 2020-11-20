------------------------------------
Version 0.10.1.dev change list and installation procedure:
------------------------------------

Главный Компьютер:
1.

Модуль david_web_server:
1. Добавлены методы оповещения голосом о превышении уровня газа и стоящей на плите посуде (201012).

Справочник david_lib:
1. Файлы mp3 заменены на справочник (201012)
2. Добавлен gas_emergency_threshold (201016)

Модуль david_currency_check:
1. Добавлены котировки акций (201005)
2. Добавлена котировка LAST (201106)

Модуль david_user_interface:
1. Изменен return на bool в методе InformUser.mail (201012).
2. Добавлен метод оповещения play_file (201012).

Модуль climate_check:
1. Заменен метод оповещения на david_user_interface (201016)

Модуль david_gas_check:
1. Заменен метод оповещения на david_user_interface (201016)
2. Добавлен gas_emergency_threshold из david_lib (201016)

Микроконтроллер NodeMcu01BedRoom:
1.

Микроконтроллер NodeMcu02Gas:
1. Сделан обработчик отсутствия дисплея (201018)
2. Добавлены тесты отсутствия дисплея (201019)

Микроконтроллер NodeMcu03Door:
1. Добавлен выход для TX / RX на плате (201109)
2. Добавлены притягивающие к земле резисторы на плате для пинов motion, чтобы по умолчанию подавался ноль (201109)
3. Управляющий Q5 Pin перенесен с I02 на I00 на плате (201109)

Version installation procedure:

1. Заменить файлы контроллера NodeMcu02Gas

------------------------------------
Version 0.9.0.dev change list and installation procedure:
------------------------------------

Главный Компьютер:
1.

Модуль david_web_server:
1. Добавлен класс Timer для контроля периодичности отправки emergency mail gas и oven (200921)
2. Выполнен переход на FastAPI с async (200925)

Микроконтроллер NodeMcu01BedRoom:
1.

Микроконтроллер NodeMcu02Gas:
1.

Version installation procedure:

1. Установить библиотеки
pip install fastapi
pip install uvicorn

2. Обновить requirements.txt
pip freeze > requirements.txt

------------------------------------
Version 0.8.0 change list and installation procedure:
------------------------------------

Главный Компьютер:
1. david_web_server.py отправка нотификации по мэйлу только для sensor_id == '3': # NodeMcu03Door
2. Добавлена обработка get запроса от контроллера NodeMcu02Gas о стоящей на газу посуде (200904)
3. david_web_server.py методы обработки GET запросов выведены в отдельный класс (200911)

Микроконтроллер NodeMcu01BedRoom:
1. Сделана синхронизация времени в boot (200712)
2. Цикл переведен на utime.ticks_diff (200717)
3. Добавлено время на дисплей (200717)
4. Сделана точка весто Server OK (200717)
5. Сделана регулярная синхронизация времени (200717)
6. Добавлен gc.collect (200717)

Микроконтроллер NodeMcu02Gas:
1. Добавлена отправка оповещения на Главный компьютер о движении.
2. Выход управления реле заменен с D4 на D0
3. Удален buzzer (200606)
4. Добавлен gc.collect() (200606)
5. Поставлен датчик DHT22 (200706)
6. Исправлено отображение на дисплее данных температуры и влажности с точкой (200706)
7. Добавлена точку на дисплей в случае успешной отправки данных по газу на сервер согласно схеме дисплея (200706)
8. Сделан пересчет уровня газа в проценты по формуле (200706)
9. Исправлена ошибка очистки точки при отправке http запроса (200706)

Version installation procedure:

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
