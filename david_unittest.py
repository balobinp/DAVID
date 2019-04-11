import unittest
import requests

server_ip_addr = '192.168.1.52'

class TestWebServer(unittest.TestCase):
    
    def test_get_connect(self):
        url = f'http://{server_ip_addr}:80/connected;sensor=1&ip=192.168.1.63'
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, 'OK')
        
    def test_get_climate(self):
        url = f'http://{server_ip_addr}:80/climate;sensor=1&readattempt=10&temperature=24.0&humidity=35.0'
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, 'OK')
        
suite = unittest.TestLoader().loadTestsFromTestCase(TestWebServer)
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)