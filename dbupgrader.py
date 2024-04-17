"""
Database upgrader
Author: Gary Twinn
"""

import zipfile
import os.path
import os
import time
import sqlite3
from app_control import settings


def backup_database():
    """Backup the exisiting database"""
    print('Starting Database Backup')
    backupfile= os.path.dirname(os.path.abspath(settings['database']['databasepath']))  + '\\pre-upgrade-db-backup.zip'
    dbzip = zipfile.ZipFile(backupfile, 'w')
    dbzip.write(os.path.abspath(settings['database']['databasepath']),
                os.path.basename(settings['database']['databasepath']),  compress_type=zipfile.ZIP_DEFLATED)
    dbzip.write(os.path.abspath(settings['database']['resultsdatabasepath']),
                os.path.basename(settings['database']['resultsdatabasepath']),  compress_type=zipfile.ZIP_DEFLATED)
    dbzip.close()
    print("Backup processing time = %s seconds" % time.process_time())
    print('**** Backup Script Finished ****')

def pyms_database_update():
    """Upgrade the exisiting database"""
    print('Stating PyMS Database upgrade')
    database = sqlite3.connect(settings['database']['databasepath'])
    cursor_obj = database.cursor()
    dbversion = check_db_version(database)
    print('Database version = %s' % dbversion)
    if dbversion == 1:
        print('Database convertion to v2 starting')
        sql_script = 'ALTER TABLE cycles add laserpower double'
        database.execute(sql_script)
        sql_script = 'ALTER TABLE cycles add issample boolean'
        database.execute(sql_script)
        sql_query = 'SELECT id, name from cycles'
        cursor_obj.execute(sql_query)
        sql_update_query = """ UPDATE cycles SET name = ?, laserpower = ?, issample = ? WHERE id = ?"""
        for cycleid in cursor_obj.fetchall():
            if cycleid[1][:6] == 'Sample':
                cyclename = 'Apatite' + cycleid[1][6:]
                laserpower = settings['laser']['power']
                issample = True
            else:
                cyclename = cycleid[1]
                laserpower = 0
                issample = False
            print('id = %s, name = %s, laserpower = %s, issample = %s' % (cycleid[0], cyclename, laserpower, issample))
            datarow = (cyclename, laserpower, issample, cycleid[0])
            cursor_obj.execute(sql_update_query, datarow)
        database.commit()
        sql_query = 'SELECT runnumber, cycle from batchsteps WHERE cycle like "Sample%"'
        cursor_obj.execute(sql_query)
        sql_update_query = 'UPDATE batchsteps SET cycle = ? WHERE runnumber = ?'
        for batchid in cursor_obj.fetchall():
            cyclename = 'Apatite' + batchid[1][6:]
            print('runnumber = %s new name = %s' % (batchid[0], cyclename))
            datarow = (cyclename, batchid[0])
            cursor_obj.execute(sql_update_query, datarow)
        database.commit()
        cursor_obj.execute('UPDATE settings SET version = 2 WHERE version = 1')
        database.commit()
    database.close()

def check_db_version(database):
    """Check the exisiting database vesrions"""
    cursor_obj = database.cursor()
    sql_query = 'SELECT * from settings'
    try:
        cursor_obj.execute(sql_query)
    except sqlite3.OperationalError:
        print('settings table missing - version 0 database')
        sql_script = 'CREATE TABLE settings (version INT);'
        database.execute(sql_script)
        sql_script = 'INSERT INTO settings (version) VALUES (1);'
        database.execute(sql_script)
        database.commit()
        cursor_obj.execute(sql_query)
    return cursor_obj.fetchone()[0]


def results_database_update():
    """Upgrade the results database"""
    print('Stating Results Database upgrade')
    database = sqlite3.connect(settings['database']['resultsdatabasepath'])
    cursor_obj = database.cursor()
    dbversion = check_db_version(database)
    print('Database version = %s' % dbversion)
    if dbversion == 1:
        print('Database convertion to v2 starting')
        sql_query = 'SELECT id , type from HeliumRuns WHERE type like "Sample%"'
        cursor_obj.execute(sql_query)
        sql_update_query = 'UPDATE HeliumRuns SET type = ? WHERE id = ?'
        for heliumrun in cursor_obj.fetchall():
            cyclename = 'Apatite' + heliumrun[1][6:]
            print('id = %s new name = %s' % (heliumrun[0], cyclename))
            datarow = (cyclename, heliumrun[0])
            cursor_obj.execute(sql_update_query, datarow)
        database.commit()
        cursor_obj.execute('UPDATE settings SET version = 2 WHERE version = 1')
        database.commit()
    database.close()


if __name__ == '__main__':
    backup_database()
    pyms_database_update()
    results_database_update()
