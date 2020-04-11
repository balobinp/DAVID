import ftplib
import json
from os.path import join
import datetime as dt

import david_lib

dir_david = david_lib.dir_david
ftp_ip_addr = david_lib.ftp_ip_addr
file_pass_path = join(dir_david, 'david_pass.json')
file_sqlite_db = david_lib.file_sqlite_db
file_sqlite_db_path = join(dir_david, file_sqlite_db)

def make_db_backup_ftp():
    ftp_backup_dir = r'Transcend/david/db_backup'
    with open(file_pass_path, "r") as json_file:
        passwords = json.load(json_file)
    ftp_user = passwords['ftp_user']
    ftp_pass = passwords['ftp_pass']
    try:
        ftp = ftplib.FTP(ftp_ip_addr)
        ftp.login(ftp_user, ftp_pass)
        file_sqlite_db_backup = f'david_db_{dt.datetime.now().strftime("%Y%m%d")}.sqlite'
        ftp.storbinary('STOR ' + f'{ftp_backup_dir}/{file_sqlite_db_backup}', open(file_sqlite_db_path, 'rb'))
        ftp.cwd(ftp_backup_dir)
        db_backups = ftp.nlst()
        db_backups.sort()
        for db_backup in db_backups[:-3]:
            ftp.delete(db_backup)
        db_backups = ftp.nlst()
        db_backups.sort()
        ftp.quit()
    except Exception as e:
        db_backups = None
    return db_backups

if __name__ == '__main__':
    db_backups = make_db_backup_ftp()