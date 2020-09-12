import sys
import urequests
from machine import RTC

rtc = RTC()

CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10

_level_dict = {
    CRITICAL: "CRIT",
    ERROR: "ERRO",
    WARNING: "WARN",
    INFO: "INFO",
    DEBUG: "DEBG",
}

_ip=None
_port=None
_stream = 'std'
# _stream = sys.stderr

class Logger:

    def __init__(self, name):
        self.level = INFO
        self.handlers = []
        self.name = name

    def setLevel(self, level):
        self.level = level

    def addHandler(self, hdlr):
        try:
            if not (hdlr in self.handlers):
                self.handlers.append(hdlr)
        except:
            raise

    def log(self, level, msg):
        if level >= self.level:
            t = rtc.datetime()
            t_frm = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}:{:03d};"\
                    .format(t[0], t[1], t[2], t[4], t[5], t[6], t[7])
            l_msg = "{};{};{}".format(_level_dict.get(level), self.name, msg)
            sys.stderr.write(t_frm)
            print(l_msg, file=sys.stderr)
            for hdlr in self.handlers:
                hdlr.emit(t_frm, l_msg)

    def debug(self, msg):
        self.log(DEBUG, msg)

    def info(self, msg):
        self.log(INFO, msg)

    def warning(self, msg):
        self.log(WARNING, msg)

    def error(self, msg):
        self.log(ERROR, msg)

    def critical(self, msg):
        self.log(CRITICAL, msg)

    def exc(self, e, msg):
        self.log(ERROR, msg)
        sys.print_exception(e, _stream)

    def exception(self, msg):
        self.exc(sys.exc_info()[1], msg)


class FileHandler:
    def __init__(self):
        pass


class HttpHandler:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def emit(self, t, record):
        try:
            r = urequests.get('http://{0}:{1}/{2}'.format(self.ip, self.port, record.replace(" ", '')))
            r.close()
        except:
            raise