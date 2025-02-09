"""Imports data from a datatdump file and genertes a helium file and updates the database"""

from datetime import datetime
import os
from ast import literal_eval
import sqlite3
from app_control import settings
from ncc_calc import linbestfit

def getdata(filename):
    """Get data from a datadump file and return a list of lists"""
    try:
        with open(filename, 'r', encoding='utf-8') as datafile:
            dumpdata = datafile.read()
            dumpdata = literal_eval(dumpdata)
            print('dumpdata has %s rows' % len(dumpdata))
            return dumpdata
    except FileNotFoundError:
        print('File not found - %s' % filename)
        return []


def writefile(dump_file_name, date_run, helium_file_path, helium_run):
    """Write Helium Data file to disk"""
    try:
        database = sqlite3.connect(settings['database']['resultsdatabasepath'])
        cursor_obj = database.cursor()
        sql_query = 'Select id, identifier from HeliumRuns where id = ?'
        cursor_obj.execute(sql_query,[str(helium_run)])
        datarow= cursor_obj.fetchone()
        identifier=datarow[1]
        print('database ideintifier = %s' % identifier)
        database.close()
    except sqlite3.OperationalError:
        print('Database get detsils error')
        return

    data = getdata(dump_file_name)
    print('Datafile has %s rows' % len(data))
    multiplier = 1 / settings['MassSpec']['multiplier']
    print('multiplier = %s' % multiplier)
    timestamp = []
    m1 = []
    m3 = []
    m4 = []
    m5 = []
    m6 = []
    m40 = []
    try:
        for row in data:
            print(row)
            sampledate = (datetime.strptime(row[0], '%d/%m/%Y %H:%M:%S') - date_run).total_seconds()
            if sampledate > 0:
                timestamp.append(round(sampledate, 6))
                m1.append(round(float(row[2]) * multiplier, 6))
                m3.append(round(float(row[3]) * multiplier, 6))
                m4.append(round(float(row[4]) * multiplier, 6))
                m5.append(0)
                m40.append(round(float(row[5]) * multiplier, 6))
                m6.append(0)

        if len(timestamp) == 0:
            print('O rows added to file, Data dumped to a file')
        print('msHiden: Calculating bestfit')
        bestfit = linbestfit(timestamp, m1, m3, m4)

        print('bestfit = %s' % bestfit[1])
    except:
        print()
        print('msHiden: writefile error parsing the data')
        return
    try:

        if identifier == 'Line Blank':
            line = 'LB@'
        else:
            line = identifier + '@'
        outfile = open(helium_file_path, 'w', encoding='utf-8')
        print('openng filepath = %s' % helium_file_path)
        for i in range(0, len(timestamp)):
            line = line + '%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
                timestamp[i], m1[i], m3[i], m4[i], m5[i], m40[i], m6[i])
            print(line, file=outfile)
            line = ''
        outfile.close()
    except:
        print("failed to write to helium results file %s " % Exception)
        return



dumpfilename = input('Enter full filename of datadump file: ')
dateruntxt = input('Enter datadump "Timer Start" date (yyyy-mm-dd hh:mm:ss): ')
daterun = datetime.strptime(dateruntxt, '%Y-%m-%d %H:%M:%S')
heliumfilepath = dumpfilename[:-12]
heliumrun = os.path.basename(heliumfilepath)
print('Data dump filename: %s' % dumpfilename)
print('Helium file = %s' % heliumfilepath)
print('Helium run: %s' % heliumrun)
print('Timer Start - %s' % daterun)
writefile(dumpfilename, daterun, heliumfilepath, heliumrun)
