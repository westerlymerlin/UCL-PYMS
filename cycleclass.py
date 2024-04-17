"""
Cycle Class
Author: Gary Twinn
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
    - readdatabase(): Get the list of enabled cycles from the database.
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
        self.enabled = True  # the ststus of the current cycle
        self.laserpower = 0  # The laserpower of the current cycle
        self.cycles = []  # The list of available cycle names
        self.samples = []  # Is the available cycle one that processes samples and uses the laser
        self.locations = []  # the list of all locations on the planchet
        self.steptime = []  # current cycle list of step times
        self.steptarget = []  # current cycle list of targets
        self.stepcommand = []  # current cycle list of commands
        self.readdatabase()

    def readdatabase(self):
        """Get the list of enabled cycles from the database"""
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
        """Set the current cycle to the given name and retrieve all the steps (used when the cycle starts)"""
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
        """Return the current Cycle name and discription"""
        return [self.name, self.description]

    def currenttask(self, time):
        """Return the current task"""
        if len(self.steptime) > 0:
            if time == self.steptime[0]:
                return [self.steptime[0], self.steptarget[0], self.stepcommand[0]]
            return [time, 'No task', 'No task']
        return [1, 'End', 'End']

    def currentstep(self):
        """Return the current step"""
        if len(self.steptime) > 0:
            return [self.steptime[0], self.steptarget[0], self.stepcommand[0]]
        return [1, 'End', 'End']

    def completecurrent(self):
        """Delete the current step as it has been completed"""
        if len(self.steptime) >= 0:
            logger.debug('completed %s %s %s ', self.steptime[0], self.steptarget[0], self.stepcommand[0])
            del self.steptime[0]
            del self.steptarget[0]
            del self.stepcommand[0]

    def steplist(self):
        """return the list of steps to be completed"""
        index = 0
        returnval = []
        for _ in self.steptime:
            returnval.append([self.steptime[index], self.steptarget[index], self.stepcommand[index]])
            index = index + 1
        return returnval

    def steplistformatted(self):
        """Generate a formatted list of steps as a list of strings"""
        index = 0
        returnval = []
        for _ in self.steptime:
            returnval.append('%s, %s, %s' % (self.steptime[index], self.steptarget[index], self.stepcommand[index]))
            index = index + 1
        if len(returnval) == 0:
            returnval = ['1, End, End']
        return returnval

    def sample(self, cycleitem):
        """Check is an item is in the list of samples"""
        for item in self.samples:
            if cycleitem == item:
                return True
        return False


currentcycle = CycleClass()
