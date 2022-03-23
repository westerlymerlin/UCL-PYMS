import struct
import os
import time
import sqlite3
import numpy
from scipy import stats
from datetime import datetime
from settings import settings, writesettings, friendlydirname
from backup import backupfile
from metrics import write_metrics


def linbestfit(sampletime, m, m1, m4, hd_h):
    nt = len(sampletime)
    hd = numpy.zeros(nt, dtype='double')
    he3 = numpy.zeros(nt, dtype='double')
    he4_he3 = numpy.zeros(nt, dtype='double')
    for i in range(len(hd)):
        hd[i] = m1[i] * hd_h
        he3[i] = m[i] - hd[i]
        he4_he3[i] = (m4[i] / he3[i]) * 1000
    return stats.linregress(sampletime, he4_he3)


class MSClass:
    def __init__(self):
        self.databasepath = settings['database']['databasepath']
        self.resultstabasepath = settings['database']['resultsdatabasepath']
        self.readfile = settings['MassSpec']['readfile']
        self.multiplier = 1 / settings['MassSpec']['multiplier']
        self.resetclass()
        self.time = []
        self.m1 = []
        self.m = []
        self.m4 = []
        self.m5 = []
        self.m40 = []
        self.m6 = []
        self.bestfit = []
        self.quaddata = []
        self.id = settings['MassSpec']['nextH']
        self.type = ''
        self.filename = ''
        self.identifier = ''
        self.daterun = time.time()
        self.batchdescription = ''
        self.batchid = 0
        self.batchitemid = 0
        self.alarm = 0
        self.laserpower = settings['laser']['power']
        self.dde = None
        self.filereader()

    def resetclass(self):
        self.time = []
        self.m1 = []
        self.m = []
        self.m4 = []
        self.m5 = []
        self.m40 = []
        self.m6 = []
        self.bestfit = 0
        self.id = settings['MassSpec']['nextH']
        self.type = ''
        self.filename = ''
        self.identifier = ''
        self.daterun = time.time()
        self.batchdescription = ''
        self.batchid = 0
        self.batchitemid = 0
        self.laserpower = settings['laser']['power']

    def starttimer(self, batchtype, identifier, batchdescription, batchid, batchitemid):
        self.daterun = time.time()
        self.id = settings['MassSpec']['nextH']
        self.type = batchtype
        self.identifier = identifier
        self.laserpower = settings['laser']['power']
        self.batchdescription = batchdescription
        self.batchid = batchid
        self.batchitemid = batchitemid

    def check_quad_is_online(self):
        return self.quaddata[0]

    def filereader(self):
        filepath = self.readfile
        counter = 0
        while counter < 2:
            bytelist = []
            try:
                with open(self.readfile, "rb") as datafile:
                    bytelist = datafile.read()
                datafile.close()
            except PermissionError:
                print('msFileclass: QuadStar Permission Error')
                self.quaddata = ['Off Line', datetime.now(), '', '', '', '', '', 0, 0, 0, 0, 0, 'No File']
            except FileNotFoundError:
                print('msFileclass: QuadStar File not Found')
                self.quaddata = ['Off Line', datetime.now(), '', '', '', '', '', 0, 0, 0, 0, 0, 'No File']
            except:
                print('msFileclass: QuadStar File other read error')
                self.quaddata = ['Off Line', datetime.now(), '', '', '', '', '', 0, 0, 0, 0, 0, 'No File']
            if len(bytelist) > 500:
                # print("msFileclass counter %s" % counter)
                counter = 10
            else:
                time.sleep(0.1)
                counter += 1
                print("msFileclass: QuadStar File too short error")
        if len(bytelist) > 500:
            filetype = str(bytelist[205:216], 'cp1252')
            c0 = str(bytelist[317:326], 'cp1252')
            c1 = str(bytelist[350:359], 'cp1252')
            c2 = str(bytelist[383:392], 'cp1252')
            c3 = str(bytelist[416:425], 'cp1252')
            c4 = str(bytelist[449:458], 'cp1252')
            sampletime = datetime(1900 + bytelist[13], bytelist[12], bytelist[11],
                                  bytelist[10], bytelist[9], bytelist[8])
            pos = 488
            e0 = struct.unpack('f', bytearray(bytelist[pos + 0:pos + 4]))[0]
            e1 = struct.unpack('f', bytearray(bytelist[pos + 4:pos + 8]))[0]
            e2 = struct.unpack('f', bytearray(bytelist[pos + 8:pos + 12]))[0]
            e3 = struct.unpack('f', bytearray(bytelist[pos + 12:pos + 16]))[0]
            e4 = struct.unpack('f', bytearray(bytelist[pos + 16:pos + 20]))[0]
            self.quaddata = [os.path.basename(filepath), sampletime, c0, c1, c2, c3, c4, e0, e1, e2, e3, e4, filetype]
            self.alarm = 0
            if (time.time() - datetime.timestamp(sampletime)) > 30:
                self.quaddata[0] = 'Off Line'
                self.alarm = 1
                print('msFileclass: Quad read: Late file time=%s' % sampletime)
            else:
                if settings['metrics'] == 1:
                    write_metrics(settings['vacuum']['tank']['current'],settings['vacuum']['turbo']['current'],settings['vacuum']['ion']['current'],settings['pyrometer']['current'],e1,e1,e2,e3,e4)
        else:
            print("msFileclass: Quad Read fail after 2 attempts")
            self.alarm = 1
            self.quaddata = ['Off Line', datetime.now(), '', '', '', '', '', 0, 0, 0, 0, 0, 'No File']


    def read(self):
        e0 = self.quaddata[7] * self.multiplier
        e1 = self.quaddata[8] * self.multiplier
        e2 = self.quaddata[9] * self.multiplier
        e3 = self.quaddata[10] * self.multiplier
        e4 = self.quaddata[11] * self.multiplier
        sampletime = self.quaddata[1]
        print('msFileclass: Quad data %s, %s, %s, %s, %s, %s ' % (sampletime, e0, e1, e2, e3, e4))

        self.time.append(round(sampletime.timestamp() - self.daterun, 6))
        self.m1.append(round(e0, 6))
        self.m.append(round(e1, 6))
        self.m4.append(round(e2, 6))
        self.m5.append(round(e3, 6))
        self.m40.append(round(e4, 6))
        self.m6.append(round(0, 6))

    def writefile(self):
        print('msFileclass: Calculating bestfit')
        self.bestfit = linbestfit(self.time, self.m, self.m1, self.m4, settings['MassSpec']['HD/H'])
        try:
            self.filename = 'HE' + str(self.id) + 'R'
            print('msFileclass: filename = %s' % self.filename)
            filepath = settings['MassSpec']['datadirectory'] + friendlydirname(str(self.batchid) + ' ' + self.batchdescription)

            os.makedirs(filepath, exist_ok=True)
            filename = filepath + '\\' + self.filename
            line = self.identifier + '@'
            outfile = open(filename, 'w')
            # print('openng filepath = %s' % filename)
            for i in range(0, len(self.time)):
                line = line + '%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
                    self.time[i], self.m1[i], self.m[i], self.m4[i], self.m5[i], self.m40[i], self.m6[i])
                print(line, file=outfile)
                line = ''
            outfile.close()
            backupfile(filename)
            # print('closed filepath = %s' % filename)
            writesettings()
            with open(filename, 'rb') as infile:
                blobfile = infile.read()
            infile.close()
        except:
            print("msFileclass: failed to write to helium results file %s " % Exception)
        try:
            database = sqlite3.connect(self.resultstabasepath)
            cursor_obj = database.cursor()
            sql_insert_query = """INSERT INTO HeliumRuns (id, type, identifier, daterun, batchdescription, batchid, 
             batchitemid, laserpower, filedata, Bestfit) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """
            datarow = (self.filename, self.type, self.identifier, datetime.now(), self.batchdescription, self.batchid,
                       self.batchitemid, self.laserpower, blobfile, self.bestfit[1])

            cursor_obj.execute(sql_insert_query, datarow)
            database.commit()
            sql_insert_query = """INSERT INTO MSRawData (id, time, m1, m, m4, m5, m40, m6) VALUES (?, ?, ?, ?, ?, ?, 
            ?, ?) """
            for i in range(0, len(self.time)):
                datarow = (
                    self.filename, self.time[i], self.m1[i], self.m[i], self.m4[i], self.m5[i], self.m40[i], self.m6[i])
                cursor_obj.execute(sql_insert_query, datarow)
            database.commit()
            settings['MassSpec']['nextH'] += 1
            writesettings()
            self.resetclass()
        except sqlite3.Error as error:
            print("msFileclass: failed to write to helium results database ", error)


ms = MSClass()
