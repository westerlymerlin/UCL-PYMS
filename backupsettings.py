from backup import backupfile
import os
from settings import settings


current_path = os.getcwd()
backupfile(current_path + "\\settings.json")
backupfile(current_path + "\\alerts.json" )
backupfile(current_path + "\\backup.json" )
backupfile(settings['MassSpec']['datadirectory'] + "metrics.csv")
backupfile(settings['database']['databasepath'])
backupfile(settings['database']['resultsdatabasepath'])