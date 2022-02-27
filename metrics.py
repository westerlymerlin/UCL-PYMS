from settings import settings
from datetime import datetime
from os import path
import csv

count = 0

def datafilecheck(filename):
    if(path.exists(filename) == False) or path.getsize(filename) > 200000000:
        print('Createing new metrics file')
        datarow = 'Date, Tank (mBar), Turbo (Mbar), Ion (mBar), Temperature (C), M (3He), M1 (H), M4 (4He), M5, M40 (40Ar)'
        outfile = open(filename, "w")
        print(datarow, file=outfile)
        outfile.close()


def write_metrics(Tank, Turbo, Ion, Temperature, M, M1, M4, M5, M40):
    global count
    filename = '%sMetrics.csv' % settings['MassSpec']['datadirectory']
    if count == 0:
        datafilecheck(filename)
        datarow = '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s' %(datetime.now(), Tank, Turbo, Ion, Temperature, M, M1, M4, M5, M40)
        outfile = open(filename, "a")
        print(datarow, file=outfile)
        outfile.close()

    count += 1
    if count == 30:
        count = 0

