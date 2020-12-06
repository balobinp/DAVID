#python3.6
#Author: balobin.p@mail.ru

from os.path import isfile, join
import logging
import david_lib
from david_lib import check_file

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


if __name__ == '__main__':
    check_file(temp_log, file_sqlite_db_path)
    check_file(temp_log, file_log_temp_path)
