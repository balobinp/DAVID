# std usecase
import logging
logger = logging.Logger('test')
logger.setLevel(logging.DEBUG)
logger.debug('Level 1. Debug message')
logger.info('Level 2. info message')
logger.warning('Level 3. warn message')
logger.error('Level 4. error message')
logger.critical("Level 5. critical message")

# http usecase
import logging
logger = logging.Logger('test_http')
http_hdlr = logging.HttpHandler('192.168.1.63', 80)
logger.addHandler(http_hdlr)
logger.setLevel(logging.DEBUG)
logger.debug('Level 1 Debug message')
logger.info('Level 2 info message')
logger.warning('Level 3 warn message')
logger.error('Level 4 error message')
logger.critical("Level 5 critical message")