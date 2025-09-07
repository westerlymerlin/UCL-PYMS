# Module Documentation


This document contains the documentation for all the modules in this project.

---

## Contents


[about_form](./about_form.md)  
About Dialog

[alertmessage](./alertmessage.md)  
Alert Message Module

This module provides functionality to send alert notifications via email using
SMTP and Office 365 authentication. It reads configuration from 'alerts.json'
and supports sending customized alert messages to multiple recipients.

Features:
- Secure authentication using base64 encoded Office 365 credentials
- Configurable SMTP settings, subjects, and message templates
- Logging of alert delivery status
- Support for multiple recipients

Usage:
    from alertmessage import alert

    # Send a custom alert message
    alert("Critical error in data processing module")

Configuration:
    Requires 'alerts.json' file with the following structure:
    {
        "SMTPServer": "smtp.office365.com",
        "SMTPPort": 587,
        "O365Sender": "alerts@example.com",
        "O365From": "alerts@example.com",
        "O365Key": "<base64-encoded-username-and-password>",
        "Subject": "System Alert",
        "Message": "The following alert was triggered:",
        "Recipients": ["admin@example.com", "manager@example.com"]
    }

Author: Gary Twinn

[app_control](./app_control.md)  
Application Control module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function. Has global variables and routine for
calculating a file name and removing illegal character.

[batchclass](./batchclass.md)  
BatchClass - used to manage a batch of cycles (samples, blanks, qshots or other tasks)

[cycle_edit_form](./cycle_edit_form.md)  
UI Form for Editing Cycles
Author: Gary Twinn

[cycleclass](./cycleclass.md)  
Cycle Class
Author: Gary Twinn

[datadumpfixer](./datadumpfixer.md)  
Imports data from a datatdump file and genertes a helium file and updates the database

[dbupgrader](./dbupgrader.md)  
Database upgrader
Author: Gary Twinn

[host_commands](./host_commands.md)  
Noble Gas Concentration Calculator (NCC) Module
Author: Gary Twinn

This module provides comprehensive functionality for processing helium isotope measurement data
and calculating noble gas concentrations from mass spectrometry results. It handles the complete
workflow from data file reading through blank correction to final NCC calculation and output.

Key Components:
- HeResults: Main class for processing and analyzing helium isotope measurement data
- singlefilereader: Function for reading and parsing individual measurement data files
- linbestfit: Linear regression analysis function for isotope ratio calculations

The module supports:
- Reading and parsing helium measurement data files from various sources
- Blank correction calculations and statistical analysis
- Linear regression fitting for He3/He4 isotope ratios
- NCC (Noble Gas Concentration) calculations with error propagation
- Automated file output generation for processed results
- Quality control and data validation throughout the analysis pipeline

[host_queries](./host_queries.md)  
Hardware Query Interface Module
Author: Gary Twinn

This module provides query functions for retrieving status and data from various hardware
components in the mass spectrometry system. It handles communication with multiple host
controllers to obtain real-time information about system state and measurements.

Key Functions:
- lasergetalarm: Retrieves alarm status from the laser system
- lasergetstatus: Gets current status information from the laser controller
- valvegetstatus: Queries valve states and configuration from the valve controller
- pressuresread: Reads pressure measurements from various system components
- xyread: Obtains current X-Y stage position and movement status

The module handles network communication with hardware hosts, manages timeouts and
exceptions, and provides consistent data structures for system status information.
All functions return structured data that can be used by the main application for
monitoring and control purposes.

This module works in conjunction with host_commands.py to provide complete hardware
interface functionality for the mass spectrometry automation system.

[imagefiler](./imagefiler.md)  
Application Window Screenshot Capture Module

This module provides functionality for capturing screenshots of specific application windows
and saving them as PNG image files. It is designed for mass spectrometry automation systems
to document the visual state of various instrument control applications during batch processing.

Key Features:
- Captures screenshots of named application windows using Windows API
- Saves images with descriptive filenames based on batch information
- Automatically creates directory structures for organized file storage
- Handles window enumeration for debugging and application discovery
- Provides robust error handling and logging for capture failures

Main Functions:
- imager(): Captures and saves a screenshot of a specified application window
- enumHandler(): Enumerates visible windows for debugging purposes

Dependencies:
- Windows-specific APIs (win32gui, win32ui, ctypes)
- PIL (Python Imaging Library) for image processing
- Custom modules: app_control, logmanager

Author: Gary Twinn

[laser_manual_form](./laser_manual_form.md)  
Laser Manual Form, used to manually control the Helium line laser ina  controlled manner
Author: Gary Twinn

[log_viewer_form](./log_viewer_form.md)  
UI form for viewing the logs

[logmanager](./logmanager.md)  
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

[main_form](./main_form.md)  
Main Helium line form - graphical output of the Heliumline state and timers for running samples
Author: Gary Twinn

[manual_xy_form](./manual_xy_form.md)  
Manual XY-Form
Author: Gary Twinn

[ms_hiden_class](./ms_hiden_class.md)  
Mass spectrometry control and data management class for a Hiden Residual Gas Analyser.

This class manages the complete workflow for mass spectrometry operations including:
- Batch processing and step execution
- Network communication with measurement equipment
- Data acquisition and file output
- Timer and timeout management
- System status monitoring and control

The class handles both MID (Multiple Ion Detection) and profile scanning modes,
manages socket connections to external equipment, and coordinates the execution
of measurement batches with proper error handling and retry mechanisms.

Key Features:
- Automated batch execution with configurable timeouts
- Real-time data acquisition and processing
- File-based result storage with customizable output formats
- Network communication for equipment control
- Comprehensive error handling and recovery

Attributes:
    host (str): Network host address for equipment communication
    port (int): Network port for equipment communication
    timeoutseconds (int): Timeout duration for operations
    timeoutretries (int): Number of retry attempts on timeout
    running (bool): Current execution state
    processing (bool): Data processing state
    batchid (int): Current batch identifier

Author: Gary Twinn

[ncc_calc](./ncc_calc.md)  
Noble Gas Concentration Calculator (NCC) Module
Author: Gary Twinn

This module provides functionality for processing helium isotope measurement data and calculating
noble gas concentrations. It handles data file reading, blank correction, linear regression
analysis, and NCC (Nano Cubic Centimetre) calculation for mass spectrometry results.
e
Key Components:
- HeResults: Main class for processing helium isotope measurement data
- singlefilereader: Function for reading individual measurement files
- linbestfit: Linear regression analysis function

The module supports:
- Reading and parsing helium measurement data files
- Blank correction calculations
- Linear regression fitting for isotope ratios
- NCC (Noble Gas Concentration) calculations
- File output generation for processed results

[ncc_calc_form](./ncc_calc_form.md)  
NCC Calculation Form
Author: Gary Twinn

[new_batch_form](./new_batch_form.md)  
New Batch dialog
Author: Gary Twinn

[planchet_form](./planchet_form.md)  
Planchet entry form
Author: Gary Twinn

[settings_viewer_form](./settings_viewer_form.md)  
Settings Viewer form
Author: Gary Twinn

[simple_batch_form](./simple_batch_form.md)  
Dialog for a simple batch (used for tesing the Helium line) has a maximum of 5 stepa
Author: Gary Twinn


---


  
-------
#### Copyright (C) 2025 Gary Twinn  

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.  
  
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.  
  
  ##### Author: Gary Twinn  
  
 -------------
  
