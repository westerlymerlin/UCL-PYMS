# PyMS - Python Mass Spectrometry 

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-Qt6-green.svg)](https://wiki.qt.io/Qt_for_Python)

PyMS is a desktop application that provides a Graphical User Interface (GUI) for managing cycles of batches on the
London Geochronology Centres's Helium extraction line. Built with Python and the Qt6 UI framework via PySide6,
PyMS offers robust tools for batch processing control and visualisation.

## 🚀 Features

- Intuitive graphical interface for batch cycle management
- Real-time monitoring of cycle processes
- NCC value viewing and generation
- Cycle step editing capabilities

## 📋 Application Components

| Component | Description |
|-----------|-------------|
| `PyMS.pyw` | Main application entry point |
| `NccViewer.pyw` | Tool for viewing NCC values for run samples and generating new NCC files based on line blanks |
| `CycleEditor.pyw` | Interface for editing cycle steps - add, modify, or delete tasks at specific run times |
| `imagefiler.py` | Utility that lists all open windows (helpful for identifying window names when using applications with camera images) |
| `settings.json` | Configuration file containing settings for laser, host addresses, and data file locations |

## 📖 Documentation

- **Application Documentation**: See [readme.pdf](./readme.pdf)
- **Python Module Documentation**: Available in the [docs](./docs/readme.md) folder
- **Change Log**: View recent changes in [changelog.txt](./changelog.txt)

## 🔧 Installation

A windows installer is found in the [distribution](./distribution) folder.  
Download the file and run it (requires Windows 10 or higher)

## 🔧 Building a new version

To create a new version of PyMS, first clone the repo from Github using the command below:  
`git clone https://github.com/westerlymerlin/UCL-PYMS.git`  
you will need to have Python 3.12 installed with all the dependencies listed in [requirements.txt](./requirements.txt).  
`pip install -r requirements.txt`  

In order to package the code into a windows application, you will need the latest version of **pyinstaller** and **pyinstaller_versionfile** and installed.  
`pip install pyinstaller pyinstaller_versionfile` 
You will need InstallForge installed to create the windows installer file - download and install from [**InstallForge.net**](https://installforge.net/download/ )

Please create a new branch in git for your edits. 
`git branch -b my-new-feature`    
Make your changes to the code in your favorite IDE and test them, once you are happy with the results you are ready to package the new version:  
1. Update the version number in the module app_control.py  
2. Add a new line to the `changelog.txt`  
3. Run the following command to package the application:  
`python -m ./packager/make.py`  
   The makefile will create the new packaged files and start sourceforge, you will need to click the build button to create the new installed into the ./distribution folder.

Please commit the changes you have made to git and push to the repository to git for version control.  
`git add .`  
`git commit -m "My commit message"`  
`git push origin my-new-feature`

There is a workflow that will update the docs files and create a pull request for the code owner to review and merge to the main branch.

--------------

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


Author:  Gary Twinn  
Repository:  [github.com/westerlymerlin](https://github)

-------------

