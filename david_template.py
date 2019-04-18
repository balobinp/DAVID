#python3.6
#Author: balobin.p@mail.ru

from os.path import isfile
import logging
#from importlib import reload

#reload(logging)

file_log = r'/home/david/log/<file name>.log'

# Create logger
logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(asctime)s;Application=%(name)s;%(levelname)s;%(message)s')
<log name> = logging.getLogger('<logger name>')

# Logger examples

#<log name>.debug(f'Message=;')
#<log name>.info(f'Message=;')
#<log name>.warning(f'Message=;')
#<log name>.error(f'Message=;')
#<log name>.critical(f'Message=;')

def check_file(file_name):
    if isfile(file_name):
        <log name>.info(f'Message=check_file;File={file_name};Result=exists')
    else:
        < log name >.error(f'Message=check_file;File={file_name};Result=does_not_exist')
    return None

check_file(file_log)