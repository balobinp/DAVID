#python3.6
#Author: balobin.p@mail.ru

from os.path import isfile, join
import logging

import david_lib

dir_david = david_lib.dir_david
file_log = 'temp.log'
file_log_path = join(dir_david, file_log)

# Create logger
temp_log = logging.getLogger('climate_check')
temp_log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s;Application=%(name)s;%(levelname)s;%(message)s')
file_handler = logging.FileHandler(file_log_path)
file_handler.setFormatter(formatter)
temp_log.addHandler(file_handler)

# Logger examples

#<log name>.debug(f'Message=;')
#<log name>.info(f'Message=;')
#<log name>.warning(f'Message=;')
#<log name>.error(f'Message=;')
#<log name>.critical(f'Message=;')

def check_file(file_name):
    if isfile(file_name):
        return None
    else:
        temp_log.error(f'Message=check_file;File={file_name};Result=does_not_exist')
    return None

check_file(file_log)