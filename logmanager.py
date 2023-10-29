"""
logmanager, setus up application logging. use the **logger** property to
write to the log.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from settings import settings

# Ensure log directory exists
log_dir = os.path.dirname(settings['logging']['logfilepath'])
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger(settings['logging']['logappname'])
"""
Usage:\n
**logger.info('message')** for info messages\n
**logger.warning('message')** for warnings\n
**logger.error('message')** for errors\n
**logger.debug('message')** for debugging info

"""

if settings['logging']['level'].lower() == 'debug':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

LogFile = RotatingFileHandler('%s%s.log' %(settings['logging']['logfilepath'],settings['logging']['logappname']),
                              maxBytes=1048576, backupCount=10)
formatter = logging.Formatter('%(asctime)s, %(name)s, %(levelname)s : %(message)s')
LogFile.setFormatter(formatter)
logger.addHandler(LogFile)
logger.info('Logging level set to: %s',settings['logging']['level'].upper())
