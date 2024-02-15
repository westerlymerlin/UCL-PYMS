"""
Main Helium line form - graphical outut of the Heliumline state and timers for running samples
Author: Gary Twinn
"""

import threading
import webbrowser
from tkinter import messagebox
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from settings import settings, writesettings, setrunning, running, alarms, VERSION
from host_queries import valvegetstatus, lasergetstatus, lasergetalarm, pressuresread, xyread, tempratureread
from host_commands import lasercommand, lasersetpower, valvechange, xymoveto, xymove, pyrolasercommand, rpi_reboot
from classes.batchclass import batch
from classes.cycleclass import currentcycle
from classes.ms_hiden_class import ms
from alertmessage import alert
from logmanager import logger
from ui.ui_layout_main import Ui_MainWindow
from ui.new_batch_form import UiBatch
from ui.about_form import UiAbout
from ui.log_viewer_form import UiLogViewer
from ui.settings_viewer_form import UiSettingsViewer
from ui.manual_xy_form import ManualXyForm
from ui.laser_manual_form import LaserFormUI
from ui.ncc_calc_form import NccCalcUI


def valvestatus(status):
    """convertor for valve status messages from valve controller"""
    if status == 'open':
        return 1
    return 0


class UiMain(QMainWindow, Ui_MainWindow):
    """Qt Class for main window"""
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('PyMS - Python Mass Spectrometry v%s' % VERSION)
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
        self.imgSRS.setHidden(settings['MassSpec']['srs-rga-hide'])
        self.move(settings['mainform']['x'], settings['mainform']['y'])
        self.tbValve1.clicked.connect(lambda: valvechange('valve1', self.wValve1.isHidden()))
        self.tbValve2.clicked.connect(lambda: valvechange('valve2', self.wValve2.isHidden()))
        self.tbValve3.clicked.connect(lambda: valvechange('valve3', self.wValve3.isHidden()))
        self.tbValve4.clicked.connect(lambda: valvechange('valve4', self.wValve4.isHidden()))
        self.tbValve5.clicked.connect(lambda: valvechange('valve5', self.wValve5.isHidden()))
        self.tbValve6.clicked.connect(lambda: valvechange('valve6', self.wValve6.isHidden()))
        self.tbValve7.clicked.connect(lambda: valvechange('valve7', self.wValve7.isHidden()))
        self.tbValve8.clicked.connect(lambda: valvechange('valve8', self.wValve8.isHidden()))
        self.tbValve10.clicked.connect(lambda: valvechange('valve10', self.wValve10.isHidden()))
        self.tbValve11.clicked.connect(lambda: valvechange('valve11', self.wValve11.isHidden()))
        self.tbValve12.clicked.connect(lambda: valvechange('valve12', self.wValve12.isHidden()))
        self.tbValve13.clicked.connect(lambda: valvechange('valve13', self.wValve13.isHidden()))
        self.tbStop.clicked.connect(self.emergency_stop)
        self.tbRun.clicked.connect(self.run_click)
        self.actionExit.triggered.connect(self.closeEvent)
        self.actionStartNewBatch.triggered.connect(self.menu_show_new_batch)
        self.actionManualControl.triggered.connect(self.menu_show_xymanual)
        self.actionXYOpenStatusPage.triggered.connect(lambda: menu_open_web_page('XY Status'))
        self.actionXYOpenLogPage.triggered.connect(lambda: menu_open_web_page('XY Log'))
        self.actionReboot_XY.triggered.connect(lambda: restart_pi('xyhost'))
        self.actionValveOpenStatusPage.triggered.connect(lambda: menu_open_web_page('Valve Status'))
        self.actionValveOpenLogPage.triggered.connect(lambda: menu_open_web_page('Valve Log'))
        self.actionReboot_Valve.triggered.connect(lambda: restart_pi('valvehost'))
        self.actionPumpOpenStatusPage.triggered.connect(lambda: menu_open_web_page('Pump Status'))
        self.actionPumpOpenLogPage.triggered.connect(lambda: menu_open_web_page('Pump Log'))
        self.actionReboot_Pump.triggered.connect(lambda: restart_pi('pumphost'))
        self.actionLaserOpenStatusPage.triggered.connect(lambda: menu_open_web_page('Laser Status'))
        self.actionLaserOpenLogPage.triggered.connect(lambda: menu_open_web_page('Laser Log'))
        self.actionReboot_Laser.triggered.connect(lambda: restart_pi('laserhost'))
        self.actionCO2LaserOn.triggered.connect(self.menu_show_lasermanual)
        self.actionPyroLaserOn.triggered.connect(lambda: manual_laser('on'))
        self.actionPyroLaserOff.triggered.connect(lambda: manual_laser('off'))
        self.actionAboutPyMS.triggered.connect(self.menu_show_about)
        self.actionViewPyMSLog.triggered.connect(self.menu_show_log_viewer)
        self.actionViewPyMSSettings.triggered.connect(self.menu_show_settings_viewer)
        self.actionStartMIDScan.triggered.connect(ms.start_mid)
        self.actionStartProfileScan.triggered.connect(ms.start_profile)
        self.actionStopScan.triggered.connect(ms.stop_runnning)
        self.actionNCCViewer.triggered.connect(self.menu_show_ncc)
        self.btnHidenMID.clicked.connect(ms.start_mid)
        self.btnHidenProfile.clicked.connect(ms.start_profile)
        self.btnHidenStop.clicked.connect(ms.stop_runnning)
        self.btnNCCViewer.clicked.connect(self.menu_show_ncc)
        font1 = QFont()
        font1.setFamilies(['Segoe UI'])
        font1.setPointSize(10)
        font1.setBold(True)
        self.tableResults.setColumnWidth(0, 120)
        self.tableResults.setColumnWidth(1, 100)
        self.tableResults.setColumnWidth(2, 175)
        self.tableResults.setColumnWidth(3, 83)
        newitem0 = QTableWidgetItem('Date')
        newitem0.setTextAlignment(Qt.AlignLeading | Qt.AlignVCenter)
        newitem0.setFont(font1)
        newitem1 = QTableWidgetItem('Data File')
        newitem1.setTextAlignment(Qt.AlignLeading | Qt.AlignVCenter)
        newitem1.setFont(font1)
        newitem2 = QTableWidgetItem('Sample Description')
        newitem2.setTextAlignment(Qt.AlignLeading | Qt.AlignVCenter)
        newitem2.setFont(font1)
        newitem3 = QTableWidgetItem('Best Fit')
        newitem3.setTextAlignment(Qt.AlignLeading | Qt.AlignVCenter)
        newitem3.setFont(font1)
        self.tableResults.setHorizontalHeaderItem(0, newitem0)
        self.tableResults.setHorizontalHeaderItem(1, newitem1)
        self.tableResults.setHorizontalHeaderItem(2, newitem2)
        self.tableResults.setHorizontalHeaderItem(3, newitem3)
        self.secondcount = 0
        self.secondincrement = 0
        self.timertick = 0
        self.xposition = 0
        self.yposition = 0
        self.xyerrors = 0
        self.valveerrors = 0
        self.newdialog = None   # used for modal dialogs
        currentcycle.setcycle(batch.current()[0])
        self.run = 0
        self.taskrunning = False
        self.turbopumphigh = 0
        self.ionpumphigh = 0
        self.lblCurrent.setText('idle')
        self.update_ui_batch_list()
        self.update_ui_commandlist()
        threading.Timer(5, self.global_timer).start()
        self.update_ui_results_table()

    def global_timer(self):
        """Timer thread for updating displays, runs every second"""
        if running:
            self.secondcount = self.secondcount + self.secondincrement
            self.lcdElapsedTime.display(self.secondcount)
            timerthread = threading.Timer(1, self.global_timer)
            timerthread.start()
            valvereaderthread = threading.Timer(0.05, self.update_ui_display_items)
            valvereaderthread.start()
            msreaderthread = threading.Timer(0.1, self.read_ms)
            msreaderthread.start()
            alarmreaderthread = threading.Timer(0.3, self.check_alarms)
            alarmreaderthread.start()
            if not self.taskrunning:
                taskrunnerthread = threading.Timer(0.2, self.event_timer)
                taskrunnerthread.start()
            if self.timertick == 0 or self.timertick == 2:
                xyreaderthread = threading.Timer(0.1, self.update_ui_xy_positions)
                xyreaderthread.start()
            if self.timertick == 0:
                pressurereaderthread = threading.Timer(0.5, self.update_ui_pressures)
                pressurereaderthread.start()
                pyroreaderthread = threading.Timer(0.7, self.update_ui_temprature)
                pyroreaderthread.start()
            if self.timertick == 3:
                self.timertick = 0
            else:
                self.timertick += 1

    def read_ms(self):
        """Update the Hiden Mass Spectrometer widget with its status"""
        labletext = ms.check_quad_is_online()
        if labletext != 'Off Line':
            self.imgQMS.setHidden(False)
        else:
            self.imgQMS.setHidden(True)
        self.lblMS.setText(labletext)

    def check_alarms(self):
        """Test for alarms"""
        status = ''
        if ms.timeoutcounter > ms.timeoutretries:
            if ms.check_quad_is_online() == 'Off Line':
                status = status + 'The Hiden Quad Reader is showing as offline.\nIt might ' \
                                      'be that the MAS10 application has stopped responding and needs a restart or ' \
                                  'the Hiden Control unit has been switched off, the system is paused. \n '
                self.secondincrement = 0
                self.run = 0
                self.tbRun.setChecked(False)
        if alarms['laseralarm'] != 133:
            logger.error('%s laser alarm firing', alarms['laseralarm'])
            status = status + ('The laser is not ready, please ensure that the laser is powered on, the key is in '
                               'position 2 and the enable button has been pressed. This error can also follow a '
                               'power fail\n')
            alarms['laseralarm'] = lasergetalarm()['status']
            self.secondincrement = 0
            self.run = 0
            self.tbRun.setChecked(False)
        if alarms['valvehost'] > 10:
            status = status + 'Valve controller is offline, the system is paused. \n'
            self.secondincrement = 0
            self.run = 0
            self.tbRun.setChecked(False)
        if alarms['xyhost'] > 10:
            status = status + 'X-Y controller is offline, the system is paused. \n'
            self.secondincrement = 0
            self.run = 0
            self.tbRun.setChecked(False)
        if alarms['pumphost'] > 10:
            status = status + 'Pump reader is offline, the system is paused. \n'
            self.secondincrement = 0
            self.run = 0
            self.tbRun.setChecked(False)
        if alarms['laserhost'] > 100:
            status = status + 'Laser controller is offline, the system is paused. \n'
            self.secondincrement = 0
            self.run = 0
            self.tbRun.setChecked(False)
        if settings['vacuum']['ion']['current'] == 0:
            status = status + 'Ion pump is offline, the system is paused. \n'
            self.secondincrement = 0
            self.run = 0
            self.tbRun.setChecked(False)
        if settings['vacuum']['ion']['current'] > settings['vacuum']['ion']['high']:
            self.ionpumphigh += 1
            if self.ionpumphigh > 29:
                status = status + 'Ion pump is showing loss of vacuum, the system is paused. \n'
                self.secondincrement = 0
                self.run = 0
                self.tbRun.setChecked(False)
        else:
            self.ionpumphigh = 0
        if settings['vacuum']['turbo']['current'] > settings['vacuum']['turbo']['high']:
            self.turbopumphigh += 1
            if self.turbopumphigh > 29:
                status = status + 'Turbo gauge is showing loss of vacuum, the system is paused. \n' \
                                  'This is norrmal during a planchet load \n'
                self.secondincrement = 0
                self.run = 0
                self.tbRun.setChecked(False)
        else:
            self.turbopumphigh = 0
        if settings['vacuum']['turbo']['current'] == 0:
            status = status + 'Turbo gauge is offline, the system is paused. \n'
            self.secondincrement = 0
            self.run = 0
            self.tbRun.setChecked(False)
        if self.lblAalarm.text() != status:
            self.lblAalarm.setText(status)
            self.lblFinishTime.setText('')
            if status != '':
                alert(status)
                logger.error('Main form major alarm: %s', status)

    def update_ui_display_items(self):
        """Update the valve and laser widgets on the display"""
        status = valvegetstatus()
        if status[0]['status'] != 'timeout':
            if self.wValve1.isVisible() != valvestatus(status[0]['status']):
                logger.debug('t=%s mainUIForm: Valve 1 changed', self.secondcount)
                self.wValve1.setVisible(valvestatus(status[0]['status']))
            if self.wValve2.isVisible() != valvestatus(status[1]['status']):
                logger.debug('t=%s mainUIForm: Valve 2 changed', self.secondcount)
                self.wValve2.setVisible(valvestatus(status[1]['status']))
            if self.wValve3.isVisible() != valvestatus(status[2]['status']):
                logger.debug('t=%s mainUIForm: Valve 3 changed', self.secondcount)
                self.wValve3.setVisible(valvestatus(status[2]['status']))
            if self.wValve4.isVisible() != valvestatus(status[3]['status']):
                logger.debug('t=%s mainUIForm: Valve 4 changed', self.secondcount)
                self.wValve4.setVisible(valvestatus(status[3]['status']))
            if self.wValve5.isVisible() != valvestatus(status[4]['status']):
                logger.debug('t=%s mainUIForm: Valve 5 changed', self.secondcount)
                self.wValve5.setVisible(valvestatus(status[4]['status']))
            if self.wValve6.isVisible() != valvestatus(status[5]['status']):
                logger.debug('t=%s mainUIForm: Valve 6 changed', self.secondcount)
                self.wValve6.setVisible(valvestatus(status[5]['status']))
            if self.wValve7.isVisible() != valvestatus(status[6]['status']):
                logger.debug('t=%s mainUIForm: Valve 7 changed', self.secondcount)
                self.wValve7.setVisible(valvestatus(status[6]['status']))
            if self.wValve8.isVisible() != valvestatus(status[7]['status']):
                logger.debug('t=%s mainUIForm: Valve 8 changed', self.secondcount)
                self.wValve8.setVisible(valvestatus(status[7]['status']))
            if self.wValve10.isVisible() != valvestatus(status[8]['status']):
                logger.debug('t=%s mainUIForm: Valve 10 changed', self.secondcount)
                self.wValve10.setVisible(valvestatus(status[8]['status']))
            if self.wValve11.isVisible() != valvestatus(status[9]['status']):
                logger.debug('t=%s mainUIForm: Valve 11 changed', self.secondcount)
                self.wValve11.setVisible(valvestatus(status[9]['status']))
            if self.wValve12.isVisible() != valvestatus(status[10]['status']):
                logger.debug('t=%s mainUIForm: Valve 12 changed', self.secondcount)
                self.wValve12.setVisible(valvestatus(status[10]['status']))
            if self.wValve13.isVisible() != valvestatus(status[11]['status']):
                logger.debug('t=%s mainUIForm: Valve 13 changed', self.secondcount)
                self.wValve13.setVisible(valvestatus(status[11]['status']))
        self.lblLaserPower.setText('%.1f' % settings['laser']['power'])
        status = lasergetstatus()
        if status['laser'] != 'timeout':
            if self.imgLaser.isVisible() != status['laser']:
                logger.debug('t=%s mainUIForm: Laser Status changed', self.secondcount)
                self.imgLaser.setVisible(status['laser'])

    def emergency_stop(self):
        """Emergency stop event triggered"""
        logger.warning('Main form: Emergency stop triggred')
        self.secondincrement = 0
        self.secondcount = 0
        self.run = 0
        valvechange('closeallvalves', True)
        lasercommand('off')
        xymove('x', 0)
        xymove('y', 0)
        batch.changed = 1
        self.tbRun.setChecked(0)
        self.tbStop.setChecked(0)
        self.runstate()

    def run_click(self):
        """Run button event handler"""
        if self.tbRun.isChecked():
            logger.info('t=%s mainUIForm: Run pressed', self.secondcount)
            self.run = 2
            self.xyerrors = 0
            self.valveerrors = 0
            self.lblFinishTime.setText(batch.finishtime())
            self.taskrunning = False
        else:
            logger.warning('t=%s mainUIForm: Pause pressed, will halt after this cycle ends', self.secondcount)
            self.run = 1
            self.lblFinishTime.setText('')
        self.runstate()

    def runstate(self):
        """Events dependent on run state"""
        try:
            if self.run > 0:
                self.frmHeLine.setEnabled(False)
                self.lblStatus.setText('Status: Automated Control Enabled')
                self.actionCO2LaserOn.setEnabled(False)
                self.secondincrement = 1
            else:
                self.frmHeLine.setEnabled(True)
                self.actionCO2LaserOn.setEnabled(True)
                self.lblFinishTime.setText('')
                self.lblStatus.setText('Status: Manual Control')
                self.secondincrement = 0
                lasercommand('off')
        except:
            logger.error('t=%s mainUIForm: Runstate error', self.secondcount)

    def closeEvent(self, event):
        """Application close handler"""
        logger.debug('mainUIForm: Main Form close event triggered')
        settings['mainform']['x'] = self.x()
        settings['mainform']['y'] = self.y()
        writesettings()
        setrunning(False)
        self.deleteLater()

    def event_timer(self):
        """Event timer used when a batch is running"""
        try:
            if self.run > 0:
                self.event_parser()
            if batch.changed == 1:
                batch.changed = 0
                currentcycle.setcycle(batch.current()[0])
                self.update_ui_batch_list()
                self.update_ui_commandlist()
                self.update_ui_results_table()
        except ValueError:
            logger.error('t=%s mainUIForm: timedevents value error %s', self.secondcount, Exception())
        except TypeError:
            logger.error('t=%s mainUIForm: timedevents type error %s', self.secondcount, Exception())

    def event_parser(self):
        """Reads tasks from the current cycle list and initiates them if the time is correct"""
        try:
            self.taskrunning = True
            current = currentcycle.currentstep()
            if self.secondcount >= current[0]:
                self.lblCurrent.setText('%s, %s' % (current[1], current[2]))
                if current[1][0:5] == 'valve' or current[1][0:7] == 'pipette':
                    valvechange(current[1], current[2])
                    currentcycle.completecurrent()
                    self.listCommands.takeItem(0)
                elif current[1][0:5] == 'laser':
                    if current[2] == 'on':
                        lasercommand('on')
                    elif current[2] == 'setpower':
                        lasersetpower(currentcycle.laserpower)
                    elif current[2] == 'checkalarms':
                        if lasergetalarm()['status'] != 133:
                            alarms['laseralarm'] = 0
                            self.run = 0  # pause the run as the laser is not ready
                            self.secondincrement = 0
                            self.tbRun.setChecked(False)
                            return
                        alarms['laseralarm'] = 133
                    else:
                        lasercommand('off')
                    currentcycle.completecurrent()
                    self.listCommands.takeItem(0)
                elif current[1][0:7] == 'xytable':
                    self.move_next()
                    currentcycle.completecurrent()
                    self.listCommands.takeItem(0)
                elif current[1] == 'quad':
                    if current[2] == 'starttimer':
                        logger.debug('t=%s mainUIForm: start quad timer', self.secondcount)
                        ms.starttimer(batch.currentcycle(), batch.formatsample(), batch.currentdescription(), batch.id,
                                      batch.runnumber[0])
                        currentcycle.completecurrent()
                        self.listCommands.takeItem(0)
                    elif current[2] == 'starttimer-reheat':
                        logger.debug('t=%s mainUIForm: start quad timer for reheat', self.secondcount)
                        ms.starttimer(batch.currentcycle(), batch.formatsample() + '_RE', batch.currentdescription(),
                                      batch.id, batch.runnumber[0])
                        currentcycle.completecurrent()
                        self.listCommands.takeItem(0)
                    else:
                        if ms.command_parser(current[2]) == 1:
                            currentcycle.completecurrent()
                            self.listCommands.takeItem(0)
                elif current[1] == 'image':
                    logger.debug('t=%s mainUIForm: take image %s', self.secondcount, current[2])
                    batch.image(current[2])
                    currentcycle.completecurrent()
                    self.listCommands.takeItem(0)
                elif current[1] == 'prompt':
                    promptthread = threading.Timer(1, lambda: promptbox(current[2]))
                    promptthread.start()
                    currentcycle.completecurrent()
                    self.listCommands.takeItem(0)
                elif current[1] == 'End':
                    if not batch.isitthereyet(self.xposition, self.yposition):
                        logger.warning('t=%s mainUIform: location not there yet x=%s, y=%s', self.secondcount,
                                       self.xposition, self.yposition)
                        self.lblCurrent.setText('Waiting for X-Y Stage to position')
                        self.taskrunning = False
                        return
                    self.secondincrement = 0
                    logger.info('t=%s mainUIForm: End of cycle detected', self.secondcount)
                    self.lblCurrent.setText('idle')
                    currentrunstate = self.run
                    self.run = 0
                    logger.debug("mainUIForm: starting complete current")
                    batch.completecurrent()
                    logger.debug("mainUIForm: Setting cycle to next")
                    currentcycle.setcycle(batch.current()[0])
                    logger.debug('mainUIForm: New Cycle loaded')
                    self.secondcount = 0
                    logger.debug('mainUIForm: Update lists')
                    self.update_ui_batch_list()
                    self.update_ui_commandlist()
                    self.update_ui_results_table()
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
                else:
                    currentcycle.completecurrent()
                    self.listCommands.takeItem(0)
            self.taskrunning = False
        except:
            self.taskrunning = False
            logger.error('t=%s mainUIForm: runevents error %s', self.secondcount, Exception)

    def menu_show_new_batch(self):
        """Menu handler new batch"""
        self.newdialog = UiBatch()
        self.newdialog.setModal(True)
        self.newdialog.openbatcheck()
        self.newdialog.show()

    def menu_show_about(self):
        """Menu handler show about form"""
        self.newdialog = UiAbout()
        self.newdialog.show()

    def menu_show_log_viewer(self):
        """Menu handler show log viewer"""
        self.newdialog = UiLogViewer()
        self.newdialog.loadlog()
        self.newdialog.show()

    def menu_show_settings_viewer(self):
        """Menu handler show settings viewer"""
        self.newdialog = UiSettingsViewer()
        self.newdialog.loadsettings()
        self.newdialog.show()

    def menu_show_xymanual(self):
        """Menu Handler show xy manual form"""
        self.newdialog = ManualXyForm()
        self.newdialog.setModal(True)
        self.newdialog.show()

    def menu_show_lasermanual(self):
        """Menu Handler show lasermanual form"""
        self.newdialog = LaserFormUI()
        self.newdialog.setModal(True)
        self.newdialog.show()

    def menu_show_ncc(self):
        """Menu Handler show NCC Form"""
        self.newdialog = NccCalcUI()
        self.newdialog.setModal(True)
        self.newdialog.refreshlist()
        self.newdialog.show()

    def update_ui_batch_list(self):
        """Update the btach list"""
        try:
            logger.debug('mainUIForm: Update Batch List')
            self.listBatch.clear()
            self.listBatch.addItems(batch.listformatted())
            text = batch.formatdescription()
            self.linePlanchet.setText(text)
            text = batch.formatsample()
            self.lineLocation.setText(text)
            settings['laser']['power'] = currentcycle.laserpower
            batch.changed = 0
        except:
            logger.error('mainUIForm: batchlist error')

    def update_ui_commandlist(self):
        """Update the list of tasks remsining in the cycle"""
        try:
            logger.debug('mainUIForm: Update command list')
            self.listCommands.clear()
            self.listCommands.addItems(currentcycle.steplistformatted())
        except:
            logger.error('mainUIForm: command list error')

    def update_ui_pressures(self):
        """Update the guage pressures on the top of teh Main Form"""
        pressuresread()
        self.lineIonPump.setText('%.2e' % settings['vacuum']['ion']['current'])
        self.lineTurboPump.setText('%.2e' % settings['vacuum']['turbo']['current'])
        self.lineScrollPump.setText('%.2e' % settings['vacuum']['tank']['current'])

    def update_ui_temprature(self):
        """Update the pyro temperature on the top of teh Main Form"""
        status = tempratureread()
        self.linePyrometer.setText('%s' % settings['pyrometer']['current'])
        self.imgPyrometer.setHidden(not status['laser'])

    def update_ui_xy_positions(self):
        """Update the X anmd Y positions on the top of teh Main Form"""
        status = xyread()
        if status['xmoving'] != 'timeout':
            self.xposition = status['xpos']
            self.yposition = status['ypos']
            self.lineXPosition.setText('%.3f' % self.xposition)
            self.lineYPosition.setText('%.3f' % self.yposition)

    def update_ui_results_table(self):
        """Upfate the results table showing completed batches and the best fit t=0 values"""
        try:
            logger.debug('mainUIForm: Update results')
            self.tableResults.setRowCount(0)
            logger.debug('mainUIForm: Results table cleared')
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
            logger.debug('mainUIForm: Results Table Updated')
        except:
            logger.error('mainUIForm: Update results error - %s', Exception)

    def move_next(self):
        """Move to the next planchet location"""
        logger.debug('t:%s mainUIform: Move to %s', self.secondcount, batch.nextlocation())
        movexthread = threading.Timer(0.5, move_x)
        movexthread.start()
        moveythread = threading.Timer(1.5, move_y)
        moveythread.start()


