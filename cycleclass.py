"""
Module for managing and manipulating cycle information in a system.

This module defines the `CycleClass`, which represents a cycle and provides functionality for
retrieving and setting cycle information, as well as managing the steps within a cycle. The cycle
information is loaded from a database, and the class includes methods to query and process cycle data.
"""
import sqlite3
from app_control import settings
from logmanager import logger


class CycleClass:
    """

    :class: CycleClass

    The CycleClass represents a cycle in a system. It stores information such as the current cycle name, description,
     status, laser power, available cycle names, samples, locations, step times, targets, and commands.
     It also provides methods to manipulate and retrieve information about the cycle.

    Attributes:
    - id (int): The ID of the current cycle.
    - name (str): The name of the current cycle.
    - description (str): The description of the current cycle.
    - enabled (bool): The status of the current cycle.
    - laserpower (float): The laser power of the current cycle.
    - cycles (list): The list of available cycle names.
    - samples (list): The available cycle names that process samples and use the laser.
    - locations (list): The list of all locations on the planchet.
    - steptime (list): The list of step times for the current cycle.
    - steptarget (list): The list of targets for each step in the current cycle.
    - stepcommand (list): The list of commands for each step in the current cycle.

    Methods:
    - read_database(): Get the list of enabled cycles from the database.
    - setcycle(name: str): Set the current cycle to the given name and retrieve all the steps.
    - current(): Return the current cycle name and description.
    - currenttask(time: float): Return the current task at the given time.
    - currentstep(): Return the current step.
    - completecurrent(): Delete the current step as it has been completed.
    - steplist(): Return the list of steps to be completed.
    - steplistformatted(): Generate a formatted list of steps as a list of strings.
    - sample(cycleitem: str): Check if an item is in the list of samples.

    """

    def __init__(self):
        self.id = -1
        self.name = None  # The name of the current cycle
        self.description = None  # The description of the current cycle
        self.enabled = True  # the status of the current cycle
        self.laserpower = 0  # The laserpower of the current cycle
        self.cycles = []  # The list of available cycle names
        self.samples = []  # Is the available cycle one that processes samples and uses the laser
        self.locations = []  # the list of all locations on the planchet
        self.steptime = []  # current cycle list of step times
        self.steptarget = []  # current cycle list of targets
        self.stepcommand = []  # current cycle list of commands
        self.readdatabase()

    def readdatabase(self):
        """
        Reads data from the configured database and updates the instance with retrieved records.

        The method performs the following operations:
        1. Connects to the database using the specified configuration.
        2. Retrieves a list of enabled cycles from the 'cycles' table and updates the internal cycles list.
        3. Identifies cycles marked as samples and adds them to the internal samples list.
        4. Retrieves all entries from the 'locations' table and updates the internal locations list.
        5. Closes the database connection after all operations are complete.
        """
        self.cycles.append('End')
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = 'SELECT name, issample from cycles WHERE enabled = 1'
        cursor_obj.execute(sql_query)
        returnobjects = cursor_obj.fetchall()
        for cycle in returnobjects:
            self.cycles.append(cycle[0])
            if cycle[1]:
                self.samples.append((cycle[0]))
        sql_query = 'SELECT * from locations'
        cursor_obj.execute(sql_query)
        returnobjects = cursor_obj.fetchall()
        for location in returnobjects:
            self.locations.append(location[0])
        database.close()

    def setcycle(self, name):
        """
        Sets the current cycle to the specified name if it exists in the list of available cycles.
        If the name is not found, logs a warning. Retrieves cycle data from the database and populates
        the object's attributes with its details and associated steps. The method skips further
        execution if the name is 'End'.
        """
        if name not in self.cycles:
            logger.warning('Cycle Class: set cycle %s name not found', name)
            return
        if name == 'End':
            return
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = """SELECT * from cycles WHERE name = ?"""
        cursor_obj.execute(sql_query, [name])
        returnobjects = cursor_obj.fetchall()
        self.id = returnobjects[0][0]
        self.name = name
        self.description = returnobjects[0][2]
        self.enabled = returnobjects[0][3]
        self.laserpower = returnobjects[0][4]
        sql_query = """SELECT * from cyclesteps WHERE id = ?"""
        cursor_obj.execute(sql_query, [self.id])
        returnobjects = cursor_obj.fetchall()
        self.steptime = []
        self.steptarget = []
        self.stepcommand = []
        for task in returnobjects:
            self.steptime.append(task[1])
            self.steptarget.append(task[2])
            self.stepcommand.append(task[3])

    def current(self):
        """
        Returns information about the current object.

        This method compiles selected details of the object, such as its
        name and description, into a list. It is useful for obtaining a
        quick summary of the primary attributes of the object.
        """
        return [self.name, self.description]

    def currenttask(self, time):
        """
        Determines and returns the current task based on the given time.

        The method evaluates whether the provided time matches the scheduled
        time of the next step in the process and returns the respective
        task details. If no task matches the time, it provides default
        values indicating either no task or the end of the tasks.
        """
        if len(self.steptime) > 0:
            if time == self.steptime[0]:
                return [self.steptime[0], self.steptarget[0], self.stepcommand[0]]
            return [time, 'No task', 'No task']
        return [1, 'End', 'End']

    def currentstep(self):
        """
        Returns the current step details if available, otherwise returns the default
        step representation. The method checks if there are steps recorded and, if so,
        returns the first step's information. If no steps are present, it defaults to
        returning an end step.
        """
        if len(self.steptime) > 0:
            return [self.steptime[0], self.steptarget[0], self.stepcommand[0]]
        return [1, 'End', 'End']

    def completecurrent(self):
        """
        Complete the current step in the process.

        This method removes the oldest step details from the relevant attributes
        to mark the current step as completed. It logs the completion details
        including the step time, target, and command of the current step
        before removing them from their respective attributes.
        """
        if len(self.steptime) >= 0:
            logger.debug('completed %s %s %s ', self.steptime[0], self.steptarget[0], self.stepcommand[0])
            del self.steptime[0]
            del self.steptarget[0]
            del self.stepcommand[0]

    def steplist(self):
        """
        Generates a list of step details combining step time, target, and command information.
        """
        index = 0
        returnval = []
        for _ in self.steptime:
            returnval.append([self.steptime[index], self.steptarget[index], self.stepcommand[index]])
            index = index + 1
        return returnval

    def steplistformatted(self):
        """
        Generates a formatted list of steps based on step time, target, and command.

        This method combines the attributes `steptime`, `steptarget`, and `stepcommand` into
        a formatted list of strings. Each string contains the values from these attributes
        at the corresponding index, separated by commas. If no steps exist, a default step
        (`1, End, End`) is returned.
        """
        index = 0
        returnval = []
        for _ in self.steptime:
            returnval.append('%s, %s, %s' % (self.steptime[index], self.steptarget[index], self.stepcommand[index]))
            index = index + 1
        if len(returnval) == 0:
            returnval = ['1, End, End']
        return returnval

    def sample(self, cycleitem):
        """
        Checks if a given item exists in the sample list.

        This method iterates through the 'samples' attribute and compares each
        item with the provided 'cycleitem'. If the 'cycleitem' matches any item
        in the list, the method returns True; otherwise, it returns False.
        """
        for item in self.samples:
            if cycleitem == item:
                return True
        return False


currentcycle = CycleClass()
