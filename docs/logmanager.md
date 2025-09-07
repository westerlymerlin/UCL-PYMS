# None

<a id="logmanager"></a>

# logmanager

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

<a id="logmanager.sys"></a>

## sys

<a id="logmanager.os"></a>

## os

<a id="logmanager.logging"></a>

## logging

<a id="logmanager.RotatingFileHandler"></a>

## RotatingFileHandler

<a id="logmanager.settings"></a>

## settings

<a id="logmanager.log_dir"></a>

#### log\_dir

<a id="logmanager.logger"></a>

#### logger

Usage:
**logger.info('message')** for info messages
**logger.warning('message')** for warnings
**logger.error('message')** for errors
**logger.debug('message')** for debugging info

<a id="logmanager.LogFile"></a>

#### LogFile

<a id="logmanager.formatter"></a>

#### formatter

