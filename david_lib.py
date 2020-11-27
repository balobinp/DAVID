# python3.6

from typing import Dict

version = '0.10.4'
currency_threshold_increase_per = 2
currency_usd_threshold_high = 67
currency_usd_threshold_low = 63
tickers_foreign = ['AAPL-RM', 'AMZN-RM', 'GOOG-RM', 'MSFT-RM']
tickers_russian = ['SBER', 'GMKN', 'LKOH', 'MAIL', 'YNDX']
climate_cold_threshold = 20
climate_hot_threshold = 25
gas_emergency_threshold = 600

# DavidServer

ip_addr = '192.168.1.44'
port = 80
ftp_ip_addr = '192.168.1.1'
timer_gas_mail_delay = 60  # Time interval to send mail in case of gas emergency
timer_oven_mail_delay = 60  # Time interval to send mail in case of oven emergency
ftp_db_backup_dir = 'Transcend/david/db_backup'
dir_david = r'/home/david'
mp3_files_dict: Dict[str, str] = {
    'climate_hot_bedroom': r'./VOICE_SAMPLES/climate_hot_bedroom.mp3',
    'climate_cold_bedroom': r'./VOICE_SAMPLES/climate_cold_bedroom.mp3',
    'gas_danger': r'./VOICE_SAMPLES/gas_danger.mp3',
    'check_oven': r'./VOICE_SAMPLES/check_oven.mp3'
}
file_sqlite_db = r'david_db.sqlite'
file_log_web_server = r'./log/david_web_server.log'
file_log_climate_check = r'./log/climate_check.log'
file_log_currency_check = r'./log/currency_check.log'
file_log_gas_check = r'./log/gas_check.log'
file_log_healthcheck = r'./log/healthcheck.log'
file_log_user_interface = r'./log/user_interface.log'

# For tests

# ip_addr = '192.168.1.53'
# port = 80
# ftp_ip_addr = '192.168.1.1'
# timer_gas_mail_delay = 6  # Time interval to send mail in case of gas emergency
# timer_oven_mail_delay = 6  # Time interval to send mail in case of oven emergency
# ftp_db_backup_dir = 'Transcend/david/db_backup'
# dir_david = r'c:\Users\balob\Downloads\DAVID'
# mp3_files_dict: Dict[str, str] = {
#     'climate_hot_bedroom': r'.\VOICE_SAMPLES\climate_hot_bedroom.mp3',
#     'climate_cold_bedroom': r'.\VOICE_SAMPLES\climate_cold_bedroom.mp3',
#     'gas_danger': r'.\VOICE_SAMPLES\gas_danger.mp3',
#     'check_oven': r'.\VOICE_SAMPLES\check_oven.mp3'
# }
# file_sqlite_db = r'david_db.sqlite'
# file_log_web_server = r'.\log\david_web_server.log'
# file_log_climate_check = r'.\log\climate_check.log'
# file_log_currency_check = r'.\log\currency_check.log'
# file_log_gas_check = r'.\log\gas_check.log'
# file_log_healthcheck = r'.\log\healthcheck.log'
# file_log_user_interface = r'.\log\user_interface.log'