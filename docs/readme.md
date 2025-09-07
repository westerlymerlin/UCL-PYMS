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
has appeared it will creat from the defaults in the initialise function. Has global vraiables and routine for
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
Commands to the controller APIs

[host_queries](./host_queries.md)  
Queries to the controller APIs

[imagefiler](./imagefiler.md)  
Image Filer
Author: Gary Twinn

[laser_manual_form](./laser_manual_form.md)  
Laser Manual Form, used to manually control the Helium line laser ina  controlled manner
Author: Gary Twinn

[log_viewer_form](./log_viewer_form.md)  
UI form for viewing the logs

[logmanager](./logmanager.md)  
logmanager, setus up application logging. use the **logger** property to
write to the log.

[main_form](./main_form.md)  
Main Helium line form - graphical outut of the Heliumline state and timers for running samples
Author: Gary Twinn

[manual_xy_form](./manual_xy_form.md)  
Manual XY-Form
Author: Gary Twinn

[ms_hiden_class](./ms_hiden_class.md)  
Class to read data from a Hiden Mass Spectrometer and calculate the best-fit value for t=0

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
  
