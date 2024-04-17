"""
logmanager, setus up application logging. use the **logger** property to
write to the log.
"""
import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from app_control import settings

# Ensure log directory exists
log_dir = os.path.dirname(settings['logging']['logfilepath'])
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger(settings['logging']['logappname'])
"""Usage:
**logger.info('message')** for info messages
**logger.warning('message')** for warnings
**logger.error('message')** for errors
**logger.debug('message')** for debugging info"""


if settings['logging']['level'].upper() == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

LogFile = RotatingFileHandler('%s%s.log' %(settings['logging']['logfilepath'],settings['logging']['logappname']),
                              maxBytes=1048576, backupCount=10)
formatter = logging.Formatter('%(asctime)s, %(name)s, %(levelname)s : %(message)s')
LogFile.setFormatter(formatter)
logger.addHandler(LogFile)
try:
    LogFile.doRollover()
except PermissionError:
    logger.warning('log file was already open')
logger.info('Runnng Python %s on %s', sys.version, sys.platform)
logger.info('Logging level set to: %s',settings['logging']['level'].upper())
