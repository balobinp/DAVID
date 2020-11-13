#python3.6
#Author: balobin.p@mail.ru

from os.path import isfile, join
import logging
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from typing import List

import david_lib

dir_david = david_lib.dir_david
file_pass_path = join(dir_david, 'david_pass.json')
file_log_user_interface = david_lib.file_log_user_interface
file_log_user_interface_path = join(dir_david, file_log_user_interface)
file_sqlite_db = david_lib.file_sqlite_db
file_sqlite_db_path = join(dir_david, file_sqlite_db)
mp3_files_dict = david_lib.mp3_files_dict

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
# user_interface_log.debug(f'Message=get_task;Class=;')
#
# б. inform_user_attempt
# user_interface_log.debug(f'Message=inform_user_attempt;Class=;Method=;')
#
# в. inform_user_result
# user_interface_log.debug(f'Message=inform_user_result;Class=;Method=;')


def check_file(file_name):
    if isfile(file_name):
        return None
    else:
        user_interface_log.error(f'Message=check_file;File={file_name};Result=does_not_exist')
    return None


class InformUser:

    def __init__(self, mp3_files_dict_=mp3_files_dict, dir_david_=dir_david, check_file_=check_file):
        check_file_(file_sqlite_db_path)
        check_file_(file_log_user_interface_path)
        check_file_(file_pass_path)
        self.mp3_files_dict = mp3_files_dict_
        self.dir_david = dir_david_
        user_interface_log.info(f'Message=get_task;Class=InformUser;Result=constructed.')

        with open(file_pass_path, "r") as json_file:
            self.passwords = json.load(json_file)

    def mail(self, subject: str, html_message: str, receiver_mail_list: List[str]) -> bool:
        """
        To inform user by mail.

        :param subject:
            The Subject of mail.
        :param html_message:
            The message body in html format.
        :param receiver_mail_list:
            The list of mail destination addresses.

        :return:
            Returns True in case of success and False otherwise.
        """
        user_interface_log.info(f'Message=inform_user_attempt;Class=InformUser;Method=mail;Called with subject: {subject}')
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        gmail_account = "balobin.p@gmail.com"
        gmail_password = self.passwords['gmail_password'] # Отв1
        receiver_email = receiver_mail_list # "balobin.p@mail.ru"  # Enter receiver address
        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = gmail_account
        message["To"] = ", ".join(receiver_email)
        html_message_body = MIMEText(html_message, "html")
        message.attach(html_message_body)
        context = ssl.create_default_context()
        result = False
        try:
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(gmail_account, gmail_password)
                server.sendmail(gmail_account, receiver_email, message.as_string())
            result = True
            user_interface_log.info(f'Message=inform_user_result;Class=InformUser;Method=mail;Result={result};Subject={subject}')
        except Exception as e:
            user_interface_log.error(f'Message=inform_user_result;Class=InformUser;Method=mail;Result={result};Subject={subject}')
        return result

    def play_file(self, mp3_file: str) -> bool:
        """
        To inform user by voice. It uses stored mp3 files.

        :param mp3_file:
            Specifies the predefined mp3 file to play.
            Allowed values are listed in david_lib.mp3_files_dict.

        :return:
            Returns True in case of success and False otherwise.
        """
        user_interface_log.debug(f'Message=inform_user_attempt;Class=InformUser;Method=play_file;Message={mp3_file}')
        result = False
        if mp3_file in self.mp3_files_dict.keys():
            try:
                os.system("sudo mpg123 " + join(self.dir_david, self.mp3_files_dict[mp3_file]))
                user_interface_log.info(
                    f'Message=inform_user_result;Class=InformUser;Method=play_file;Result={result};Message={mp3_file}')
                result = True
            except Exception as e:
                user_interface_log.error(
                    f'Message=inform_user_result;Class=InformUser;Method=play_file;Result={result};Exception={e}')
        else:
            user_interface_log.error(
                f'Message=inform_user_result;Class=InformUser;Method=play_file;Result={result};Unknown mp3 file.')
        return result


if __name__ == '__main__':
    pass
