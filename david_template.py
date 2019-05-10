#python3.6
#Author: balobin.p@mail.ru

from os.path import isfile, join
import logging
import david_lib

dir_david = david_lib.dir_david
file_log_temp = david_lib.file_log_name_temp
file_log_temp_path = join(dir_david, file_log_temp)
file_sqlite_db = david_lib.file_sqlite_db
file_sqlite_db_path = join(dir_david, file_sqlite_db)

# Create logger
temp_log = logging.getLogger('climate_check')
temp_log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s;Application=%(name)s;%(levelname)s;%(message)s')
file_handler = logging.FileHandler(file_log_temp_path)
file_handler.setFormatter(formatter)
temp_log.addHandler(file_handler)

# Logger levels

# temp_log.debug(f'Message=;')
# temp_log.info(f'Message=;')
# temp_log.warning(f'Message=;')
# temp_log.error(f'Message=;')
# temp_log.critical(f'Message=;')

# Logger examples
# Действия (для логирования):
# а. check_file
# temp_log.debug(f'Message=check_file;')

# б. get_data_from_db
# temp_log.debug(f'Message=get_data_from_db;')

# в. play_audio
# temp_log.debug(f'Message=play_audio;')

def check_file(file_name):
    if isfile(file_name):
        return None
    else:
        temp_log.error(f'Message=check_file;File={file_name};Result=does_not_exist')
    return None

if __name__ == '__main__':
    check_file(file_sqlite_db_path)
    check_file(file_log_temp_path)