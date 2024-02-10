"""Backup all settings files to sharepoint """
import os
from backup import backupfile
from settings import settings


current_path = os.getcwd()
backupfile(current_path + "\\settings.json")
backupfile(current_path + "\\alerts.json")
backupfile(current_path + "\\backup.json")
backupfile(settings['MassSpec']['datadirectory'] + "metrics.csv")
backupfile(settings['database']['databasepath'])
backupfile(settings['database']['resultsdatabasepath'])
backupfile(settings['logging']['logfilepath'] + settings['logging']['logappname'] + '.log')
backupfile(settings['logging']['logfilepath'] + settings['logging']['logappname'] + '.log.1')
backupfile(settings['logging']['logfilepath'] + settings['logging']['logappname'] + '.log.2')
backupfile(settings['logging']['logfilepath'] + settings['logging']['logappname'] + '.log.3')
backupfile(settings['logging']['logfilepath'] + settings['logging']['logappname'] + '.log.4')
backupfile(settings['logging']['logfilepath'] + settings['logging']['logappname'] + '.log.6')
backupfile(settings['logging']['logfilepath'] + settings['logging']['logappname'] + '.log.7')
backupfile(settings['logging']['logfilepath'] + settings['logging']['logappname'] + '.log.8')
backupfile(settings['logging']['logfilepath'] + settings['logging']['logappname'] + '.log.9')
