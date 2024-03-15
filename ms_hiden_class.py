"""Class to read data from a Hiden Mass Spectrometer and calculate the best-fit value for t=0"""
import socket
from datetime import datetime
import os
import threading
import time
import sqlite3
from settings import settings, writesettings, friendlydirname
from backup import backupfile
from ncc_calc import linbestfit
from logmanager import logger


class MsClass:
    """
    Class representing a Hiden Mass Spectrometer.

    Attributes:
    - __resultstabasepath: str - the path to the results database
    - __midfile: str - the name of the Hiden MID file
    - __profilefile: str - the name of the Hiden profile file
    - __runfile: str - the name of the run file
    - __host: str - the host of the Hiden Mass Spectrometer
    - __port: int - the port of the Hiden Mass Spectrometer
    - __multiplier: float - the multiplier used in calculations
    - timeoutretries: int - the maximum number of timeout retries
    - time: list - a list of time values
    - m1: list - a list of m1 values
    - m3: list - a list of m3 values
    - m4: list - a list of m4 values
    - m5: list - a list of m5 values
    - m40: list - a list of m40 values
    - m6: list - a list of m6 values
    - bestfit: int - the best fit value
    - id: str - the MS file ID in the format HEnnnnnR
    - type: str - the file type
    - filename: str - the file name
    - identifier: str - the sample identifier
    - daterun: datetime - the date and time the run was started
    - batchdescription: str - the batch description
    - batchid: int - the batch ID
    - batchitemid: int - the batch item ID
    - socketreturn: int - the return value from the socket
    - running: bool - indicates whether the run is currently in progress
    - timeoutcounter: int - counter for the number of timeouts

    Methods:
    - command_parser(command: str) -> int: Processes a command for the quad target
    - resetclass(): Resets class variables to their default values
    - starttimer(batchtype: str, identifier: str, batchdescription: str, batchid: int, batchitemid: int): Starts a timer
    - check_quad_is_online() -> str: Self test to check if the quad is online and ready
    - start_mid() -> List[str]: Starts a multiple ion detection run on the Hiden Mass Spectrometer
    - start_profile() -> List[str]: Starts a 1 to 10 amu scan on the Hiden Mass Spectrometer
    - getdata() -> List[List[str]]: Requests mid data from the Hiden Mass Spectrometer
    - getcolumns() -> List[str]: Requests columns from the Hiden Mass Spectrometer
    - getcycle(): Requests cycles from the Hiden Mass Spectrometer
    """
    def __init__(self):
        #  self.databasepath = settings['database']['databasepath']
        self.resultstabasepath = settings['database']['resultsdatabasepath']
        self.midfile = settings['MassSpec']['hidenMID']
        self.profilefile = settings['MassSpec']['hidenProfile']
        self.runfile = settings['MassSpec']['hidenRunfile']
        self.host = settings['MassSpec']['hidenhost']
        self.port = settings['MassSpec']['hidenport']
        self.multiplier = 1 / settings['MassSpec']['multiplier']
        self.timeoutretries = settings['MassSpec']['timeoutretries']
        self.resetclass()
        self.time = []
        self.m1 = []
        self.m3 = []
        self.m4 = []
        self.m5 = []
        self.m40 = []
        self.m6 = []
        self.bestfit = []
        self.id = self.next_id()  # MS File ID in the format HEnnnnnR
        self.type = ''  # File Type
        self.filename = ''  # File Name
        self.identifier = ''  # Sample Identifier
        self.daterun = datetime.now()
        self.batchdescription = ''  # Batch description (For file path)
        self.batchid = 0  # Batch ID (For file path)
        self.batchitemid = 0
        self.socketreturn = 0
        self.running = False
        self.timeoutcounter = 0

    def command_parser(self, command):
        """Command processor for any cycle command with 'quad' as its target"""
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
        """Reset class variables to their default"""
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
        """Start timer - used as t=0 when calculating best-fits"""
        logger.debug('msHiden: start timer %s, %s, %s, %s, %s,', batchtype, identifier, batchdescription,
                     batchid, batchitemid)
        self.daterun = datetime.now()
        self.id = self.next_id()
        self.type = batchtype
        self.identifier = identifier
        self.batchdescription = batchdescription
        self.batchid = batchid
        self.batchitemid = batchitemid

    def check_quad_is_online(self):
        """Self test to check the quad is online and ready"""
        try:
            s = socket.create_connection((self.host, self.port), .5)
            s.recv(1024).decode()
            s.send(bytes('-xStatus \r\n', 'utf-8'))
            status = s.recv(1024).decode()
            # logger.debug('MsHiden status recieved = %s', status[:-2])
            self.timeoutcounter = 0
            if status[:-2] == 'Unavailable':
                logger.error('msHiden - return of Unavailable, the software cannot access the RGA')
                return 'Unavailable'
            return status[:-2]
        except socket.timeout:
            self.timeoutcounter += 1
            logger.warning('msHiden - Timeout to MS software - try %s', self.timeoutcounter)
            return 'Off Line'

    def start_mid(self):
        """Start a multiple ion detection run on the Hiden Mass Spectrometer"""
        runningfile = 'none  '
        s = socket.create_connection((self.host, self.port), .5)
        self.socketreturn = s.recv(1024).decode()
        s.send(bytes('-xStatus \r\n', 'utf-8'))
        status = s.recv(1024).decode()
        logger.debug('Status = %s', status)
        if status[:-2] in ('StoppedShutDown', 'Protected'):
            s.send(bytes('-f"%s" \r\n' % self.midfile, 'utf-8'))
            try:
                self.socketreturn = s.recv(1024).decode()
            except socket.timeout:
                time.sleep(4)
                self.socketreturn = s.recv(1024).decode()
            s.send(bytes('-xFilename \r\n', 'utf-8'))
            runningfile = s.recv(1024).decode()
            logger.debug('Loaded file - %s', runningfile)
            time.sleep(1)
            s.send(bytes('-xGo %s \r\n' % self.runfile, 'utf-8'))
            time.sleep(.5)
            # self.socketreturn = s.recv(1024).decode()
            time.sleep(2)
            s.send(bytes('-xStatus \r\n', 'utf-8'))
            status = s.recv(1024).decode()
            logger.debug('Run file status = %s', status)
            self.running = True
        s.close()
        return [runningfile[:-2], status[:-2]]

    def start_profile(self):
        """Start a 1 to 10 amu scan on the Hiden Mass Spectrometer"""
        runningfile = 'none  '
        s = socket.create_connection((self.host, self.port), .5)
        self.socketreturn = s.recv(1024).decode()
        s.send(bytes('-xStatus \r\n', 'utf-8'))
        status = s.recv(1024).decode()
        logger.debug('Status = %s', status)
        if status[:-2] in ('StoppedShutDown', 'Protected', 'Available'):
            s.send(bytes('-f"%s" \r\n' % self.profilefile, 'utf-8'))
            try:
                self.socketreturn = s.recv(1024).decode()
            except socket.timeout:
                time.sleep(4)
                self.socketreturn = s.recv(1024).decode()
            s.send(bytes('-xFilename \r\n', 'utf-8'))
            runningfile = s.recv(1024).decode()
            logger.debug('Loaded file - %s', runningfile)
            time.sleep(1)
            s.send(bytes('-xGo %s \r\n' % self.runfile, 'utf-8'))
            # self.socketreturn = s.recv(1024).decode()
            time.sleep(2)
            s.send(bytes('-xStatus \r\n', 'utf-8'))
            status = s.recv(1024).decode()
            logger.debug('Run file status = %s', status)
            self.running = True
        s.close()
        return [runningfile[:-2], status[:-2]]

    def getdata(self):
        """Request mid data from Hiden Mass Spectrometer"""
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
        """Request columns from Hiden Mass Spectrometer"""
        s = socket.create_connection((self.host, self.port), .5)
        self.socketreturn = s.recv(1024).decode()
        s.send(bytes('-lLegends -v1 \r\n', 'utf-8'))
        legends = s.recv(1024).decode()
        s.close()
        return legends.split('\t')

    def getcycle(self):
        """Request cycles from Hiden Mass Spectrometer"""
        s = socket.create_connection((self.host, self.port), .5)
        self.socketreturn = s.recv(1024).decode()
        s.send(bytes('-lCycle -v1 \r\n', 'utf-8'))
        scycle = s.recv(1024).decode()
        s.close()
        return scycle

    def getenv(self):
        """Request environment from Hiden Mass Spectrometer"""
        s = socket.create_connection((self.host, self.port), .5)
        self.socketreturn = s.recv(1024).decode()
        s.send(bytes('-lEnvironment -v1 \r\n', 'utf-8'))
        senv = s.recv(1024).decode()
        s.close()
        logger.debug('Hidenclass: %s', senv)

    def getloadedfile(self):
        """Return the loaded file from the Hiden Mass Spectrometer"""
        s = socket.create_connection((self.host, self.port), .5)
        self.socketreturn = s.recv(1024).decode()
        s.send(bytes('-xFilename \r\n', 'utf-8'))
        senv = s.recv(1024).decode()
        s.close()
        logger.debug('Hidenclass filename: %s', senv)

    def stop_runnning(self):
        """Stop the running experiment on the Hiden Mass Spectrometer"""
        s = socket.create_connection((self.host, self.port), .5)
        self.socketreturn = s.recv(1024).decode()
        s.send(bytes('-xStatus \r\n', 'utf-8'))
        status = s.recv(1024).decode()
        logger.debug('Status = %s', status)
        if self.running:
            self.running = False
            logger.info('msHiden - Stopping Hiden')
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
        """Generate the next Helium run ID"""
        try:
            database = sqlite3.connect(self.resultstabasepath)
            cursor_obj = database.cursor()
            sql_query = "SELECT id FROM HeliumRuns ORDER BY id DESC LIMIT 1"
            cursor_obj.execute(sql_query)
            lastfile = cursor_obj.fetchall()
            nextfile = 'HE' + str(int(lastfile[0][0][2:-1]) + 1) + 'R'
            return nextfile
        except sqlite3.Error as error:
            logger.error("msHiden: next_id error %s", error)
            return "HE00000R"

    def writefile(self):
        """Write Helium Data file to disk"""
        data = self.getdata()
        for row in data:
            sampledate = (datetime.strptime(row[0], '%d/%m/%Y %H:%M:%S') - self.daterun).total_seconds()
            if sampledate > 0:
                self.time.append(round(sampledate, 6))
                self.m1.append(round(float(row[2]) * self.multiplier, 6))
                self.m3.append(round(float(row[3]) * self.multiplier, 6))
                self.m4.append(round(float(row[4]) * self.multiplier, 6))
                self.m5.append(0)
                self.m40.append(round(float(row[5]) * self.multiplier, 6))
                self.m6.append(0)
        logger.debug('msHiden - Datafile has %s rows', len(self.time))
        logger.debug('msHiden: Calculating bestfit')
        self.bestfit = linbestfit(self.time, self.m1, self.m3, self.m4)
        try:
            self.filename = self.next_id()
            logger.info('msHiden: filename = %s', self.filename)
            filepath = settings['MassSpec']['datadirectory'] + friendlydirname(str(self.batchid)
                                                                               + ' ' + self.batchdescription)
            os.makedirs(filepath, exist_ok=True)
            filename = filepath + '\\' + self.filename
            if self.identifier == 'Line Blank':
                line = 'LB@'
            else:
                line = self.identifier + '@'
            outfile = open(filename, 'w', encoding='utf-8')
            logger.debug('mshiden: openng filepath = %s', filename)
            for i in range(0, len(self.time)):
                line = line + '%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
                    self.time[i], self.m1[i], self.m3[i], self.m4[i], self.m5[i], self.m40[i], self.m6[i])
                print(line, file=outfile)
                line = ''
            outfile.close()
            backupfile(filename)
            logger.debug('closed filepath = %s', filename)
            writesettings()
            with open(filename, 'rb') as infile:
                blobfile = infile.read()
            infile.close()
        except:
            logger.error("msHiden: failed to write to helium results file %s ", Exception)
        try:
            database = sqlite3.connect(self.resultstabasepath)
            cursor_obj = database.cursor()
            sql_insert_query = ('INSERT INTO HeliumRuns (id, type, identifier, daterun, batchdescription, batchid,'
                                ' batchitemid, filedata, Bestfit) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ')
            datarow = (self.filename, self.type, self.identifier, datetime.now(), self.batchdescription, self.batchid,
                       self.batchitemid, blobfile, self.bestfit[1])
            cursor_obj.execute(sql_insert_query, datarow)
            database.commit()
            sql_insert_query = ('INSERT INTO MSRawData (id, time, m1, m3, m4, m5, m40, m6) VALUES '
                                '(?, ?, ?, ?, ?, ?, ?, ?)')
            for i in range(0, len(self.time)):
                datarow = (
                    self.filename, self.time[i], self.m1[i], self.m3[i],
                    self.m4[i], self.m5[i], self.m40[i], self.m6[i])
                cursor_obj.execute(sql_insert_query, datarow)
            database.commit()
            settings['MassSpec']['nextH'] = self.next_id()
            writesettings()
        except sqlite3.Error as error:
            logger.error('msHiden: failed to write to helium results database %s', error)
        self.resetclass()


ms = MsClass()

if __name__ == '__main__':
    print('Starting ms class')
    print("ms.starttimer('Line Blank', 'Line Blank', 'manual test', 272, 3486)")
