"""
Batch management for PyMS.

This module provides a lightweight persistence layer and in-memory model for
building and executing a queue of measurement steps (a “batch”). A batch may be
a simple list of sample runs or a planchet layout; steps are stored in / loaded
from the project’s SQLite database and processed in order.

Key features:
- Create a new batch and append steps (cycle, location, identifier)
- Load any unfinished steps from the database on startup
- Persist batch metadata and steps (insert/update)
- Mark the current step complete, cancel remaining steps, and advance the queue
- Generate per-batch results output (CSV + NCC file generation)

Notes:
- Database paths and runtime settings are taken from the shared application
  settings.
- The module exposes a singleton-like `batch` instance for use by the UI and
  control code.
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
        read_database()
            Reads the PyMS database for any open batches.

        cancel_batch()
            Used to cancel_batch a batch. Marks all samples as cancelled and closes the batch.

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
        self.type = None            # can be Simple Batch or Planchet
        self.runnumber = []         # ID of each item in the batch inc lb, q and samples
        self.cycle = []             # type of cycle required
        self.location = []          # hole location if needed
        self.identifier = []        # description of sample or Q number
        self.status = []            # item status 0=to do, 1=complete, 2=cancelled
        self.changed = 0
        self.read_database()

    def read_database(self):
        """
        Reads the database to fetch batch step and batch details with specific status and updates
        relevant attributes accordingly. The method retrieves information on batch steps with a
        status of 0 and their corresponding batch details. Additionally, it updates internal
        statuses, identifiers, and other related attributes based on the retrieved data.
        """
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = 'SELECT * from batchsteps WHERE status = 0'
        cursor_obj.execute(sql_query)
        batch_list = cursor_obj.fetchall()
        if len(batch_list) > 0:
            self.changed = 1
            self.id = batch_list[0][1]
            sql_query = """SELECT * from batches WHERE id = ? """
            cursor_obj.execute(sql_query, [str(batch_list[0][1])])
            batch_details = cursor_obj.fetchall()
            self.date = batch_details[0][1]
            self.description = batch_details[0][2]
            self.type = batch_details[0][3]
            for item in batch_list:
                self.runnumber.append(item[0])
                self.cycle.append(item[2])
                self.location.append(item[3])
                self.identifier.append(item[4])
                self.status.append(item[5])
        database.close()

    def cancel_batch(self):
        """
        Cancels all batch steps with a status of 0 (unprocessed) and updates their status to 2 (cancelled).

        This method connects to the database, retrieves all batch steps with a status
        of 0, and updates their status to 2. It resets several internal attributes of
        the object to default values after successfully processing the batch steps.
        """
        try:
            database = sqlite3.connect(settings['database']['databasepath'])
            cursor_obj = database.cursor()
            sql_query = 'SELECT * from batchsteps WHERE status = 0'
            cursor_obj.execute(sql_query)
            batch_list = cursor_obj.fetchall()
            if len(batch_list) > 0:
                self.id = batch_list[0][1]
                sql_update_query = """ UPDATE batchsteps SET status = 2 WHERE id = ? and status = 0 """
                for _ in batch_list:
                    query_result = [(str(self.id))]
                    cursor_obj.execute(sql_update_query, query_result)
                database.commit()
            reset_q()
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
            logger.error('BatchClass cancel_batch error')

    def new(self, batch_type, description):
        """
        Creates a new batch with the specified type and description.

        This method initializes a new batch process by setting its type and description
        attributes, and assigns the current date and time to the batch. If the batch
        has already been created (identified by an id greater than 0), it cancels the
        current batch before proceeding.

        Parameters:
            batch_type: The type of the batch to be created.
            description: A description for the batch.
        """
        if self.id > 0:
            self.cancel_batch()
        self.type = batch_type
        self.description = description
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def addstep(self, cycle, location, identifier):
        """
        Adds a new step to track in the process by appending details to respective attributes.
        """
        self.runnumber.append(-1)
        self.cycle.append(cycle)
        self.location.append(location)
        self.identifier.append(identifier)
        self.status.append(0)

    def save(self):
        """
        Saves the current state of the batch object and its associated steps to the database. If the batch is new, it inserts
        a new batch record; otherwise, it updates the existing batch record. It also ensures that related batch steps are
        inserted or updated appropriately. If the batch type is 'planchet', additional recalculations are performed.
        """
        reset_q()
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        self.changed = 1
        if self.id == -1:
            sql_insert_query = """ INSERT INTO batches (date, description, type) VALUES (?, ?, ?)"""
            query_result = (self.date, self.description, self.type)
            cursor_obj.execute(sql_insert_query, query_result)
            self.id = cursor_obj.lastrowid
        else:
            sql_update_query = """ UPDATE batches SET description = ? WHERE id = ?"""
            query_result = (self.description, str(self.id))
            cursor_obj.execute(sql_update_query, query_result)
        database.commit()
        item_counter = 0
        if self.type == 'planchet':
            self.recalulateplanchet()
        for item in self.runnumber:
            if self.cycle[item_counter] == 'Q-Standard':
                self.identifier[item_counter] = next_q()
            if item == -1:
                sql_insert_query = 'INSERT INTO batchsteps (id, cycle, location, identifier, status)' \
                                   ' VALUES (?, ?, ?, ?, ?)'

                query_result = (self.id, self.cycle[item_counter], self.location[item_counter],
                           self.identifier[item_counter], 0)
                cursor_obj.execute(sql_insert_query, query_result)
                self.runnumber[item_counter] = cursor_obj.lastrowid
            else:
                sql_update_query = 'UPDATE batchsteps SET cycle = ?, location = ?,  identifier = ?, status = ?' \
                                   '  WHERE runnumber = ?'
                query_result = (self.cycle[item_counter], self.location[item_counter], self.identifier[item_counter],
                           self.status[item_counter], self.runnumber[item_counter])
                print(query_result)
                cursor_obj.execute(sql_update_query, query_result)
            item_counter = item_counter + 1
        database.commit()
        database.close()
        writesettings()

    def current(self):
        """
        Returns the details of the current batch being processed or a message indicating no batches remain.

        Summary:
        This method checks whether any batches are available for processing. If batches exist,
        it returns a list containing the current cycle, location, and identifier of the batch.
        If no batches are left, it returns a list with a message signaling the end of processing
        along with default placeholder values.
        """
        if len(self.runnumber) > 0:
            logger.debug('BatchClass-there is a batch %s', len(self.cycle))
            return [self.cycle[0], self.location[0], self.identifier[0]]
        logger.debug('BatchClass-no batch left')
        return ['End', 'S1', 'No more samples to process']

    def completecurrent(self):
        """
        Updates the current batch step status to 1 (completed) in the database and moves on to the next task if
        any remaining task exists. If all tasks are completed, it resets the relevant attributes
        to their default values.
        """
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
        """
        Writes a detailed log for the batch process, including batch metadata and results. The method handles directory
        creation, data retrieval from the database, CSV file generation, and integrates results into the specified
        output directory.
        """
        try:
            logger.info('BatchClass-Complete Current: Creating Results Directory')
            filepath = settings['MassSpec']['datadirectory'] + \
                friendlydirname(str(self.id) + ' ' + self.description)
            os.makedirs(filepath, exist_ok=True)
            formatted_data = ['"Batch No:","%s"' % self.id, '"Batch Description:","%s"' % self.description, ' ',
                             '"Date","HE File","Description","Best Fit"']
            logger.info('BatchClass-Complete Current: Opening Results Database')
            database = sqlite3.connect(settings['database']['resultsdatabasepath'])
            cursor_obj = database.cursor()
            sql_query = """SELECT id, identifier, daterun, bestfit from HeliumRuns WHERE batchid = ? """
            cursor_obj.execute(sql_query, [str(self.id)])
            query_result = cursor_obj.fetchall()
            for data_row in query_result:
                formatted_data.append(
                    '"%s","%s","%s",%.3f' % (data_row[2][:16], data_row[0], data_row[1], data_row[3]))
            database.close()
            logger.info('BatchClass-Complete Current: Writing Results File')
            filename = filepath + '\\' + 'batchresults.csv'
            logfile = open(filename, 'w', encoding='utf-8')
            for formatted_line in formatted_data:
                print(formatted_line, file=logfile)
            logfile.close()
            ncc.filegenerator(filepath)
        except:
            logger.error("BatchClass: Error creating batchlog file")

    def list(self):
        """
        Produces a consolidated list of details from multiple attributes.

        This method iterates through the values of `runnumber`, combining corresponding
        values from `cycle`, `location`, and `identifier` attributes to create a list of
        lists. Each inner list contains the following elements in order: `runnumber`,
        `cycle`, `location`, and `identifier`.
        """
        index = 0
        return_values = []
        for _ in self.runnumber:
            return_values.append([self.runnumber[index], self.cycle[index], self.location[index], self.identifier[index]])
            index = index + 1
        return return_values

    def listformatted(self):
        """
        Generates a formatted list of data points based on run numbers, cycles, and other attributes.

        Summary:
        The method iterates over the 'runnumber' list of the class, creating a formatted string for each
        data point. It combines the run number, cycle, and other attributes conditionally based on specific
        criteria. If no data points are processed, a default value is returned.
        """
        index = 0
        return_values = []
        for _ in self.runnumber:
            datapoint = '%s ' % self.runnumber[index]
            datapoint = datapoint + self.cycle[index]
            if currentcycle.sample(self.cycle[index]):
                datapoint = datapoint + ', HOLE_' + self.location[index] + '_' + self.identifier[index]
            if self.cycle[index] == 'Q-Standard':
                datapoint = datapoint + ', Q' + self.identifier[index]
            return_values.append(datapoint)
            index = index + 1
        if len(return_values) == 0:
            return_values = ['00: End']
        return return_values

    def formatsample(self):
        """
        Formatsample processes and formats a sample identifier based on its attributes and status.

        This method determines the appropriate formatting for a sample by checking its cycle
        status and related identifiers. Various conditions, such as whether the identifier is empty,
        or specific cycle values match preset categories (e.g., 'Q-Standard', 'Index'), are used
        to construct the formatted string.
        """
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
        """
        Returns the description of the current batch or a default message if no batch
        is loaded.

        This method checks the value of the 'id' attribute to determine whether a
        batch is loaded. If no batch is loaded (indicated by an 'id' value of -1),
        it returns a default message stating that no batch is loaded. Otherwise,
        it returns the description of the current batch.
        """
        if self.id == -1:
            return 'No batch loaded'
        return self.description

    def currentcycle(self):
        """
        Returns the current cycle of the loaded batch.

        This method retrieves the current cycle from the loaded batch. If no batch
        is loaded (indicated by `id` being -1), it returns a default message
        stating that no batch is loaded.
        """
        if self.id == -1:
            return 'No batch loaded'
        return self.cycle[0]

    def formatdescription(self):
        """
        Formats and returns a batch description string based on the batch ID and description.

        This method attempts to construct a string representation of the batch information.
        If the batch ID is set to -1, indicating no batch is loaded, a default message is returned.
        In case of exceptions during formatting, an error message is provided.
        """
        try:
            if self.id == -1:
                return 'No batch loaded'
            return '%s %s' % (self.id, self.description)
        except ValueError:
            return 'batch format description error'

    def getlocationsample(self, location):
        """
        Retrieves a sample identifier based on the provided location.

        This method attempts to fetch a corresponding identifier for
        the given location from the stored location list.
        """
        try:
            if len(location) == 2:
                return self.identifier[self.location.index(location)]
        except ValueError:
            return ''

    def insertcycle(self, index, cycle):
        """
        Inserts a new cycle and its associated default values at the specified index.

        This method modifies several attributes of the class by inserting a new entry at
        the given index. The inserted entry includes a cycle value and default values for
        other corresponding attributes.
        """
        self.runnumber.insert(index, -1)
        self.cycle.insert(index, cycle)
        self.location.insert(index, '')
        self.identifier.insert(index, '')
        self.status.insert(index, 0)

    def recalulateplanchet(self):
        """
        Recalculates the planchet for the current run.

        This method modifies the current run by inserting specific cycles at different
        positions in the run. If the run number length exceeds 36, additional cycles
        are inserted at the middle of the run. This is done to ensure standardization
        across the run phases.
        """
        if len(self.runnumber) > 36:
            insert_index = int(len(self.runnumber)/2)
            self.insertcycle(insert_index, 'Q-Standard')
            self.insertcycle(insert_index, 'Line Blank')
            self.insertcycle(insert_index, 'Pump')
        self.insertcycle(0, 'Q-Standard')
        self.insertcycle(0, 'Line Blank')
        self.insertcycle(0, 'Line Clean')
        self.insertcycle(len(self.runnumber), 'Q-Standard')
        self.insertcycle(len(self.runnumber), 'Line Blank')
        self.insertcycle(len(self.runnumber), 'Unload')


    def nextlocation(self):
        """
        Returns the next non-empty location from the list of locations or a fallback value.

        This method iterates through the `location` list, starting from the second
        element, to look for the first non-empty string. If all subsequent elements
        are empty, it returns a default value of 'UL'.
        """
        for loc in self.location[1:]:
            if loc != '':
                return loc
        return 'UL'

    def locxy(self, loc):
        """
        Retrieves the x and y coordinates of a specific location from the database.

        Fetches information from the locations table in the connected SQLite database
        to obtain the x and y positional values associated with the specified location name.
        """
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = """SELECT * from locations WHERE location = ?"""
        cursor_obj.execute(sql_query, [loc])
        query_result = cursor_obj.fetchall()[0]
        database.close()
        xpos = query_result[1]
        ypos = query_result[2]
        return xpos, ypos

    def isitthereyet(self, current_x_pos, current_y_pos):
        """
        Determines whether the current position is near the target location.

        The method checks if the given x and y coordinates are within a threshold
        distance from a specific target location. If the target location is not
        specified or only the initial location is available, it considers the position
        to have been reached by default. The method logs information when the x and y
        coordinates are verified as close to the target location.
        """
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
        """
        Fetches the results of the most recent or specified batch run from a SQLite database.

        This method retrieves records associated with a batch run from the database. If a specific batch
        ID (`self.id`) is greater than zero, it is used directly. Otherwise, the method identifies the
        most recent batch run using the `HeliumRuns` table. The results include details such as
        record ID, identifier, date of the run, and best fit for each entry within the specified or
        latest batch.
        """
        try:
            database = sqlite3.connect(settings['database']['resultsdatabasepath'])
            cursor_obj = database.cursor()

            if self.id > 0:
                batchid = self.id
            else:
                sql_query = """SELECT MAX(daterun), batchid from HeliumRuns"""
                cursor_obj.execute(sql_query)
                query_result = cursor_obj.fetchall()
                logger.info('batchclass: - last batch = %s', query_result)
                batchid = query_result[0][1]
            sql_query = """SELECT id, identifier, daterun, bestfit from HeliumRuns WHERE batchid = ? """
            cursor_obj.execute(sql_query, [str(batchid)])
            query_result = cursor_obj.fetchall()
            return query_result
        except:
            logger.error('BatchClass results error - %s', Exception)
            return ['0', 'Batch Error', 'today', 1]

    def image(self, application):
        """
        Formats a sample ID and initiates the imaging process for the application.

        This method creates a sample ID by combining a prefix with a unique run
        number and formatted sample data, then calls the `imager` function to
        carry out the imaging process. The generated `sample_id` is passed along
        with the application name, unique identifier, and description of the
        sample to the imaging function.
        """
        sample_id = 'IMG' + str(self.runnumber[0]) + '_' + self.formatsample()
        imager(application, str(self.id), self.description, sample_id)

    def finishtime(self):
        """
        Calculates the estimated finish time for a batch process.

        Connects to the database and calculates the total time of unfinished batch steps
        where their corresponding cycle steps have a target set to "end". Uses the current
        time and the total time retrieved from the database to compute the estimated end
        time.
        """
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = 'SELECT  sum(cyclesteps.time) from batchsteps, cyclesteps, cycles WHERE batchsteps.cycle =' \
                    ' cycles.name and cycles.id = cyclesteps.id and batchsteps.status = 0 and cyclesteps.target = "end"'
        cursor_obj.execute(sql_query)
        query_result = cursor_obj.fetchall()
        total_seconds = query_result[0][0]
        database.close()
        logger.info('Time to add %s', total_seconds)
        if total_seconds is None:
            endtime = ''
        else:
            endtime = datetime.strftime(datetime.now() + timedelta(seconds=total_seconds),
                                        'Estimated End Time: %a %d %b %Y, %H:%M')
        return endtime

def next_q():
    """
    Generates the next unique identifier for a MassSpec operation.

    The function retrieves the current value of the "nextQ" setting from the
    "MassSpec" configuration, increments it, updates the setting, and then
    returns the original value as a string.
    """
    q = settings['MassSpec']['nextQ']
    settings['MassSpec']['nextQ'] = q + 1
    return str(q)


def reset_q():
    """
    Resets the 'Q' number to the next available identifier.

    This method connects to the database, retrieves the last used identifier
    from the 'QNumbers' view, and updates the application settings with the
    next sequential number. If an error occurs during the process, it is logged.
    """
    try:
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = "SELECT identifier from QNumbers"
        cursor_obj.execute(sql_query)
        query_result = cursor_obj.fetchone()
        settings['MassSpec']['nextQ'] = int(query_result[0]) + 1
        writesettings()
        database.close()
    except sqlite3.OperationalError:
        logger.error('BatchClass - batch reset_q error')

batch = BatchClass()
