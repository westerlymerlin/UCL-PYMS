import sqlite3
from datetime import datetime
import os
from settings import settings, friendlydirname
from imagefiler import imager


class BatchClass:
    def __init__(self):
        self.id = -1                # ID number of the batch. -1 = not saved yet otherwise taken from database
        self.date = None
        self.description = None     # Batch description / planchet description
        self.type = None            # can be Simple Batch or Planchett
        self.runnumber = []         # ID of each item in the batch inc lb, q and samples
        self.cycle = []             # type of sycle required
        self.location = []          # hole location if needed
        self.identifier = []        # description of sample or qnumber
        self.status = []            # item status 0=to do, 1=complete, 2=cancelled
        self.changed = 0
        self.readdatabase()

    def readdatabase(self):
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = 'SELECT * from batchsteps WHERE status = 0'
        cursor_obj.execute(sql_query)
        batchlist = cursor_obj.fetchall()
        if len(batchlist) > 0:
            self.changed = 1
            self.id = batchlist[0][1]
            sql_query = """SELECT * from batches WHERE id = ? """
            cursor_obj.execute(sql_query, [str(batchlist[0][1])])
            batchdetails = cursor_obj.fetchall()
            self.date = batchdetails[0][1]
            self.description = batchdetails[0][2]
            self.type = batchdetails[0][3]
            for item in batchlist:
                self.runnumber.append(item[0])
                self.cycle.append(item[2])
                self.location.append(item[3])
                self.identifier.append(item[4])
                self.status.append(item[5])
        database.close()

    def cancel(self):
        try:
            database = sqlite3.connect(settings['database']['databasepath'])
            cursor_obj = database.cursor()
            sql_query = 'SELECT * from batchsteps WHERE status = 0'
            cursor_obj.execute(sql_query)
            batchlist = cursor_obj.fetchall()
            if len(batchlist) > 0:
                self.id = batchlist[0][1]
                sql_update_query = """ UPDATE batchsteps SET status = 2 WHERE id = ?  """
                for item in batchlist:
                    datarow = [(str(self.id))]
                    cursor_obj.execute(sql_update_query, datarow)
                database.commit()
            database.close()
            self.changed = 1
            self.id = -1
            self.date = None
            self.description = None
            self.type = None
            self.runnumber = []
            self.cycle = []
            self.location = []
            self.identifier = []
            self.status = []
        except sqlite3.OperationalError:
            print('batchclass batch cancel error')

    def new(self, batchtype, description):
        if self.id > 0:
            self.cancel()
        self.type = batchtype
        self.description = description
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def addstep(self, cycle, location, identifier):
        self.runnumber.append(-1)
        self.cycle.append(cycle)
        self.location.append(location)
        self.identifier.append(identifier)
        self.status.append(0)

    def save(self):
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        self.changed = 1
        if self.id == -1:
            sql_insert_query = """ INSERT INTO batches (date, description, type) VALUES (?, ?, ?)"""
            datarow = (self.date, self.description, self.type)
            cursor_obj.execute(sql_insert_query, datarow)
            self.id = cursor_obj.lastrowid
        else:
            sql_update_query = """ UPDATE batches SET description = ? WHERE id = ?"""
            datarow = (self.description, str(self.id))
            cursor_obj.execute(sql_update_query, datarow)
        database.commit()
        itemcounter = 0
        if self.type == 'planchet':
            self.recalulateplanchet()
        for item in self.runnumber:
            if item == -1:
                sql_insert_query = """INSERT INTO batchsteps (id, cycle, location, identifier, status) VALUES (?, ?, 
                ?, ?, ?) """
                if self.cycle[itemcounter] == 'Q-Standard':
                    self.identifier[itemcounter] = self.newq()
                datarow = (self.id, self.cycle[itemcounter], self.location[itemcounter],
                           self.identifier[itemcounter], 0)
                cursor_obj.execute(sql_insert_query, datarow)
                self.runnumber[itemcounter] = cursor_obj.lastrowid
            else:
                sql_update_query = """UPDATE batchsteps SET cycle = ?, location = ?,  identifier = ?, status = ? 
                WHERE runnumber = ? """
                datarow = (self.cycle[itemcounter], self.location[itemcounter], self.identifier[itemcounter],
                           self.status[itemcounter], self.runnumber[itemcounter])
                cursor_obj.execute(sql_update_query, datarow)
            itemcounter = itemcounter + 1
        database.commit()
        database.close()

    def current(self):
        if len(self.runnumber) > 0:
            # print('there is a batch %s' % len(self.cycle))
            return [self.cycle[0], self.location[0], self.identifier[0]]
        else:
            # print('no batch left')
            return ['End', 'S1', 'No more samples to process']

    def completecurrent(self):
        if len(self.runnumber) > 0:
            print('Complete Current: Updating main database')
            database = sqlite3.connect(settings['database']['databasepath'])
            cursor_obj = database.cursor()
            sql_update_query = """ UPDATE batchsteps SET  status = 1 WHERE runnumber = ?  """
            cursor_obj.execute(sql_update_query, [str(self.runnumber[0])])
            database.commit()
            database.close()
            print('Complete Current: Creating Results Directory')
            filepath = settings['MassSpec']['datadirectory'] + \
                       friendlydirname(str(self.id) + ' ' + self.description)
            os.makedirs(filepath, exist_ok=True)
            formatteddata = ['Date                File         Description             Best Fit']
            print('Complete Current: Opening Results Database')
            database = sqlite3.connect(settings['database']['resultsdatabasepath'])
            cursor_obj = database.cursor()
            sql_query = """SELECT id, identifier, daterun, bestfit from HeliumRuns WHERE batchid = ? """
            cursor_obj.execute(sql_query, [str(self.id)])
            datarows = cursor_obj.fetchall()
            for datarow in datarows:
                formatteddata.append(
                    '%s    %s    %s    %.3f' % (datarow[2][:16], datarow[0], datarow[1].ljust(20, ' '), datarow[3]))
            database.close()
            print('Complete Current: Writing Results File')
            filename = filepath + '\\' + 'batchlog.txt'
            logfile = open(filename, 'w')
            for formattedline in formatteddata:
                print(formattedline, file=logfile)
            logfile.close()
            del self.runnumber[0]
            del self.cycle[0]
            del self.location[0]
            del self.identifier[0]
            del self.status[0]
            self.changed = 1
            # print('Remaining cycles are %s' % self.runnumber)
        if len(self.runnumber) == 0:
            self.id = -1
            self.date = None
            self.description = None
            self.type = None

    def list(self):
        index = 0
        returnval = []
        for i in self.runnumber:
            returnval.append([self.runnumber[index], self.cycle[index], self.location[index], self.identifier[index]])
            index = index + 1
        return returnval

    def listformatted(self):
        index = 0
        returnval = []
        for i in self.runnumber:
            datapoint = '%s ' % self.runnumber[index]
            datapoint = datapoint + self.cycle[index]
            if self.cycle[index][:6] == 'Sample':
                datapoint = datapoint + ', HOLE_' + self.location[index] + '_' + self.identifier[index]
            if self.cycle[index] == 'Q-Standard':
                datapoint = datapoint + ', Q' + self.identifier[index]
            returnval.append(datapoint)
            index = index + 1
        if len(returnval) == 0:
            returnval = ['00: End']
        return returnval

    def formatsample(self):
        if len(self.identifier) == 0:
            return '-'
        else:
            if self.cycle[0][:6] == 'Sample':
                return 'HOLE_' + self.location[0] + '_' + self.identifier[0]
            elif self.cycle[0] == 'Q-Standard':
                return 'Q' + self.identifier[0]
            else:
                return self.cycle[0]

    def currentdescription(self):
        if self.id == -1:
            return 'No batch loaded'
        else:
            return self.description

    def currentcycle(self):
        if self.id == -1:
            return 'No batch loaded'
        else:
            return self.cycle[0]

    def formatdescription(self):
        try:
            if self.id == -1:
                return 'No batch loaded'
            else:
                return '%s %s' % (self.id, self.description)
        except ValueError:
            return 'batch format description error'

    def getlocationsample(self, location):
        try:
            if len(location) == 2:
                return self.identifier[self.location.index(location)]
        except ValueError:
            return ''

    def insertcycle(self, index, cycle):
        self.runnumber.insert(index, -1)
        self.cycle.insert(index, cycle)
        self.location.insert(index, '')
        self.identifier.insert(index, '')
        self.status.insert(index, 0)

    def recalulateplanchet(self):
        if len(self.runnumber) > 37:
            insertpos = int(len(self.runnumber)/2)
            self.insertcycle(insertpos, 'Q-Standard')
            self.insertcycle(insertpos, 'Line Blank')
            self.insertcycle(insertpos, 'Pump')
        self.insertcycle(0, 'Q-Standard')
        self.insertcycle(0, 'Line Blank')
        self.insertcycle(len(self.runnumber), 'Q-Standard')
        self.insertcycle(len(self.runnumber), 'Line Blank')
        self.insertcycle(len(self.runnumber), 'Unload')

    def newq(self):
        q = settings['MassSpec']['nextQ']
        settings['MassSpec']['nextQ'] = q + 1
        return str(q)

    def nextlocation(self):
        for loc in self.location[1:]:
            if loc != '':
                return loc
        return 'UL'

    def locxy(self, loc):
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = """SELECT * from locations WHERE location = ?"""
        cursor_obj.execute(sql_query, [loc])
        datarow = cursor_obj.fetchall()[0]
        database.close()
        xpos = datarow[1]
        ypos = datarow[2]
        return xpos, ypos

    def isitthereyet(self, currentXPos, currentYPos):
        if len(self.location) <= 1:
            return True
        if self.location[1] == '':
            return True
        else:
            loc = self.locxy(self.location[1])
            if abs(loc[0] - currentXPos) < 0.05:
                print('batchclass x is on location')
                if abs(loc[1] - currentYPos) < 0.05:
                    print('batchclass y is on location')
                    return True
        return False

    def results(self):
        try:
            database = sqlite3.connect(settings['database']['resultsdatabasepath'])
            cursor_obj = database.cursor()

            if self.id > 0:
                batchid = self.id
            else:
                sql_query = """SELECT MAX(daterun), batchid from HeliumRuns"""
                cursor_obj.execute(sql_query)
                datarows = cursor_obj.fetchall()
                print(datarows)
                batchid = datarows[0][1]
            sql_query = """SELECT id, identifier, daterun, bestfit from HeliumRuns WHERE batchid = ? """
            cursor_obj.execute(sql_query, [str(batchid)])
            datarows = cursor_obj.fetchall()
            return datarows
        except:
            print('batchclass batch results error - %s' % Exception)
            return ['0', 'Batch Error', 'today', 1]

    def image(self, application):
        sampleid = 'IMG' + str(self.runnumber[0]) + '_' + self.formatsample()
        imager(application, str(self.id), self.description, sampleid)


batch = BatchClass()
