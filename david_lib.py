from os.path import isfile
from typing import Dict
from logging import Logger

version = '0.11.0'
currency_threshold_increase_per = 2
currency_usd_threshold_high = 80
currency_usd_threshold_low = 70
tickers_foreign = ['AAPL-RM', 'AMZN-RM', 'GOOG-RM', 'MSFT-RM']
tickers_russian = ['SBER', 'GMKN', 'LKOH', 'MAIL', 'YNDX']
climate_cold_threshold = 19
climate_hot_threshold = 25
gas_emergency_threshold = 600

# DavidServer

# ip_addr = '192.168.1.44'
# port = 80
# ftp_ip_addr = '192.168.1.1'
# timer_gas_mail_delay = 60  # Time interval to send mail in case of gas emergency
# timer_oven_mail_delay = 60  # Time interval to send mail in case of oven emergency
# ftp_db_backup_dir = 'Transcend/david/db_backup'
# dir_david = r'/home/david'
# mp3_files_dict: Dict[str, str] = {
#     'climate_hot_bedroom': r'./VOICE_SAMPLES/climate_hot_bedroom.mp3',
#     'climate_cold_bedroom': r'./VOICE_SAMPLES/climate_cold_bedroom.mp3',
#     'gas_danger': r'./VOICE_SAMPLES/gas_danger.mp3',
#     'check_oven': r'./VOICE_SAMPLES/check_oven.mp3'
# }
# file_sqlite_db = r'david_db.sqlite'
# file_log_web_server = r'./log/david_web_server.log'
# file_log_climate_check = r'./log/climate_check.log'
# file_log_currency_check = r'./log/currency_check.log'
# file_log_gas_check = r'./log/gas_check.log'
# file_log_healthcheck = r'./log/healthcheck.log'
# file_log_user_interface = r'./log/user_interface.log'

# For tests

ip_addr = '192.168.1.52'
port = 80
ftp_ip_addr = '192.168.1.1'
timer_gas_mail_delay = 6  # Time interval to send mail in case of gas emergency
timer_oven_mail_delay = 6  # Time interval to send mail in case of oven emergency
ftp_db_backup_dir = 'Transcend/david/db_backup'
dir_david = r'c:\Users\balob\Downloads\DAVID'
mp3_files_dict: Dict[str, str] = {
    'climate_hot_bedroom': r'.\VOICE_SAMPLES\climate_hot_bedroom.mp3',
    'climate_cold_bedroom': r'.\VOICE_SAMPLES\climate_cold_bedroom.mp3',
    'gas_danger': r'.\VOICE_SAMPLES\gas_danger.mp3',
    'check_oven': r'.\VOICE_SAMPLES\check_oven.mp3'
}
file_sqlite_db = r'david_db.sqlite'
file_log_web_server = r'.\log\david_web_server.log'
file_log_climate_check = r'.\log\climate_check.log'
file_log_currency_check = r'.\log\currency_check.log'
file_log_gas_check = r'.\log\gas_check.log'
file_log_healthcheck = r'.\log\healthcheck.log'
file_log_user_interface = r'.\log\user_interface.log'


def check_file(logger_name: Logger, file_name: str) -> None:
    """
    **Description**

    This is to check if the file exists.
    The check result will be stored in log file.

    :param logger_name: Logger name to log the check result.
    :param file_name: The file name to check if exists.
    :return: None
    """
    if isfile(file_name):
        logger_name.info(f'Message=check_file;File={file_name};Result=exists')
    else:
        logger_name.error(f'Message=check_file;File={file_name};Result=does_not_exist')
    return None
