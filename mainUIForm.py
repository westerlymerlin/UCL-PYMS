from PySide2.QtWidgets import *
from ui_main import Ui_MainWindow
import webbrowser
import requests
from settings import settings, writesettings, setrunning, running
import threading
from newbatchform import UiBatch
from aboutui import UiAbout
from logviewerui import UiLogViewer
from settingsviewerui import UiSettingsViewer
from xymanual import XYSetupUI
from laserclass import laser
from batchclass import batch
from cycleclass import currentcycle
from msFileclass import ms


def laserstatus(status):
    if status == 'on':
        return 1
    else:
        return 0


def valvestatus(status):
    if status == 'open':
        return 1
    else:
        return 0


class UiMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.imgLaser.setHidden(True)
        self.imgPyrometer.setHidden(True)
        self.imgQMS.setHidden(True)
        self.wValve1.setHidden(True)
        self.wValve2.setHidden(True)
        self.wValve3.setHidden(True)
        self.wValve4.setHidden(True)
        self.wValve5.setHidden(True)
        self.wValve6.setHidden(True)
        self.wValve7.setHidden(True)
        self.wValve8.setHidden(True)
        self.wValve10.setHidden(True)
        self.wValve11.setHidden(True)
        self.wValve12.setHidden(True)
        self.wValve13.setHidden(True)
        self.tableResults.setColumnWidth(0, 120)
        self.tableResults.setColumnWidth(1, 100)
        self.tableResults.setColumnWidth(2, 175)
        self.tableResults.setColumnWidth(3, 70)
        self.move(settings['mainform']['x'], settings['mainform']['y'])
        self.tbValve1.clicked.connect(lambda: self.workvalve('valve1', self.wValve1.isHidden()))
        self.tbValve2.clicked.connect(lambda: self.workvalve('valve2', self.wValve2.isHidden()))
        self.tbValve3.clicked.connect(lambda: self.workvalve('valve3', self.wValve3.isHidden()))
        self.tbValve4.clicked.connect(lambda: self.workvalve('valve4', self.wValve4.isHidden()))
        self.tbValve5.clicked.connect(lambda: self.workvalve('valve5', self.wValve5.isHidden()))
        self.tbValve6.clicked.connect(lambda: self.workvalve('valve6', self.wValve6.isHidden()))
        self.tbValve7.clicked.connect(lambda: self.workvalve('valve7', self.wValve7.isHidden()))
        self.tbValve8.clicked.connect(lambda: self.workvalve('valve8', self.wValve8.isHidden()))
        self.tbValve10.clicked.connect(lambda: self.workvalve('valve10', self.wValve10.isHidden()))
        self.tbValve11.clicked.connect(lambda: self.workvalve('valve11', self.wValve11.isHidden()))
        self.tbValve12.clicked.connect(lambda: self.workvalve('valve12', self.wValve12.isHidden()))
        self.tbValve13.clicked.connect(lambda: self.workvalve('valve13', self.wValve13.isHidden()))
        self.tbStop.clicked.connect(self.closeallvalves)
        self.tbRun.clicked.connect(self.runclick)
        self.actionExit.triggered.connect(self.closeEvent)
        self.actionStartNewBatch.triggered.connect(self.shownewbatch)
        self.actionManualControl.triggered.connect(self.showxymanual)
        self.actionXYOpenStatusPage.triggered.connect(lambda: self.oppenwebpage('XY Status'))
        self.actionXYOpenLogPage.triggered.connect(lambda: self.oppenwebpage('XY Log'))
        self.actionValveOpenStatusPage.triggered.connect(lambda: self.oppenwebpage('Valve Status'))
        self.actionValveOpenLogPage.triggered.connect(lambda: self.oppenwebpage('Valve Log'))
        self.actionPumpOpenStatusPage.triggered.connect(lambda: self.oppenwebpage('Pump Status'))
        self.actionPumpOpenLogPage.triggered.connect(lambda: self.oppenwebpage('Pump Log'))
        self.actionCO2LaserOn.triggered.connect(lambda: self.manuallaser('CO2', 'on'))
        self.actionCO2LaserOff.triggered.connect(lambda: self.manuallaser('CO2', 'off'))
        self.actionPyroLaserOn.triggered.connect(lambda: self.manuallaser('Pyro', 'on'))
        self.actionPyroLaserOff.triggered.connect(lambda: self.manuallaser('Pyro', 'off'))
        self.actionAboutPyMS.triggered.connect(self.showabout)
        self.actionViewPyMSLog.triggered.connect(self.showlogviewer)
        self.actionViewPyMSSettings.triggered.connect(self.showsettingsviewer)
        self.spinLaserPower.setValue(settings['laser']['power'])
        self.spinLaserPower.valueChanged.connect(self.setlaserpower)
        self.secondcount = 0
        self.secondincrement = 0
        self.timertick = 0
        self.xposition = 0
        self.yposition = 0
        currentcycle.setcycle(batch.current()[0])
        self.run = 0
        self.taskrunning = False
        self.valveerrors = 0
        self.xyerrors = 0
        self.pumperrors = 0
        self.lblCurrent.setText('idle')
        self.updatebatchlist()
        self.update_commandlist()
        threading.Timer(5, self.timer).start()
        self.updateresults()

    def timer(self):
        if running:
            self.secondcount = self.secondcount + self.secondincrement
            self.lcdElapsedTime.display(self.secondcount)
            timerthread = threading.Timer(1, self.timer)
            timerthread.start()
            valvereaderthread = threading.Timer(0.05, self.getvalvestatus)
            valvereaderthread.start()
            msreaderthread = threading.Timer(0.1, self.read_ms)
            msreaderthread.start()
            alarmreaderthread = threading.Timer(0.3, self.check_alarms)
            alarmreaderthread.start()
            if not self.taskrunning:
                taskrunnerthread = threading.Timer(0.2, self.timedevents)
                taskrunnerthread.start()
            if self.timertick == 0 or self.timertick == 2:
                xyreaderthread = threading.Timer(0.1, self.update_xy)
                xyreaderthread.start()
            if self.timertick == 0:
                pressurereaderthread = threading.Timer(0.5, self.update_pressures)
                pressurereaderthread.start()
                pyroreaderthread = threading.Timer(0.7, self.updatetemprature)
                pyroreaderthread.start()
            if self.timertick == 3:
                self.timertick = 0
            else:
                self.timertick += 1

    def getvalvestatus(self):
        message = {"item": 'getstatus', "command": True}
        try:
            resp = requests.post(settings['hosts']['valvehost'], json=message, timeout=1)
            self.valveerrors = 0
            self.setvalves(resp.json())
        except requests.RequestException:
            self.valveerrors += 1
            print('mainUIForm: Get Status Valve Controller Timeout Error')

    def read_ms(self):
        ms.filereader()
        labletext = ms.check_quad_is_online()
        if labletext != 'Off Line':
            self.imgQMS.setHidden(False)
        else:
            self.imgQMS.setHidden(True)
        self.lblMS.setText(labletext)

    def check_alarms(self):
        status = ''
        if ms.alarm:
            if ms.check_quad_is_online() == 'Off Line':
                status = status + 'Quad Reader if offline, system is paused\n'
                self.secondincrement = 0
                self.run = 0
                self.tbRun.setChecked(False)
        if self.valveerrors > 10:
            status = status + 'Valve controller is offline, system is paused\n'
            self.secondincrement = 0
            self.run = 0
            self.tbRun.setChecked(False)
        if self.xyerrors > 10:
            status = status + 'X-Y controller is offline, system is paused\n'
            self.secondincrement = 0
            self.run = 0
            self.tbRun.setChecked(False)
        if self.pumperrors > 10:
            status = status + 'Pump reader is offline, system is paused\n'
            self.secondincrement = 0
            self.run = 0
            self.tbRun.setChecked(False)
        if settings['vacuum']['ion']['current'] > settings['vacuum']['ion']['high']:
            status = status + 'Ion Pump is showing high pressure, system is paused\n'
            self.secondincrement = 0
            self.run = 0
            self.tbRun.setChecked(False)
        if settings['vacuum']['turbo']['current'] > settings['vacuum']['turbo']['high']:
            status = status + 'Turbo Pump is showing loss of vacuum, system is paused\n'
            self.secondincrement = 0
            self.run = 0
            self.tbRun.setChecked(False)
        if self.lblAalarm.text() != status:
            self.lblAalarm.setText(status)

    def setvalves(self, resp):
        if self.wValve1.isVisible() != valvestatus(resp[0]['status']):
            print("Valve 1 changed")
            self.wValve1.setVisible(valvestatus(resp[0]['status']))
        if self.wValve2.isVisible() != valvestatus(resp[1]['status']):
            print("Valve 2 changed")
            self.wValve2.setVisible(valvestatus(resp[1]['status']))
        if self.wValve3.isVisible() != valvestatus(resp[2]['status']):
            print("Valve 3 changed")
            self.wValve3.setVisible(valvestatus(resp[2]['status']))
        if self.wValve4.isVisible() != valvestatus(resp[3]['status']):
            print("Valve 4 changed")
            self.wValve4.setVisible(valvestatus(resp[3]['status']))
        if self.wValve5.isVisible() != valvestatus(resp[4]['status']):
            print("Valve 5 changed")
            self.wValve5.setVisible(valvestatus(resp[4]['status']))
        if self.wValve6.isVisible() != valvestatus(resp[5]['status']):
            print("Valve 6 changed")
            self.wValve6.setVisible(valvestatus(resp[5]['status']))
        if self.wValve7.isVisible() != valvestatus(resp[6]['status']):
            print("Valve 7 changed")
            self.wValve7.setVisible(valvestatus(resp[6]['status']))
        if self.wValve8.isVisible() != valvestatus(resp[7]['status']):
            print("Valve 8 changed")
            self.wValve8.setVisible(valvestatus(resp[7]['status']))
        if self.wValve10.isVisible() != valvestatus(resp[8]['status']):
            print("Valve 10 changed")
            self.wValve10.setVisible(valvestatus(resp[8]['status']))
        if self.wValve11.isVisible() != valvestatus(resp[9]['status']):
            print("Valve 11 changed")
            self.wValve11.setVisible(valvestatus(resp[9]['status']))
        if self.wValve12.isVisible() != valvestatus(resp[10]['status']):
            print("Valve 12 changed")
            self.wValve12.setVisible(valvestatus(resp[10]['status']))
        if self.wValve13.isVisible() != valvestatus(resp[11]['status']):
            print("Valve 13 changed")
            self.wValve13.setVisible(valvestatus(resp[11]['status']))
        if self.imgLaser.isVisible() != laserstatus(resp[12]['status']):
            print("Laser status changed")
            self.imgLaser.setVisible(laserstatus(resp[12]['status']))

    def setlaserpower(self):
        settings['laser']['power'] = self.spinLaserPower.value()

    def workvalve(self, valve, state):
        if state:
            command = 'open'
        else:
            command = 'close'
        message = {"item": valve, "command": command}
        try:
            requests.post(settings['hosts']['valvehost'], json=message, timeout=1)
            self.valveerrors = 0
        except requests.RequestException:
            print('mainUIForm: Manual Valve Controller Timeout Error')
            self.valveerrors += 5

    def valvecommand(self, valve, command):
        message = {"item": valve, "command": command}
        try:
            requests.post(settings['hosts']['valvehost'], json=message, timeout=2)
            self.valveerrors = 0
        except requests.RequestException:
            print('mainUIForm: Automated Valve Controller at second %s Timeout Error' % self.secondcount)
            self.valveerrors += 5

    def closeallvalves(self):
        self.secondincrement = 0
        self.secondcount = 0
        self.run = 0
        message = {"item": 'closeallvalves', "command": True}
        try:
            requests.post(settings['hosts']['valvehost'], json=message, timeout=1)
            self.valveerrors = 0
        except requests.RequestException:
            print('mainUIForm: Close all Valve Controller Timeout Error')
            self.valveerrors += 11
        message = {"item": 'xmove', "command": 0}
        try:
            requests.post(settings['hosts']['xyhost'], json=message, timeout=1)
            self.xyerrors = 0
        except requests.RequestException:
            print('mainUIForm: xy Stop X Timeout Error')
            self.xyerrors += 10
        message = {"item": 'ymove', "command": 0}
        try:
            requests.post(settings['hosts']['xyhost'], json=message, timeout=1)
            self.xyerrors = 0
        except requests.RequestException:
            print('mainUIForm: Stop Y Controller Timeout Error')
            self.xyerrors += 10

        batch.changed = 1
        self.tbRun.setChecked(0)
        # sleep(0.5)
        self.tbStop.setChecked(0)
        self.runstate()

    def runclick(self):
        if self.tbRun.isChecked():
            print('mainUIForm: Run pressed')
            self.run = 2
            self.xyerrors = 0
            self.valveerrors = 0
        else:
            print('mainUIForm: Pause pressed, will halt after this cycle ends')
            self.run = 1
        self.runstate()

    def runstate(self):
        try:
            if self.run > 0:
                self.frmHeLine.setEnabled(False)
                self.lblStatus.setText('Status: Automated Control Enabled')
                self.secondincrement = 1
            else:
                self.frmHeLine.setEnabled(True)
                self.lblStatus.setText('Status: Manual Control')
                self.secondincrement = 0
                laser.off()
        except:
            print('mainUIForm: Runstate error')

    def closeEvent(self, event):
        print('mainUIForm: Main Form close event triggered')
        settings['mainform']['x'] = self.x()
        settings['mainform']['y'] = self.y()
        writesettings()
        setrunning(False)
        self.deleteLater()

    def timedevents(self):
        try:
            if self.run > 0:
                self.runevents()
            if batch.changed == 1:
                batch.changed = 0
                currentcycle.setcycle(batch.current()[0])
                self.updatebatchlist()
                self.update_commandlist()
                self.updateresults()
        except ValueError:
            print('t=%s mainUIForm: timedevents value error %s' % (self.secondcount, Exception()))
        except TypeError:
            print('t=%s mainUIForm: timedevents type error %s' % (self.secondcount, Exception()))

    def runevents(self):
        try:
            if self.valveerrors > 10 or self.xyerrors > 10:
                self.secondincrement = 0
                self.run = 0
                self.tbRun.setChecked(False)
                print("mainUIForm: Paused because of comms error")
                self.lblCurrent.setText('Paused because of comms errors. Please Check Log')
                return
            self.taskrunning = True
            current = currentcycle.currentstep()
            if self.secondcount >= current[0]:
                self.lblCurrent.setText('%s, %s' % (current[1], current[2]))
                if current[1][0:5] == 'valve' or current[1][0:7] == 'pipette':
                    self.valvecommand(current[1], current[2])
                    currentcycle.completecurrent()
                    self.listCommands.takeItem(0)
                elif current[1] == 'End':
                    if not (batch.isitthereyet(self.xposition, self.yposition)):
                        print('%s not there yet x=%s, y=%s' % (self.secondcount, self.xposition, self.yposition))
                        self.lblCurrent.setText('Waiting for X-Y Stage to position')
                        self.taskrunning = False
                        return
                    self.secondincrement = 0
                    print('mainUIForm: End detected')
                    self.lblCurrent.setText('idle')
                    currentrunstate = self.run
                    self.run = 0
                    print("mainUIForm: starting complete current")
                    batch.completecurrent()
                    print("mainUIForm: Setting cycle to next")
                    currentcycle.setcycle(batch.current()[0])
                    print('mainUIForm: New Cycle loaded')
                    self.secondcount = 0
                    print('mainUIForm: Update lists')
                    self.updatebatchlist()
                    self.update_commandlist()
                    self.updateresults()
                    self.secondincrement = 1
                    if batch.current()[0] != 'End':
                        if currentrunstate == 1:
                            self.run = 0
                            self.runstate()
                        else:
                            self.run = currentrunstate
                    else:
                        self.secondincrement = 0
                        self.secondcount = 0
                        self.run = 0
                        self.tbRun.setChecked(False)
                        self.runstate()
                elif current[1][0:5] == 'laser':
                    if current[2] == 'on':
                        laser.on()
                    elif current[2] == 'setpower':
                        laser.setpower()
                    else:
                        laser.off()
                    currentcycle.completecurrent()
                    self.listCommands.takeItem(0)
                elif current[1][0:7] == 'xytable':
                    self.movenext()
                    currentcycle.completecurrent()
                    self.listCommands.takeItem(0)
                elif current[1] == 'quad':
                    if current[2] == 'starttimer':
                        print('t=%s mainUIForm: start timer' % self.secondcount)
                        ms.starttimer(batch.currentcycle(), batch.formatsample(), batch.currentdescription(), batch.id,
                                      batch.runnumber[0])
                        currentcycle.completecurrent()
                        self.listCommands.takeItem(0)
                    elif current[2] == 'starttimer2':
                        print('t=%s mainUIForm: start timer for reheat' % self.secondcount)
                        ms.starttimer(batch.currentcycle(), batch.formatsample() + '_RE', batch.currentdescription(),
                                      batch.id, batch.runnumber[0])
                        currentcycle.completecurrent()
                        self.listCommands.takeItem(0)
                    elif current[2] == 'read':
                        print('t=%s mainUIForm: read quad' % self.secondcount)
                        ms.read()
                        currentcycle.completecurrent()
                        self.listCommands.takeItem(0)
                    elif current[2] == 'writefile':
                        print('t=%s mainUIForm: write out file' % self.secondcount)
                        ms.writefile()
                        currentcycle.completecurrent()
                        self.listCommands.takeItem(0)
                elif current[1] == 'image':
                    print('t=%s mainUIForm: take image %s' % (self.secondcount, current[2]))
                    batch.image(current[2])
                    currentcycle.completecurrent()
                    self.listCommands.takeItem(0)
                else:
                    currentcycle.completecurrent()
                    self.listCommands.takeItem(0)
            self.taskrunning = False
        except:
            self.taskrunning = False
            print('mainUIForm: runevents error %s' % Exception)

    def shownewbatch(self):
        self.newdialog = UiBatch()
        self.newdialog.setModal(True)
        self.newdialog.openbatcheck()
        self.newdialog.show()

    def showabout(self):
        self.aboutdialog = UiAbout()
        self.aboutdialog.show()

    def showlogviewer(self):
        self.logviewerdialog = UiLogViewer()
        self.logviewerdialog.loadlog()
        self.logviewerdialog.show()

    def showsettingsviewer(self):
        self.setingviewerdialog = UiSettingsViewer()
        self.setingviewerdialog.loadfile()
        self.setingviewerdialog.show()

    def showxymanual(self):
        self.newdialog = XYSetupUI()
        self.newdialog.setModal(True)
        self.newdialog.show()

    def updatebatchlist(self):
        try:
            print('mainUIForm: Update Batch List')
            self.listBatch.clear()
            self.listBatch.addItems(batch.listformatted())
            text = batch.formatdescription()
            self.linePlanchet.setText(text)
            text = batch.formatsample()
            self.lineLocation.setText(text)
            batch.changed = 0
        except:
            print('mainUIForm: batchlist error')

    def update_commandlist(self):
        try:
            print('mainUIForm: Update command list')
            self.listCommands.clear()
            self.listCommands.addItems(currentcycle.steplistformatted())
        except:
            print('mainUIForm: command list error')

    def update_pressures(self):
        message = {"item": 'getpressures', "command": True}
        try:
            resp = requests.post(settings['hosts']['pumphost'], json=message, timeout=1)
            settings['vacuum']['turbo']['current'] = float(resp.json()[0]['pressure'])
            settings['vacuum']['tank']['current'] = float(resp.json()[1]['pressure'])
            settings['vacuum']['ion']['current'] = float(resp.json()[2]['pressure'])
            self.lineIonPump.setText('%.2e' % settings['vacuum']['ion']['current'])
            self.lineTurboPump.setText('%.2e' % settings['vacuum']['turbo']['current'])
            self.lineScrollPump.setText('%.2e' % settings['vacuum']['tank']['current'])
            self.pumperrors = 0
        except requests.RequestException:
            self.pumperrors += 1
            print('mainUIForm: Get Pressures Pump Raeder Timeout Error')

    def updatetemprature(self):
        message = {"item": 'gettemperature', "command": True}
        try:
            resp = requests.post(settings['hosts']['pumphost'], json=message, timeout=1)
            settings['pyrometer']['current'] = float(resp.json()['temperature'])
            self.linePyrometer.setText('%s' % settings['pyrometer']['current'])
            self.imgPyrometer.setHidden(not(resp.json()['laser']))
            self.pumperrors = 0
        except requests.RequestException:
            self.pumperrors += 1
            print('mainUIForm: Get Temperature Pump Raeder Timeout Error')

    def update_xy(self):
        try:
            message = {"item": 'getxystatus', "command": True}
            resp = requests.post(settings['hosts']['xyhost'], json=message, timeout=1)
            self.xposition = resp.json()['xpos']
            self.yposition = resp.json()['ypos']
            self.lineXPosition.setText('%.3f' % self.xposition)
            self.lineYPosition.setText('%.3f' % self.yposition)
            self.xyerrors = 0
        except requests.RequestException:
            print('mainUIForm: Get Status X-Y Controller Timeout Error')
            self.xyerrors += 1

    def updateresults(self):
        try:
            print('Update results')
            self.tableResults.setRowCount(0)
            print('Results table cleared')
            results = batch.results()
            for row in results:
                x = self.tableResults.rowCount()
                self.tableResults.insertRow(x)
                newtime_item = QTableWidgetItem(row[2][:16])
                newfile_item = QTableWidgetItem(row[0])
                newdescription_item = QTableWidgetItem(row[1])
                newresults_item = QTableWidgetItem('%.3f' % row[3])
                self.tableResults.setItem(x, 0, newtime_item)
                self.tableResults.setItem(x, 1, newfile_item)
                self.tableResults.setItem(x, 2, newdescription_item)
                self.tableResults.setItem(x, 3, newresults_item)
            print('mainUIForm: Results Table Updated')
        except:
            print('mainUIForm: Update results error - %s' % Exception)

    def oppenwebpage(self, page):
        if page == 'Valve Status':
            url = settings['hosts']['valvehost'][:-4]
            webbrowser.open(url)
        elif page == 'Valve Log':
            url = settings['hosts']['valvehost'][:-3] + 'pylog'
            webbrowser.open(url)
        elif page == 'XY Status':
            url = settings['hosts']['xyhost'][:-4]
            webbrowser.open(url)
        elif page == 'XY Log':
            url = settings['hosts']['xyhost'][:-3] + 'pylog'
            webbrowser.open(url)
        elif page == 'Pump Status':
            url = settings['hosts']['pumphost'][:-4]
            webbrowser.open(url)
        elif page == 'Pump Log':
            url = settings['hosts']['pumphost'][:-3] + 'pylog'
            webbrowser.open(url)

    def movenext(self):
        print('%s Move to %s' % (self.secondcount, batch.nextlocation()))
        movexthread = threading.Timer(0.5, self.movex)
        movexthread.start()
        moveythread = threading.Timer(1.5, self.movey)
        moveythread.start()

    def movex(self):
        location = batch.locxy(batch.nextlocation())
        try:
            messagex = {"item": 'xmoveto', "command": location[0]}
            requests.post(settings['hosts']['xyhost'], json=messagex, timeout=1)
            self.xyerrors = 0
        except requests.RequestException:
            print('mainUIForm: Move XY Controller Timeout Error')
            self.xyerrors += 5

    def movey(self):
        location = batch.locxy(batch.nextlocation())
        try:
            messagey = {"item": 'ymoveto', "command": location[1]}
            requests.post(settings['hosts']['xyhost'], json=messagey, timeout=1)
            self.xyerrors = 0
        except requests.RequestException:
            print('mainUIForm: Move XY Controller Timeout Error')
            self.xyerrors += 5

    def manuallaser(self, lasertype, state):
        print("mainUIForm: Manual Laser Control: Laser %s is set to %s" % (lasertype, state))
        if lasertype == 'CO2':
            laserhost = settings['hosts']['valvehost']
            laser.setpower()
        else:
            laserhost = settings['hosts']['pumphost']
        try:
            message = {"item": 'laser', "command": state}
            if self.run < 1:
                requests.post(laserhost, json=message, timeout=1)
        except requests.RequestException:
            print('mainUIForm: Laser Manual Control Timeout Error')
