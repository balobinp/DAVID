#python3.6
#Author: balobin.p@mail.ru

from os.path import isfile, join
import logging
import david_lib

from twilio.rest import Client

dir_david = david_lib.dir_david
file_log_user_interface = david_lib.file_log_user_interface
file_log_user_interface_path = join(dir_david, file_log_user_interface)
file_sqlite_db = david_lib.file_sqlite_db
file_sqlite_db_path = join(dir_david, file_sqlite_db)

# Create logger
user_interface_log = logging.getLogger('user_interface')
user_interface_log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s;Application=%(name)s;%(levelname)s;%(message)s')
file_handler = logging.FileHandler(file_log_user_interface_path)
file_handler.setFormatter(formatter)
user_interface_log.addHandler(file_handler)

# Logger levels

# user_interface_log.debug(f'Message=;')
# user_interface_log.info(f'Message=;')
# user_interface_log.warning(f'Message=;')
# user_interface_log.error(f'Message=;')
# user_interface_log.critical(f'Message=;')

# Logger examples
# Действия (для логирования):
# а. get_task
# user_interface_log.debug(f'Message=get_task;')
#
# б. inform_user_attempt
# user_interface_log.debug(f'Message=inform_user_attempt;')
#
# в. inform_user_result
# user_interface_log.debug(f'Message=inform_user_result;')

def check_file(file_name):
    if isfile(file_name):
        return None
    else:
        user_interface_log.error(f'Message=check_file;File={file_name};Result=does_not_exist')
    return None

def inform_user_pavel_wa(key, value):
    try:
        account_sid = 'AC431b47a9c6b392bc8b5f38ccfe666a96'
        auth_token = 'df57cfe7d1b42d1eaf492fefc4c848af'
        client = Client(account_sid, auth_token)
        body = f'Your {key} code is {value}'
        message = client.messages.create(body=body,
                                         from_='whatsapp:+14155238886',
                                         to='whatsapp:+79217428080')
        result = 'successful'
    except Exception as e:
        user_interface_log.error(f'Message=send_wa_notify;Exception={e}')
        result = 'unsuccessful'
    return result

class InformUser:
    def __init__(self):
        check_file(file_sqlite_db_path)
        check_file(file_log_user_interface_path)
        print('Class InformUser is constructed')

    def pavel(self):
        result = inform_user_pavel_wa('Hello', 'world')
        print(result)

if __name__ == '__main__':
    pass