def move_x():
    """Move the x axis to the next planchet location"""
    location = batch.locxy(batch.nextlocation())
    xymoveto('x', location[0])


def move_y():
    """Move the Y axis to the next planchet location"""
    location = batch.locxy(batch.nextlocation())
    xymoveto('y', location[1])


def manual_laser(state):
    """Pyrometer rangefinder laser handler"""
    pyrolasercommand(state)


def promptbox(message):
    """ Pop up message box"""
    logger.info('Main Form Popup Message sent :%s', message)
    messagebox.showinfo('PyMS', message)
    logger.info('Main Form Popup Message clicked: %s', message)


def restart_pi(host):
    """Reboot a raspberry pi"""
    logger.info('Reboot requested for %s', host)
    msg_box = messagebox.askyesno('Restart the Raspberry Pi',
                                  'Are you really sure you want to reboot the %s?' % host, type=messagebox.YESNO)
    if msg_box:
        logger.warning('Restart confirmed for %s', host)
        rpi_reboot(host)
    else:
        logger.info('Restart cancelled for %s', host)


def menu_open_web_page(page):
    """Menu handler - open host web page"""
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
    elif page == 'Laser Status':
        url = settings['hosts']['laserhost'][:-4]
        webbrowser.open(url)
    elif page == 'Laser Log':
        url = settings['hosts']['laserhost'][:-3] + 'pylog'
        webbrowser.open(url)
    elif page == 'Pump Status':
        url = settings['hosts']['pumphost'][:-4]
        webbrowser.open(url)
    elif page == 'Pump Log':
        url = settings['hosts']['pumphost'][:-3] + 'pylog'
        webbrowser.open(url)
