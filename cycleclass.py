import sqlite3
from settings import settings


class CycleClass:
    def __init__(self):
        self.id = -1
        self.name = None
        self.description = None
        self.enabled = True
        self.cycles = []
        self.locations = []
        self.steptime = []
        self.steptarget = []
        self.stepcommand = []
        self.readdatabase()

    def readdatabase(self):
        self.cycles.append('End')
        database = sqlite3.connect(settings['database']['databasepath'])
        cursorObj = database.cursor()
        sqlQuery = 'SELECT name from cycles WHERE enabled = 1'
        cursorObj.execute(sqlQuery)
        returnobjects = cursorObj.fetchall()
        for cycle in returnobjects:
            self.cycles.append(cycle[0])
        sqlQuery = 'SELECT * from locations'
        cursorObj.execute(sqlQuery)
        returnobjects = cursorObj.fetchall()
        for location in returnobjects:
            self.locations.append(location[0])
        database.close()

    def setcycle(self, name):
        if not(name in self.cycles):
            print("%s not found" % name)
            return
        elif name == 'End':
            return
        database = sqlite3.connect(settings['database']['databasepath'])
        cursorObj = database.cursor()
        sqlQuery = """SELECT * from cycles WHERE name = ?"""
        cursorObj.execute(sqlQuery, [name])
        returnobjects = cursorObj.fetchall()
        self.id = returnobjects[0][0]
        self.name = name
        self.description = returnobjects[0][2]
        self.enabled = returnobjects[0][3]
        sqlQuery = """SELECT * from cyclesteps WHERE id = ?"""
        cursorObj.execute(sqlQuery, [self.id])
        returnobjects = cursorObj.fetchall()
        self.steptime = []
        self.steptarget = []
        self.stepcommand = []
        for task in returnobjects:
            self.steptime.append(task[1])
            self.steptarget.append(task[2])
            self.stepcommand.append(task[3])

    def current(self):
        return [self.name, self.description]

    def currenttask(self, time):
        if len(self.steptime) > 0:
            if time == self.steptime[0]:
                return [self.steptime[0], self.steptarget[0], self.stepcommand[0]]
            else:
                return [time, 'No task', 'No task']
        else:
            return [1, 'End', 'End']

    def currentstep(self):
        if len(self.steptime) > 0:
            return [self.steptime[0], self.steptarget[0], self.stepcommand[0]]
        else:
            return [1, 'End', 'End']

    def completecurrent(self):
        if len(self.steptime) >= 0:
            #  print('completed %s %s %s ' % (self.steptime[0], self.steptarget[0], self.stepcommand[0]))
            del self.steptime[0]
            del self.steptarget[0]
            del self.stepcommand[0]

    def steplist(self):
        index = 0
        returnval = []
        for i in self.steptime:
            returnval.append([self.steptime[index], self.steptarget[index], self.stepcommand[index]])
            index = index + 1
        return returnval

    def steplistformatted(self):
        index = 0
        returnval = []
        for i in self.steptime:
            returnval.append('%s, %s, %s' % (self.steptime[index], self.steptarget[index], self.stepcommand[index]))
            index = index + 1
        if len(returnval) == 0:
            returnval = ['00, End, End']
        return returnval


currentcycle = CycleClass()
