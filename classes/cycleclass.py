import sqlite3
from settings import settings


class CycleClass:
    def __init__(self):
        self.id = -1
        self.name = None
        self.description = None
        self.enabled = True
        self.laserpower = settings['laser']['power']
        self.cycles = []
        self.samples = []
        self.locations = []
        self.steptime = []
        self.steptarget = []
        self.stepcommand = []
        self.readdatabase()

    def readdatabase(self):
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
        if not(name in self.cycles):
            print("%s not found" % name)
            return
        elif name == 'End':
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
        for _ in self.steptime:
            returnval.append([self.steptime[index], self.steptarget[index], self.stepcommand[index]])
            index = index + 1
        return returnval

    def steplistformatted(self):
        index = 0
        returnval = []
        for _ in self.steptime:
            returnval.append('%s, %s, %s' % (self.steptime[index], self.steptarget[index], self.stepcommand[index]))
            index = index + 1
        if len(returnval) == 0:
            returnval = ['00, End, End']
        return returnval

    def sample(self, cycleitem):
        for item in self.samples:
            if cycleitem == item:
                return True
        return False


currentcycle = CycleClass()
