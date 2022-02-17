from backup import backupfile
import os


current_path = os.getcwd()
backupfile(current_path + "\\settings.json")
backupfile(current_path + "\\alerts.json" )
backupfile(current_path + "\\backup.json" )
