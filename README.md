# PyMS

PyMS is a desktop application designed to provide a Graphical User Interface (GUI) control to manage cycles of batches.
PyMS is designed using Python and QT6 UI framework via PySide6.

 Script File         | Description                                                                                                  
---------------------|--------------------------------------------------------------------------------------------------------------
 `PyMS.pyw`          | This is the main application.                                                                                
 `NccViewer.pyw`     | This script is used to view NCC values for run samples, and generate new NCC files depending on line blanks. 
 `CycleEditor.pyw`   | This script allows you to edit the cycle steps, add, change, and delete tasks at set run times.              
 `imagefiler.py`     | Lists all of the open windows  (useful for window names when using apps that hold camera images).            
 `backupsettings.py` | This script copies 3 settings JSON files and databases to SharePoint.                                        
 `settings.json`     | Main settings file holding settings for laser, host locations, and data file locations.                      