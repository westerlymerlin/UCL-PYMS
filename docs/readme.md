# Module Documentation


This document contains the documentation for all the modules in this project.

---

## Contents


[about_form](./about_form.md)  
About Dialog UI

[alertmessage](./alertmessage.md)  
Provides functionality to send emails using the Microsoft Graph API.

This module defines a function that sends an email through the Microsoft Graph API by authenticating
via Microsoft Authentication Library (MSAL). It uses OAuth2-based client authentication and constructs
an email payload dynamically based on input data. The email can include sender, recipient, subject, and
message body details. Logs and errors are appropriately recorded.

[app_control](./app_control.md)  
Application Control module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function. Has global variables and routine for
calculating a file name and removing illegal character.

[batchclass](./batchclass.md)  
The `BatchClass` represents a batch of samples or planchets. It allows for the creation, modification, and
completion of batch steps. The class interacts with a SQLite database to store and retrieve batch information.

Attributes:
    id (int): ID number of the batch. -1 indicates that the batch has not been saved yet, otherwise it is taken
    from the database.
    date (datetime): The date and time when the batch was created.
    description (str): The description or name of the batch.
    type (str): The type of batch. Can be either 'Simple Batch' or 'Planchet'.
    runnumber (list[int]): A list of ID numbers of each item in the batch, including the samples.
    cycle (list[str]): A list of the type of cycle required for each item.
    location (list[str]): A list of the hole location if needed for each item.
    identifier (list[str]): A list of the description of the sample or qnumber for each item.
    status (list[int]): A list of the status of each item. 0 indicates 'to do', 1 indicates 'complete', and 2
    indicates 'cancelled'.
    changed (int): A flag indicating whether the batch has been modified since the last save.

Methods:
    read_database()
        Reads the PyMS database for any open batches.

    cancel_batch()
        Used to cancel_batch a batch. Marks all samples as cancelled and closes the batch.

    new(batchtype: str, description: str)
        Creates a new batch with the specified batch type and description.

    addstep(cycle: str, location: str, identifier: str)
        Adds a sample to the batch.

    save()
        Saves the batch details to the database.

    current()
        Returns the details of the current batch step or 'End' if there are no more steps.

    completecurrent()
        Marks the current batch step as complete.

    writebatchlog()
        Generates the batchlog.csv file for the batch.

[cycle_edit_form](./cycle_edit_form.md)  
UI Form for Editing Cycles
Author: Gary Twinn

[cycleclass](./cycleclass.md)  
Cycle Class
Author: Gary Twinn

[datadumpfixer](./datadumpfixer.md)  
Imports data from a datatdump file and genertes a helium file and updates the database

[dbupgrader](./dbupgrader.md)  
Database backup and upgrade tools.

This module provides functions for performing database backups and upgrading
databases to newer versions. It includes functionalities to back up specified
databases into a compressed zip file, as well as to modify database schemas
and update data based on new version changes or requirements.

Functions:
- backup_database(): Creates a zip file backup of the main and results database.
- pyms_database_update(): Upgrades the primary database to the latest version.
- results_database_update(): Upgrades the results database to the latest version.
- check_db_version(): Determines the current version of a database or initializes
  it if it is missing required structures.

Author: Gary Twinn

[host_commands](./host_commands.md)  
Host Commands Module - Hardware Control Interface

This module provides command functions for controlling various hardware components
in the PyMS (Python Mass Spectrometry) system. It includes functions for:

- Laser control and power management
- Valve operations and state changes
- XY positioning system movement and positioning
- Communication with hardware controllers

These functions serve as the interface layer between the PyMS application
and the underlying hardware systems, handling the low-level command protocols
and hardware-specific communication.

Author: Gary Twinn

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

[manual_batch_form](./manual_batch_form.md)  
Dialog for a Manual batch (used for testing the Helium line) has a default of 8 steps but more can be added
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
NCC (Nano Cubic Centimetre) Calculation Form
Provides a GUI interface for loading, processing, and visualizing NCC data files.
Includes functionality for statistical analysis, chart generation, and data export.
Author: Gary Twinn

[new_batch_form](./new_batch_form.md)  
New Batch dialog
Author: Gary Twinn

[planchet_form](./planchet_form.md)  
Planchet entry form
Author: Gary Twinn

[settings_viewer_form](./settings_viewer_form.md)  
Settings viewer / editor form. allows user to edit setting values manually. settings are then saves in the
settings.json file
Author: Gary Twinn


---


  
-------
#### Copyright (C) 2026 Gary Twinn  

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
  
