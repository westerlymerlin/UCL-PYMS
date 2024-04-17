"""
BatchClass - used to manage a batch of cycles (samples, blanks, qshots or other tasks)
"""
import sqlite3
from datetime import datetime, timedelta
import os
from app_control import settings, friendlydirname, writesettings
from logmanager import logger
from imagefiler import imager
from ncc_calc import ncc
from cycleclass import currentcycle


class BatchClass:
    """
    The `BatchClass` represents a batch of samples or planchets. It allows for the creation, modification, and
    completion of batch steps. The class interacts with a SQLite database to store
    and retrieve batch information.

    Attributes:
        id (int): ID number of the batch. -1 indicates that the batch has not been saved yet, otherwise it is taken from
        the database.
        date (datetime): The date and time when the batch was created.
        description (str): The description or name of the batch.
        type (str): The type of batch. Can be either 'Simple Batch' or 'Planchet'.
        runnumber (list[int]): A list of ID numbers of each item in the batch, including the samples.
        cycle (list[str]): A list of the type of cycle required for each item.
        location (list[str]): A list of the hole location if needed for each item.
        identifier (list[str]): A list of the description of the sample or qnumber for each item.
        status (list[int]): A list of the status of each item. 0 indicates 'to do', 1 indicates 'complete', and 2
        indicates 'cancelled'.
        changed (int): A flag indicating whether the batch has been modified since the last save.

    Methods:
        readdatabase()
            Reads the PyMS database for any open batches.

        cancel()
            Used to cancel a batch. Marks all samples as cancelled and closes the batch.

        new(batchtype: str, description: str)
            Creates a new batch with the specified batch type and description.

        addstep(cycle: str, location: str, identifier: str)
            Adds a sample to the batch.

        save()
            Saves the batch details to the database.

        current()
            Returns the details of the current batch step or 'End' if there are no more steps.

        completecurrent()
            Marks the current batch step as complete.

        writebatchlog()
            Generates the batchlog.csv file for the batch.
    """
    def __init__(self):
        self.id = -1                # ID number of the batch. -1 = not saved yet otherwise taken from database
        self.date = None
        self.description = None     # Batch description / planchet description
        self.type = None            # can be Simple Batch or Planchett
        self.runnumber = []         # ID of each item in the batch inc lb, q and samples
        self.cycle = []             # type of cycle required
        self.location = []          # hole location if needed
        self.identifier = []        # description of sample or qnumber
        self.status = []            # item status 0=to do, 1=complete, 2=cancelled
        self.changed = 0
        self.readdatabase()

    def readdatabase(self):
        """Reads the PyMS database for any open batches"""
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
        """Used to cancel a batch - marks all samples and cancelled and closes the batch"""
        try:
            database = sqlite3.connect(settings['database']['databasepath'])
            cursor_obj = database.cursor()
            sql_query = 'SELECT * from batchsteps WHERE status = 0'
            cursor_obj.execute(sql_query)
            batchlist = cursor_obj.fetchall()
            if len(batchlist) > 0:
                self.id = batchlist[0][1]
                sql_update_query = """ UPDATE batchsteps SET status = 2 WHERE id = ?  """
                for _ in batchlist:
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
            logger.error('BatchClass-batchclass batch cancel error')

    def new(self, batchtype, description):
        """Creates a new batch ***batchtype*** is 'simple' or 'planchet'"""
        if self.id > 0:
            self.cancel()
        self.type = batchtype
        self.description = description
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def addstep(self, cycle, location, identifier):
        """Adds a sample to a batch"""
        self.runnumber.append(-1)
        self.cycle.append(cycle)
        self.location.append(location)
        self.identifier.append(identifier)
        self.status.append(0)

    def save(self):
        """Save to database"""
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
                sql_insert_query = 'INSERT INTO batchsteps (id, cycle, location, identifier, status)' \
                                   ' VALUES (?, ?, ?, ?, ?)'
                if self.cycle[itemcounter] == 'Q-Standard':
                    self.identifier[itemcounter] = self.newq()
                datarow = (self.id, self.cycle[itemcounter], self.location[itemcounter],
                           self.identifier[itemcounter], 0)
                cursor_obj.execute(sql_insert_query, datarow)
                self.runnumber[itemcounter] = cursor_obj.lastrowid
            else:
                sql_update_query = 'UPDATE batchsteps SET cycle = ?, location = ?,  identifier = ?, status = ?' \
                                   '  WHERE runnumber = ?'
                datarow = (self.cycle[itemcounter], self.location[itemcounter], self.identifier[itemcounter],
                           self.status[itemcounter], self.runnumber[itemcounter])
                cursor_obj.execute(sql_update_query, datarow)
            itemcounter = itemcounter + 1
        database.commit()
        database.close()
        writesettings()

    def current(self):
        """Returns current step or 'End' if there are no more steps"""
        if len(self.runnumber) > 0:
            logger.debug('BatchClass-there is a batch %s', len(self.cycle))
            return [self.cycle[0], self.location[0], self.identifier[0]]
        logger.debug('BatchClass-no batch left')
        return ['End', 'S1', 'No more samples to process']

    def completecurrent(self):
        """Mark the current task in the bach complete"""
        if len(self.runnumber) > 0:  # move on to the next task
            logger.info('BatchClass-Complete Current: Updating main database')
            database = sqlite3.connect(settings['database']['databasepath'])
            cursor_obj = database.cursor()
            sql_update_query = """ UPDATE batchsteps SET  status = 1 WHERE runnumber = ?  """
            cursor_obj.execute(sql_update_query, [str(self.runnumber[0])])
            database.commit()
            database.close()
            self.writebatchlog()
            del self.runnumber[0]
            del self.cycle[0]
            del self.location[0]
            del self.identifier[0]
            del self.status[0]
            self.changed = 1
            logger.debug('BatchClass-Remaining cycles are %s', self.runnumber)
        if len(self.runnumber) == 0:  # all tasks completed
            self.id = -1
            self.date = None
            self.description = None
            self.type = None

    def writebatchlog(self):
        """Generate the batchlog.csv file"""
        try:
            logger.info('BatchClass-Complete Current: Creating Results Directory')
            filepath = settings['MassSpec']['datadirectory'] + \
                friendlydirname(str(self.id) + ' ' + self.description)
            os.makedirs(filepath, exist_ok=True)
            formatteddata = ['"Batch No:","%s"' % self.id, '"Batch Description:","%s"' % self.description, ' ',
                             '"Date","HE File","Description","Best Fit"']
            logger.info('BatchClass-Complete Current: Opening Results Database')
            database = sqlite3.connect(settings['database']['resultsdatabasepath'])
            cursor_obj = database.cursor()
            sql_query = """SELECT id, identifier, daterun, bestfit from HeliumRuns WHERE batchid = ? """
            cursor_obj.execute(sql_query, [str(self.id)])
            datarows = cursor_obj.fetchall()
            for datarow in datarows:
                formatteddata.append(
                    '"%s","%s","%s",%.3f' % (datarow[2][:16], datarow[0], datarow[1], datarow[3]))
            database.close()
            logger.info('BatchClass-Complete Current: Writing Results File')
            filename = filepath + '\\' + 'batchresults.csv'
            logfile = open(filename, 'w', encoding='utf-8')
            for formattedline in formatteddata:
                print(formattedline, file=logfile)
            logfile.close()
            ncc.filegenerator(filepath)
        except:
            logger.error("batchclass: Error createing batchlog")

    def list(self):
        """Return a list of all of the outstancing tasks"""
        index = 0
        returnval = []
        for _ in self.runnumber:
            returnval.append([self.runnumber[index], self.cycle[index], self.location[index], self.identifier[index]])
            index = index + 1
        return returnval

    def listformatted(self):
        """return a formatted list of all the outstanding tasks"""
        index = 0
        returnval = []
        for _ in self.runnumber:
            datapoint = '%s ' % self.runnumber[index]
            datapoint = datapoint + self.cycle[index]
            if currentcycle.sample(self.cycle[index]):
                datapoint = datapoint + ', HOLE_' + self.location[index] + '_' + self.identifier[index]
            if self.cycle[index] == 'Q-Standard':
                datapoint = datapoint + ', Q' + self.identifier[index]
            returnval.append(datapoint)
            index = index + 1
        if len(returnval) == 0:
            returnval = ['00: End']
        return returnval

    def formatsample(self):
        """Generate a meaningful sample name based on the pit in the planchet and samplid, Qshot or line blank"""
        if len(self.identifier) == 0:
            return '-'
        if currentcycle.sample(self.cycle[0]):
            return 'HOLE_' + self.location[0] + '_' + self.identifier[0]
        if self.cycle[0] == 'Q-Standard':
            return 'Q' + self.identifier[0]
        if self.cycle[0] == 'Index':
            return 'HOLE_' + self.location[0] + '_' + self.identifier[0]
        return self.cycle[0]

    def currentdescription(self):
        """Return the description attribute for the current batch"""
        if self.id == -1:
            return 'No batch loaded'
        return self.description

    def currentcycle(self):
        """Return the sysle type for the current task in the batch"""
        if self.id == -1:
            return 'No batch loaded'
        return self.cycle[0]

    def formatdescription(self):
        """Format the description based on the batch identifier and the descri[ption field"""
        try:
            if self.id == -1:
                return 'No batch loaded'
            return '%s %s' % (self.id, self.description)
        except ValueError:
            return 'batch format description error'

    def getlocationsample(self, location):
        """Return the location on the planchet of the current sample"""
        try:
            if len(location) == 2:
                return self.identifier[self.location.index(location)]
        except ValueError:
            return ''

    def insertcycle(self, index, cycle):
        """Insert a new task into the batch - used when a planchet is created to add in Q-shots and line blanks at
         the start, mid point and end"""
        self.runnumber.insert(index, -1)
        self.cycle.insert(index, cycle)
        self.location.insert(index, '')
        self.identifier.insert(index, '')
        self.status.insert(index, 0)

    def recalulateplanchet(self):
        """Calculate the positions of Q-shots, line blanks and unload tasks. Used when editing a planchet"""
        if len(self.runnumber) > 36:
            insertpos = int(len(self.runnumber)/2)
            self.insertcycle(insertpos, 'Q-Standard')
            self.insertcycle(insertpos, 'Line Blank')
            self.insertcycle(insertpos, 'Pump')
        self.insertcycle(0, 'Q-Standard')
        self.insertcycle(0, 'Line Blank')
        self.insertcycle(0, 'Line Clean')
        self.insertcycle(len(self.runnumber), 'Q-Standard')
        self.insertcycle(len(self.runnumber), 'Line Blank')
        self.insertcycle(len(self.runnumber), 'Unload')

    def newq(self):
        """Genrate the newxt Q-Shot number"""
        q = settings['MassSpec']['nextQ']
        settings['MassSpec']['nextQ'] = q + 1
        return str(q)

    def nextlocation(self):
        """Find the next location - used when moving laser to next spot. \n
        if there is no next location then the unload 'UL' location is given"""
        for loc in self.location[1:]:
            if loc != '':
                return loc
        return 'UL'

    def locxy(self, loc):
        """for a location **loc** find the x and y values from the database"""
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = """SELECT * from locations WHERE location = ?"""
        cursor_obj.execute(sql_query, [loc])
        datarow = cursor_obj.fetchall()[0]
        database.close()
        xpos = datarow[1]
        ypos = datarow[2]
        return xpos, ypos

    def isitthereyet(self, current_x_pos, current_y_pos):
        """Check if the laser has reached the desired location"""
        if len(self.location) <= 1:
            return True
        if self.location[1] == '':
            return True
        loc = self.locxy(self.location[1])
        if abs(loc[0] - current_x_pos) < 0.05:
            logger.info('BatchClass: x is on location')
            if abs(loc[1] - current_y_pos) < 0.05:
                logger.info('BatchClass: y is on location')
                return True
        return False

    def results(self):
        """return the best-fit values for all processed tasks in the batch"""
        try:
            database = sqlite3.connect(settings['database']['resultsdatabasepath'])
            cursor_obj = database.cursor()

            if self.id > 0:
                batchid = self.id
            else:
                sql_query = """SELECT MAX(daterun), batchid from HeliumRuns"""
                cursor_obj.execute(sql_query)
                datarows = cursor_obj.fetchall()
                logger.info('batchclass: - last batch = %s', datarows)
                batchid = datarows[0][1]
            sql_query = """SELECT id, identifier, daterun, bestfit from HeliumRuns WHERE batchid = ? """
            cursor_obj.execute(sql_query, [str(batchid)])
            datarows = cursor_obj.fetchall()
            return datarows
        except:
            logger.error('BatchClass-batchclass batch results error - %s', Exception)
            return ['0', 'Batch Error', 'today', 1]

    def image(self, application):
        """Calls the **imager** task from the imagefiler module to crab a screen shot of that window"""
        sampleid = 'IMG' + str(self.runnumber[0]) + '_' + self.formatsample()
        imager(application, str(self.id), self.description, sampleid)

    def finishtime(self):
        """Calculate the theorectical finish time of the current batch"""
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = 'SELECT  sum(cyclesteps.time) from batchsteps, cyclesteps, cycles WHERE batchsteps.cycle =' \
                    ' cycles.name and cycles.id = cyclesteps.id and batchsteps.status = 0 and cyclesteps.target = "end"'
        cursor_obj.execute(sql_query)
        dbreturn = cursor_obj.fetchall()
        totalseconds = dbreturn[0][0]
        database.close()
        logger.info('Time to add %s', totalseconds)
        if totalseconds is None:
            endtime = ''
        else:
            endtime = datetime.strftime(datetime.now() + timedelta(seconds=totalseconds),
                                        'Estimated End Time: %a %d %b %Y, %H:%M')
        return endtime


batch = BatchClass()
