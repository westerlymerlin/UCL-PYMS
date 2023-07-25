from settings import settings, writesettings, friendlydirname
import socket
import os
import time
import sqlite3
import numpy
import threading
from scipy import stats
from datetime import datetime
from backup import backupfile


class MSClass:
    def __init__(self):
        self.databasepath = settings['database']['databasepath']
        self.resultstabasepath = settings['database']['resultsdatabasepath']
        self.midfile = settings['MassSpec']['hidenMID']
        self.profilefile = settings['MassSpec']['hidenProfile']
        self.runfile = settings['MassSpec']['hidenRunfile']
        self.host = settings['MassSpec']['hidenhost']
        self.port = settings['MassSpec']['hidenport']
        self.multiplier = 1 / settings['MassSpec']['multiplier']
        self.timeoutretries = settings['MassSpec']['timeoutretries']
        self.startimeoffset = settings['MassSpec']['startimeoffset']
        self.resetclass()
        self.time = []
        self.m1 = []
        self.m3 = []
        self.m4 = []
        self.m5 = []
        self.m40 = []
        self.m6 = []
        self.bestfit = []
        self.id = self.next_id()
        self.type = ''
        self.filename = ''
        self.identifier = ''
        self.daterun = datetime.now()
        self.batchdescription = ''
        self.batchid = 0
        self.batchitemid = 0
        self.socketreturn = 0
        self.running = False
        self.timeoutcounter = 0

    def command_parser(self, command):
        if command == 'hiden-startmid':
            timerthread = threading.Timer(0.1, self.start_mid)
            timerthread.start()
            return 1
        if command == 'hiden-startprofile':
            timerthread = threading.Timer(0.1, self.start_profile)
            timerthread.start()
            return 1
        if command == 'hiden-stop':
            timerthread = threading.Timer(0.1, self.stop_runnning)
            timerthread.start()
            return 1
        if command == 'writefile':
            self.writefile()
            return 1
        return 0

    def resetclass(self):
        self.time = []
        self.m1 = []
        self.m3 = []
        self.m4 = []
        self.m5 = []
        self.m40 = []
        self.m6 = []
        self.bestfit = 0
        self.id = self.next_id()
        self.type = ''
        self.filename = ''
        self.identifier = ''
        self.batchdescription = ''
        self.batchid = 0
        self.batchitemid = 0

    def starttimer(self, batchtype, identifier, batchdescription, batchid, batchitemid):
        # print('msHiden: start timer', batchtype, identifier, batchdescription, batchid, batchitemid)
        self.daterun = datetime.now()
        self.id = self.next_id()
        self.type = batchtype
        self.identifier = identifier
        self.batchdescription = batchdescription
        self.batchid = batchid
        self.batchitemid = batchitemid

    def check_quad_is_online(self):
        try:
            s = socket.create_connection((self.host, self.port), .5)
            s.recv(1024).decode()
            s.send(bytes('-xStatus \r\n', 'utf-8'))
            status = s.recv(1024).decode()
            # print('MsHiden status recieved = %s' % status)
            self.timeoutcounter = 0
            if status[:-2] == 'Unavailable':
                print('msHiden - return of Unavailable')
                return 'Unavailable'
            return status[:-2]
        except socket.timeout:
            self.timeoutcounter += 1
            print('msHiden - Timeout to MS software - try %s' % self.timeoutcounter)
            return 'Off Line'

    def start_mid(self):
        runningfile = 'none  '
        s = socket.create_connection((self.host, self.port), .5)
        self.socketreturn = s.recv(1024).decode()
        s.send(bytes('-xStatus \r\n', 'utf-8'))
        status = s.recv(1024).decode()
        # print('Status = %s' % status)
        if status[:-2] in ('StoppedShutDown', 'Protected'):
            s.send(bytes('-f"%s" \r\n' % self.midfile, 'utf-8'))
            try:
                self.socketreturn = s.recv(1024).decode()
            except socket.timeout:
                time.sleep(4)
                self.socketreturn = s.recv(1024).decode()
            s.send(bytes('-xFilename \r\n', 'utf-8'))
            runningfile = s.recv(1024).decode()
            print('Loaded file - %s' % runningfile)
            time.sleep(1)
            s.send(bytes('-xGo %s \r\n' % self.runfile, 'utf-8'))
            time.sleep(.5)
            # self.socketreturn = s.recv(1024).decode()
            time.sleep(2)
            s.send(bytes('-xStatus \r\n', 'utf-8'))
            status = s.recv(1024).decode()
            #  print('Run file status = %s' % status)
            self.running = True
        s.close()
        return [runningfile[:-2], status[:-2]]

    def start_profile(self):
        runningfile = 'none  '
        s = socket.create_connection((self.host, self.port), .5)
        self.socketreturn = s.recv(1024).decode()
        s.send(bytes('-xStatus \r\n', 'utf-8'))
        status = s.recv(1024).decode()
        # print('Status = %s' % status)
        if status[:-2] in ('StoppedShutDown', 'Protected'):
            s.send(bytes('-f"%s" \r\n' % self.profilefile, 'utf-8'))
            try:
                self.socketreturn = s.recv(1024).decode()
            except socket.timeout:
                time.sleep(4)
                self.socketreturn = s.recv(1024).decode()
            s.send(bytes('-xFilename \r\n', 'utf-8'))
            runningfile = s.recv(1024).decode()
            print('Loaded file - %s' % runningfile)
            time.sleep(1)
            s.send(bytes('-xGo %s \r\n' % self.runfile, 'utf-8'))
            # self.socketreturn = s.recv(1024).decode()
            time.sleep(2)
            s.send(bytes('-xStatus \r\n', 'utf-8'))
            status = s.recv(1024).decode()
            #  print('Run file status = %s' % status)
            self.running = True
        s.close()
        return [runningfile[:-2], status[:-2]]

    def getdata(self):
        s = socket.create_connection((self.host, self.port), .5)
        self.socketreturn = s.recv(1024).decode()
        s.send(bytes('-lData -v1 -c50 -t1 -m1 \r\n', 'utf-8'))
        sdata = s.recv(16385).decode()
        s.close()
        outputdata = []
        for item in sdata.split('\r\n'):
            outputdata.append(item.split('\t'))
        # outputdata = outputdata[len(outputdata) - 21:]
        return outputdata[:-1]

    def getcolumns(self):
        s = socket.create_connection((self.host, self.port), .5)
        self.socketreturn = s.recv(1024).decode()
        s.send(bytes('-lLegends -v1 \r\n', 'utf-8'))
        legends = s.recv(1024).decode()
        s.close()
        return legends.split('\t')

    def getcycle(self):
        s = socket.create_connection((self.host, self.port), .5)
        self.socketreturn = s.recv(1024).decode()
        s.send(bytes('-lCycle -v1 \r\n', 'utf-8'))
        scycle = s.recv(1024).decode()
        s.close()
        return scycle

    def getenv(self):
        s = socket.create_connection((self.host, self.port), .5)
        self.socketreturn = s.recv(1024).decode()
        s.send(bytes('-lEnvironment -v1 \r\n', 'utf-8'))
        senv = s.recv(1024).decode()
        s.close()
        print('Hidenclass: %s' % senv)

    def getloadedfile(self):
        s = socket.create_connection((self.host, self.port), .5)
        self.socketreturn = s.recv(1024).decode()
        s.send(bytes('-xFilename \r\n', 'utf-8'))
        senv = s.recv(1024).decode()
        s.close()
        print('Hidenclass filename: %s' % senv)

    def stop_runnning(self):
        s = socket.create_connection((self.host, self.port), .5)
        self.socketreturn = s.recv(1024).decode()
        s.send(bytes('-xStatus \r\n', 'utf-8'))
        status = s.recv(1024).decode()
        #print('Status = %s' % status)
        if self.running:
            self.running = False
            print('msHiden - Stopping Hiden')
            s.send(bytes('-f"%s" \r\n' % self.runfile, 'utf-8'))
            self.socketreturn = s.recv(1024).decode()
            time.sleep(2)
            s.send(bytes('-xAbort \r\n', 'utf-8'))
            time.sleep(2)
            self.socketreturn = s.recv(1024).decode()
            s.send(bytes('-xClose \r\n', 'utf-8'))
            time.sleep(2)
            self.socketreturn = s.recv(1024).decode()
        s.close()

    def next_id(self):
        try:
            database = sqlite3.connect(self.resultstabasepath)
            cursor_obj = database.cursor()
            sql_query = "SELECT id FROM HeliumRuns ORDER BY id DESC LIMIT 1"
            cursor_obj.execute(sql_query)
            lastfile = cursor_obj.fetchall()
            nextfile = 'HE' + str(int(lastfile[0][0][2:-1]) + 1) + 'R'
            return nextfile
        except sqlite3.Error as error:
            print("msHiden: next_id error %s" % error)
            return"HE00000R"

    def writefile(self):
        data = self.getdata()
        for row in data:
            sampledate = (datetime.strptime(row[0], '%d/%m/%Y %H:%M:%S') - self.daterun).total_seconds()
            # print(datetime.strptime(row[0], '%d/%m/%Y %H:%M:%S'), self.daterun, sampledate)
            if sampledate > self.startimeoffset:
                if len(self.time) < 20:
                    self.time.append(round(sampledate, 6))
                    self.m1.append(round(float(row[2]) * self.multiplier, 6))
                    self.m3.append(round(float(row[3]) * self.multiplier, 6))
                    self.m4.append(round(float(row[4]) * self.multiplier, 6))
                    self.m5.append(0)
                    self.m40.append(round(float(row[5]) * self.multiplier, 6))
                    self.m6.append(0)
        print('msHiden - Datafile has %s rows' % len(self.time))
        print('msHiden: Calculating bestfit')
        self.bestfit = linbestfit(self.time, self.m3, self.m1, self.m4, settings['Ncc']['HD_H'])
        try:
            self.filename = self.next_id()
            print('msHiden: filename = %s' % self.filename)
            filepath = settings['MassSpec']['datadirectory'] + friendlydirname(str(self.batchid)
                                                                               + ' ' + self.batchdescription)
            os.makedirs(filepath, exist_ok=True)
            filename = filepath + '\\' + self.filename
            if self.identifier == 'Line Blank':
                line = 'LB@'
            else:
                line = self.identifier + '@'
            outfile = open(filename, 'w')
            # print('openng filepath = %s' % filename)
            for i in range(0, len(self.time)):
                line = line + '%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
                    self.time[i], self.m1[i], self.m3[i], self.m4[i], self.m5[i], self.m40[i], self.m6[i])
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
            print("msHiden: failed to write to helium results file %s " % Exception)
        try:
            database = sqlite3.connect(self.resultstabasepath)
            cursor_obj = database.cursor()
            sql_insert_query = """INSERT INTO HeliumRuns (id, type, identifier, daterun, batchdescription, batchid, 
             batchitemid, filedata, Bestfit) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) """
            datarow = (self.filename, self.type, self.identifier, datetime.now(), self.batchdescription, self.batchid,
                       self.batchitemid, blobfile, self.bestfit[1])
            cursor_obj.execute(sql_insert_query, datarow)
            database.commit()
            sql_insert_query = """INSERT INTO MSRawData (id, time, m1, m3, m4, m5, m40, m6) VALUES (?, ?, ?, ?, ?, ?, 
            ?, ?) """
            for i in range(0, len(self.time)):
                datarow = (
                    self.filename, self.time[i], self.m1[i], self.m3[i],
                    self.m4[i], self.m5[i], self.m40[i], self.m6[i])
                cursor_obj.execute(sql_insert_query, datarow)
            database.commit()
            settings['MassSpec']['nextH'] = self.next_id()
            writesettings()
        except sqlite3.Error as error:
            print("msHiden: failed to write to helium results database ", error)
        self.resetclass()


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


ms = MSClass()

if __name__ == '__main__':
    print('Starting ms class')
    print("ms.starttimer('Line Blank', 'Line Blank', 'manual test', 272, 3486)")
