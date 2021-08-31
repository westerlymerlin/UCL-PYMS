from PySide2.QtWidgets import *
from ui_xymanualcontrol import Ui_dialogXYSetup
from settings import settings
import threading
import sqlite3
import requests
from cycleclass import currentcycle
from batchclass import batch
from time import sleep
import sys

class XYSetupUI(QDialog, Ui_dialogXYSetup):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(settings['xymanualform']['x'], settings['xymanualform']['y'])
        self.comboLocation1.addItems(currentcycle.locations)
        self.btnClose.clicked.connect(self.formclose)
        self.btnGoto.clicked.connect(self.gotopress)
        self.btnStop.clicked.connect(self.stopall)
        self.btnSave.clicked.connect(self.savelocation)
        self.btnUp.clicked.connect(lambda: self.movepress(['y', 1]))
        self.btnDown.clicked.connect(lambda: self.movepress(['y', -1]))
        self.btnRight.clicked.connect(lambda: self.movepress(['x', 1]))
        self.btnLeft.clicked.connect(lambda: self.movepress(['x', -1]))
        self.xposition = 0
        self.yposition = 0
        self.running = 1
        threading.Timer(1, self.timer).start()

    def formclose(self):
        self.running = 0
        settings['xymanualform']['x'] = self.x()
        settings['xymanualform']['y'] = self.y()
        self.deleteLater()

    def timer(self):
        if self.running:
            timerthread = threading.Timer(1, self.timer)
            timerthread.start()
            xyreaderthread = threading.Timer(0.05, self.updateXY)
            xyreaderthread.start()

    def updateXY(self):
        try:
            message = {"item": 'getxystatus', "command": True}
            resp = requests.post(settings['hosts']['xyhost'], json=message, timeout=1)
            self.xposition = resp.json()['xpos']
            self.yposition = resp.json()['ypos']
            self.lineXPosition.setText('%.3f' % self.xposition)
            self.lineYPosition.setText('%.3f' % self.yposition)
        except requests.RequestException:
            print('Status Valve Controller Timeout Error')

    def gotopress(self):
        goloc = batch.locxy(self.comboLocation1.currentText())
        try:
            messagex = {"item": 'xmoveto', "command": goloc[0]}
            requests.post(settings['hosts']['xyhost'], json=messagex, timeout=1)
            sleep(.5)
            messagey = {"item": 'ymoveto', "command": goloc[1]}
            requests.post(settings['hosts']['xyhost'], json=messagey, timeout=1)
        except requests.RequestException:
            print('Status Valve Controller Timeout Error')

    def movepress(self, dir):
        if dir[0] == 'x':
            messagee = {"item": 'xmove', "command": dir[1]}
        else:
            messagee = {"item": 'ymove', "command": dir[1]}
        try:
            requests.post(settings['hosts']['xyhost'], json=messagee, timeout=1)
        except requests.RequestException:
            print('Status Valve Controller Timeout Error')

    def stopall(self):
        message = {"item": 'xmove', "command": 0}
        try:
            requests.post(settings['hosts']['xyhost'], json=message, timeout=1)
        except requests.RequestException:
            print('Stop X Timeout Error')
        message = {"item": 'ymove', "command": 0}
        try:
            requests.post(settings['hosts']['xyhost'], json=message, timeout=1)
        except requests.RequestException:
            print('Stop Y Controller Timeout Error')

    def savelocation(self):
        database = sqlite3.connect(settings['database']['databasepath'])
        cursorObj = database.cursor()
        sql_update_query = """ UPDATE locations SET x = ?, y = ? WHERE location = ?  """
        datarow = (round(self.xposition,3), round(self.yposition,3), self.comboLocation1.currentText())
        cursorObj.execute(sql_update_query, datarow)
        database.commit()
        database.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = XYSetupUI()
    dialog.show()
    sys.exit(app.exec_())
