"""
Application logging configuration and setup module.

This module initializes and configures the logging system for the application,
including file rotation, formatting, and log level management. It provides a
centralized logger instance that can be imported and used throughout the application.

Features:
    - Automatic log directory creation
    - Rotating file handler with configurable size limits and backup count
    - Configurable logging levels (DEBUG/INFO)
    - Standardized log message formatting with timestamps
    - System information logging on startup

Usage:
    Import the logger instance and use it for logging:

    from logmanager import logger

    logger.info('Informational message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.debug('Debug message (only visible in DEBUG mode)')

Configuration:
    Logging configuration is read from app_control.settings with the following keys:
    - logging.logfilepath: Directory path for log files
    - logging.logappname: Application name used for logger and log filename
    - logging.level: Logging level ('DEBUG' or 'INFO')

The logger is automatically configured on module import and begins logging
system information including Python version and platform details.

Author: Gary Twinn
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
logger.info('Running Python %s on %s', sys.version, sys.platform)
logger.info('Logging level set to: %s',settings['logging']['level'].upper())
