import david_user_interface
import datetime as dt

try:
    dt_now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"Subject: Motion detected {dt_now}\n"
    message += f"David indore motion detected at {dt_now}"
    inform_user_mail = david_user_interface.InformUser()
    inform_user_mail.mail(message, ["balobin.p@mail.ru", "pavel@roamability.com"])
except Exception as e:
    print(e)