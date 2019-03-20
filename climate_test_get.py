# Тестовая отправка GET запросов

import requests
#payload = {'key1':'value1','key2':'value2'}
r = requests.get('http://192.168.1.52:80/connected;sensor=1&ip=192.168.1.63')
r = requests.get('http://192.168.1.52:80/climate;sensor=1&readattempt=10&temperature=nan&humidity=nan')
r = requests.get('http://192.168.1.52:80/climate;sensor=1&readattempt=10&temperature=10.0&humidity=20.0')
print('Status: ',r.status_code,'\n',r.text)
r.close()