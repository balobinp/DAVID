from fastapi import BackgroundTasks, FastAPI, HTTPException
import uvicorn
import datetime as dt
from time import sleep
from urllib.parse import parse_qs, urlparse

import david_user_interface

inform_user_mail = david_user_interface.InformUser()

def send_mail():
    try:
        dt_now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        subject = f"Test message {dt_now}"
        message = f"Test message {dt_now}"
        inform_user_mail.mail(subject, message, ["balobin.p@mail.ru", "pavel@roamability.com"])
        print(f'Message=inform_user_mail;Sensor=1;Sent=done')
        sleep(1)
    except Exception as e:
        print(f'Message=inform_user_mail;Exception={e}')

def get_request_handler(url_parameters):
    get_url = urlparse(url_parameters)
    get_params = parse_qs(get_url.params, keep_blank_values=True)
    return get_url, get_params

app = FastAPI()

@app.get("/{parameters}")  # to read data.
async def get(parameters: str, background_tasks: BackgroundTasks):
    get_url, get_params = get_request_handler(parameters)
    # print(get_url, get_params)
    # if item_id == 4:
    #     raise HTTPException(status_code=404)
    # else:
    #     pass
    #     # background_tasks.add_task( send_mail )
    # return 'OK', 200
    return {"message": "OK", "get_url": get_url.path, "get_params": get_params, "sensor": get_params.get('sensor')[0]}

if __name__ == "__main__":
    uvicorn.run("test:app", host="127.0.0.1", port=8000, log_level="info")
