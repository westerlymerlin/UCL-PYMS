"""
Module for the main window interface of the PyMS application.

This module defines the structure and functionality for the main GUI window of
the Python Mass Spectrometry (PyMS) application. It includes event handlers,
UI updates, and interactions with mass spectrometry hardware and associated
software components.
"""

import webbrowser
from tkinter import messagebox
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QTimer, QThreadPool
from app_control import settings, writesettings, setrunning, alarms, VERSION
from host_queries import valvegetstatus, lasergetstatus, lasergetalarm, pressuresread, xyread
from host_commands import lasercommand, lasersetpower, valvechange, xymoveto, xymove
from batchclass import batch
from cycleclass import currentcycle
from ms_hiden_class import ms
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


GAUGE_GOOD = 'background-color: rgb(255, 255, 255);  color: rgb(10, 10, 10); font: 14pt "Segoe UI"; image: "";'
GAUGE_BAD = 'background-color: rgb(180, 0, 0); color: rgb(255, 255, 255); font: 14pt "Segoe UI"; image: "";'


class UiMain(QMainWindow, Ui_MainWindow):
    """
    UiMain class provides the main interface and control logic for the PyMS application.

    This class is responsible for handling UI interactions, connection to various hardware
    components, and updating the system status. It acts as a centralised hub for managing
    batch processes, valves, and real-time data updates from components such as the vacuum
    gauges and mass spectrometer.
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('PyMS - Python Mass Spectrometry v%s' % VERSION)
        self.imgLaser.setHidden(True)
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
        self.actionValveOpenStatusPage.triggered.connect(lambda: menu_open_web_page('Valve Status'))
        self.actionValveOpenLogPage.triggered.connect(lambda: menu_open_web_page('Valve Log'))
        self.actionPumpOpenStatusPage.triggered.connect(lambda: menu_open_web_page('Pump Status'))
        self.actionPumpOpenLogPage.triggered.connect(lambda: menu_open_web_page('Pump Log'))
        self.actionLaserOpenStatusPage.triggered.connect(lambda: menu_open_web_page('Laser Status'))
        self.actionLaserOpenLogPage.triggered.connect(lambda: menu_open_web_page('Laser Log'))
        self.actionCO2LaserOn.triggered.connect(self.menu_show_lasermanual)
        self.actionAboutPyMS.triggered.connect(self.menu_show_about)
        self.actionHelp.triggered.connect(lambda: menu_open_web_page('Help File'))
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
        self.btnNCCViewer.setHidden(False)
        self.lblIonPump.setText('Ion Gauge (%s)' % settings['vacuum']['ion']['units'])
        self.lblTurboPump.setText('Turbo Gauge (%s)' % settings['vacuum']['turbo']['units'])
        self.lblTankPump.setText('Tank Gauge (%s)' % settings['vacuum']['tank']['units'])
        self.lblN2Pump.setText('N2 Gauge (%s)' % settings['vacuum']['N2']['units'])
        font1 = QFont()
        font1.setFamilies(['Segoe UI'])
        font1.setPointSize(10)
        font1.setBold(True)
        self.tableResults.setColumnWidth(0, 120)
        self.tableResults.setColumnWidth(1, 100)
        self.tableResults.setColumnWidth(2, 175)
        self.tableResults.setColumnWidth(3, 83)
        self.thread_manager = QThreadPool()
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
        self.n2_pressurel_ow = 0
        self.lblCurrent.setText('idle')
        self.update_ui_batch_list()
        self.update_ui_commandlist()
        self.update_ui_results_table()
        self.globaltimer = QTimer()
        self.globaltimer.setTimerType(Qt.TimerType.PreciseTimer)
        self.globaltimer.setInterval(1000)
        self.globaltimer.timeout.connect(self.global_timer)
        self.globaltimer.start()

    def global_timer(self):
        """
        Updates the global timer and manages periodic tasks and UI updates.

        This function increments the timer by a predefined step, updates the displayed
        elapsed time, and triggers several background threads to perform periodic
        updates and checks. Depending on the current timer state, it schedules
        specific tasks such as updating UI components or repainting the interface.
        """
        self.secondcount = self.secondcount + self.secondincrement
        self.lcdElapsedTime.display(self.secondcount)
        self.thread_manager.start(self.update_ui_display_items)
        self.thread_manager.start(self.read_ms)
        self.thread_manager.start(self.check_alarms)
        if not self.taskrunning:
            self.thread_manager.start(self.event_timer)
        if self.timertick == 0 or self.timertick == 2:
            self.thread_manager.start(self.update_ui_xy_positions)
        if self.timertick == 0:
            self.thread_manager.start(self.update_ui_pressures)
        if self.timertick >= 3:
            self.repaint()
            self.timertick = 0
        else:
            self.timertick += 1

    def read_ms(self):
        """
        Reads the status of the Hiden Quadrupole Mass Spectrometer and updates the UI elements
        accordingly based on its online or offline status.
        """
        labletext = ms.check_quad_is_online()
        if labletext != 'Off Line':
            self.imgQMS.setHidden(False)
        else:
            self.imgQMS.setHidden(True)
        self.lblMS.setText(labletext)

    def check_alarms(self):
        """
        Checks various alarm conditions and updates system status accordingly.

        This method evaluates multiple alarm indicators to ensure the proper operation
        of the system. If any issues are detected, it updates the system's status, resets
        relevant operational counters, pauses the system, and generates appropriate alerts.
        The method interacts with a variety of subsystems, including laser controllers, vacuum
        pumps, Hiden instruments, and other hardware components. Alerts and logging are
        generated for detected failures or deviations from normal operating conditions.
        """
        status = ''
        if ms.timeoutcounter > ms.timeoutretries:
            if ms.check_quad_is_online() == 'Off Line':
                status = status + 'The Hiden Quad Reader is showing as offline.\nIt might ' \
                                      'be that the MAS10 application has stopped responding and needs a restart or ' \
                                  'the Hiden Control unit has been switched off, the system is paused. \n'
                self.secondincrement = 0
                self.run = 0
                self.tbRun.setChecked(False)
        if alarms['laseralarm'] != 133:
            logger.error('%s laser alarm firing', alarms['laseralarm'])
            status = status + ('The laser is not ready, please ensure that the laser is powered on, the key is in '
                               'position 2 and the enable button has been pressed. This error can also follow a '
                               'power fail. \n')
            alarms['laseralarm'] = lasergetalarm()['status']
            self.secondincrement = 0
            self.run = 0
            self.tbRun.setChecked(False)
        if alarms['valvehost'] > 10:
            status = status + 'Valve controller is offline, the system is paused. \n'
            self.secondincrement = 0
            self.run = 0
            self.tbRun.setChecked(False)
        if alarms['hidenhost'] == 10:
            status = status + 'Hiden Issue = Hiden has just returned 0 line of data, stopping processing. \n'
            self.secondincrement = 0
            self.run = 0
            self.tbRun.setChecked(False)
        if alarms['hidenhost'] == 11:
            status = status + ('Hiden Issue = the Hiden software has failed to unload the experiment file, please press'
                               ' the red square on teh Hiden app to stop the experiment and then close the experiment'
                               'window and re-press the run button to continue. The system is paused. \n')
            self.secondincrement = 0
            self.run = 0
            self.tbRun.setChecked(False)
        if alarms['hidenhost'] == 12:
            status = status + 'Hiden Issue = Something went wrong with the Hiden, stopping processing. \n'
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
        if alarms['laserhost'] > 10:
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
            self.lineIonPump.setStyleSheet(GAUGE_BAD)
            if self.ionpumphigh > 29:
                status = status + 'Ion pump is showing loss of vacuum, the system is paused. \n'
                self.secondincrement = 0
                self.run = 0
                self.tbRun.setChecked(False)
        else:
            self.ionpumphigh = 0
            self.lineIonPump.setStyleSheet(GAUGE_GOOD)
        if settings['vacuum']['turbo']['current'] > settings['vacuum']['turbo']['high']:
            self.turbopumphigh += 1
            self.lineTurboPump.setStyleSheet(GAUGE_BAD)
            if self.turbopumphigh > 29:
                status = status + 'Turbo gauge is showing loss of vacuum, the system is paused. \n' \
                                  'This is normal during a planchet load \n'
                self.secondincrement = 0
                self.run = 0
                self.tbRun.setChecked(False)
        else:
            self.turbopumphigh = 0
            self.lineTurboPump.setStyleSheet(GAUGE_GOOD)
        if settings['vacuum']['turbo']['current'] == 0:
            status = status + 'Turbo gauge is offline, the system is paused. \n'
            self.secondincrement = 0
            self.run = 0
            self.tbRun.setChecked(False)
        if settings['vacuum']['N2']['current'] < settings['vacuum']['N2']['low']:
            self.n2_pressurel_ow += 1
            self.lineN2Pressure.setStyleSheet(GAUGE_BAD)
            if self.n2_pressurel_ow > 29:
                status = status + 'N2 gauge is showing loss of pressure, the system is paused. \n'
                self.secondincrement = 0
                self.run = 0
                self.tbRun.setChecked(False)
        else:
            self.n2_pressurel_ow = 0
            self.lineN2Pressure.setStyleSheet(GAUGE_GOOD)
        if self.lblAalarm.text() != status:
            self.lblAalarm.setText(status)
            self.lblFinishTime.setText('')
            if status != '':
                alert(status)
                logger.error('Main form major alarm: %s', status)

    def update_ui_display_items(self):
        """
        Updates the UI display elements based on the current status of various system components.

        This method dynamically adjusts the visibility of UI elements representing valves and the laser
        based on their statuses retrieved from external status functions. It ensures the UI remains
        synchronised with the underlying system status by logging changes and updating the visibility
        of corresponding UI components.
        """
        status = valvegetstatus()
        if status[0] == 0:
            if self.wValve1.isVisible() != status[1]:
                logger.debug('t=%s mainUIForm: Valve 1 changed', self.secondcount)
                self.wValve1.setVisible(status[1])
            if self.wValve2.isVisible() != status[2]:
                logger.debug('t=%s mainUIForm: Valve 2 changed', self.secondcount)
                self.wValve2.setVisible(status[2])
            if self.wValve3.isVisible() != status[3]:
                logger.debug('t=%s mainUIForm: Valve 3 changed', self.secondcount)
                self.wValve3.setVisible(status[3])
            if self.wValve4.isVisible() != status[4]:
                logger.debug('t=%s mainUIForm: Valve 4 changed', self.secondcount)
                self.wValve4.setVisible(status[4])
            if self.wValve5.isVisible() != status[5]:
                logger.debug('t=%s mainUIForm: Valve 5 changed', self.secondcount)
                self.wValve5.setVisible(status[5])
            if self.wValve6.isVisible() != status[6]:
                logger.debug('t=%s mainUIForm: Valve 6 changed', self.secondcount)
                self.wValve6.setVisible(status[6])
            if self.wValve7.isVisible() != status[7]:
                logger.debug('t=%s mainUIForm: Valve 7 changed', self.secondcount)
                self.wValve7.setVisible(status[7])
            if self.wValve8.isVisible() != status[8]:
                logger.debug('t=%s mainUIForm: Valve 8 changed', self.secondcount)
                self.wValve8.setVisible(status[8])
            if self.wValve10.isVisible() != status[10]:
                logger.debug('t=%s mainUIForm: Valve 10 changed', self.secondcount)
                self.wValve10.setVisible(status[10])
            if self.wValve11.isVisible() != status[11]:
                logger.debug('t=%s mainUIForm: Valve 11 changed', self.secondcount)
                self.wValve11.setVisible(status[11])
            if self.wValve12.isVisible() != status[12]:
                logger.debug('t=%s mainUIForm: Valve 12 changed', self.secondcount)
                self.wValve12.setVisible(status[12])
            if self.wValve13.isVisible() != status[13]:
                logger.debug('t=%s mainUIForm: Valve 13 changed', self.secondcount)
                self.wValve13.setVisible(status[13])
        self.lblLaserPower.setText('%.1f' % settings['laser']['power'])
        status = lasergetstatus()
        if status['laser'] != 'exception':
            if self.imgLaser.isVisible() != status['laser']:
                logger.debug('t=%s mainUIForm: Laser Status changed', self.secondcount)
                self.imgLaser.setVisible(status['laser'])

    def emergency_stop(self):
        """
        Triggers an emergency stop for the system, halting all ongoing operations, resetting
        counters, and ensuring that safety protocols are followed. This method is designed to
        handle critical situations requiring immediate intervention.
        """
        logger.warning('Main form: Emergency stop triggered')
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
        """
        Handles the click event for the run button in the user interface.

        This method checks the state of the 'Run' toggle button and updates various
        instance attributes accordingly. If the button is pressed, it triggers a 'Run'
        operation, logging the event and initialising associated variables. If the
        button is not pressed, it triggers a 'Pause' operation, logging the event and
        adjusting attributes to reflect the paused state. The method also updates the
        finish time label in the user interface based on the operation mode.
        """
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
        """
        Handles toggling between automated and manual control modes.

        This method adjusts the state of the control panel based on the current
        run mode. It disables or enables certain UI components, updates the status
        label, and controls the laser state accordingly. In case of any errors
        during execution, it logs the error event.
        """
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
        """
        Handles the close event of the main UI form.

        This method is triggered when the main form receives a close event.
        It logs the event, saves the current position of the form to the settings,
        writes the updated settings to persistent storage, flags the application state
        as no longer running, and cleans up the form instance.
        """
        logger.debug('mainUIForm: Main Form close event triggered')
        settings['mainform']['x'] = self.x()
        settings['mainform']['y'] = self.y()
        writesettings()
        setrunning(False)
        self.deleteLater()

    def event_timer(self):
        """
        Handles timed events and updates the user interface based on the current batch's state.

        This method is called periodically to check for updates and handle events such as changes
        to the current batch or executing event parsing logic. It performs the necessary updates to
        reload interface components when the current batch has changed and logs errors in case of
        unexpected issues.
        """
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
        """
        Handles the parsing and execution of events in a predefined sequence.

        This method is responsible for managing the execution of commands in the current cycle
        based on specific timing and conditions. It performs various tasks depending on the type
        of command, such as controlling valves, lasers, an XY table, taking images, sending manual
        messages, or handling the end of a cycle. It ensures synchronisation of the sequence,
        monitors laser alarms, and updates the list and state of the program accordingly.
        """
        try:
            self.taskrunning = True
            current = currentcycle.currentstep()
            if self.secondcount >= current[0]:
                self.lblCurrent.setText('%s, %s' % (current[1], current[2]))
                if current[1][0:5] == 'valve':
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
                elif current[1] == 'manual':
                    self.manual_message(current[2])
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
        """
        Displays a new batch dialog.

        This method initialises and shows a modal dialogue for creating or working
        with a new batch. It ensures the dialogue is set up properly and executes
        necessary checks before display.
        """
        self.newdialog = UiBatch()
        self.newdialog.setModal(True)
        self.newdialog.openbatcheck()
        self.newdialog.show()

    def menu_show_about(self):
        """
        Displays the "About" dialogue for the application.

        This method is responsible for initialising and displaying the "About"
        dialog when triggered. It creates an instance of the UiAbout class
        and uses it to show the dialogue to the user.
        """
        self.newdialog = UiAbout()
        self.newdialog.show()

    def menu_show_log_viewer(self):
        """
        Displays and initialises the log viewer dialogue.

        This method creates an instance of the log viewer dialogue, loads the log
        data, and makes the dialogue visible to the user.
        """
        self.newdialog = UiLogViewer()
        self.newdialog.loadlog()
        self.newdialog.show()

    def menu_show_settings_viewer(self):
        """
        Displays the settings viewer dialogue.

        This method initialises and displays the settings viewer dialogue to allow
        users to view and manage application settings and secrets.
        """
        self.newdialog = UiSettingsViewer()
        self.newdialog.load_settings_secrets()
        self.newdialog.show()

    def menu_show_xymanual(self):
        """
        Displays the XY Manual dialogue to the user.

        This method initialises and displays a modal dialogue, allowing the
        user to interact with the XY Manual form.
        """
        self.newdialog = ManualXyForm()
        self.newdialog.setModal(True)
        self.newdialog.show()

    def menu_show_lasermanual(self):
        """
        Displays the laser manual interface by opening a new modal dialogue.

        This method is responsible for initialising and displaying a modal dialogue
        for the laser manual interface. It ensures the dialogue is modal to prevent
        interaction with the main interface while the dialogue is open.
        """
        self.newdialog = LaserFormUI()
        self.newdialog.setModal(True)
        self.newdialog.show()

    def menu_show_ncc(self):
        """
        Displays the NCC Calculation Menu.

        This method initialises an instance of the NccCalcUI class, sets it as a modal dialogue,
        refreshes its content, and displays the dialogue.
        """
        self.newdialog = NccCalcUI()
        self.newdialog.setModal(True)
        self.newdialog.refreshlist()
        self.newdialog.show()

    def update_ui_batch_list(self):
        """
        Updates the batch list in the user interface by clearing and repopulating the list,
        and also updates other related UI elements with formatted information from the
        batch and cycle data. Any errors during this process are logged.
        """
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
        """
        Updates the UI command list with the current cycle's formatted steps.

        This method clears the existing commands from the UI list and populates it with
        the formatted steps of the current cycle. Logs debug messages during the process
        and logs errors if an exception occurs.
        """
        try:
            logger.debug('mainUIForm: Update command list')
            self.listCommands.clear()
            self.listCommands.addItems(currentcycle.steplistformatted())
        except:
            logger.error('mainUIForm: command list error')

    def update_ui_pressures(self):
        """
        Updates the user interface with the latest vacuum pressures.

        This method retrieves current pressure readings for various vacuum components
        and updates the corresponding UI text fields. The values are formatted
        appropriately for display. If the nitrogen (N2) pressure exceeds a specific
        threshold, its display value is shown as "N/A".
        """
        pressuresread()
        self.lineIonPump.setText('%.2e' % settings['vacuum']['ion']['current'])
        self.lineTurboPump.setText('%.2e' % settings['vacuum']['turbo']['current'])
        self.lineScrollPump.setText('%.2e' % settings['vacuum']['tank']['current'])
        if settings['vacuum']['N2']['current'] > 500:
            self.lineN2Pressure.setText('N/A')
        else:
            self.lineN2Pressure.setText('%.2f' % settings['vacuum']['N2']['current'])


    def update_ui_xy_positions(self):
        """
        Updates the UI with the current X and Y positions.

        This method fetches the current X and Y positions by reading the status
        using the `xyread` function. If the status of the X movement is not
        'timeout', the method updates the X and Y position attributes and
        reflects these values in the respective UI elements for display.
        """
        status = xyread()
        if status['xmoving'] != 'timeout':
            self.xposition = status['xpos']
            self.yposition = status['ypos']
            self.lineXPosition.setText('%.3f' % self.xposition)
            self.lineYPosition.setText('%.3f' % self.yposition)

    def update_ui_results_table(self):
        """
        Updates the user interface results table with the latest data.

        This method retrieves the batch results and updates the table displayed
        in the user interface by clearing old entries and repopulating the table with
        new information. Each row of the table represents a result with the
        corresponding timestamp, file name, description, and result value.
        """
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
        """
        Moves to the next specified location by initiating motion threads.

        This method is responsible for transitioning to the next location provided
        by the batch system. It uses threads managed by `thread_manager` to
        initiate movement along the x and y axes. Debug logs are generated for
        tracking the operation status.
        """
        logger.debug('t:%s mainUIform: Move to %s', self.secondcount, batch.nextlocation())
        self.thread_manager.start(move_x)
        self.thread_manager.start(move_y)
        #movexthread = threading.Timer(0.5, move_x)
        #movexthread.start()
        #moveythread = threading.Timer(1.5, move_y)
        #moveythread.start()

    def manual_message(self, message):
        """
        Provides a method to display a manual step message to the user through a popup.

            Displays a popup message to inform the user about a necessary manual step in
            the application. The main form's state is temporarily updated to handle this
            manual step, and once the user acknowledges the popup, the state is restored.
        """
        logger.info('Main Form Popup Message sent :%s', message)
        secondinc = self.secondincrement
        self.secondincrement = 0
        messagebox.showinfo('PyMS Manual Step', 'There is a manual step needed:\n\n%s\n\n'
                                                'Please complete the action and click ok to continue' % message)
        self.secondincrement = secondinc
        self.lblFinishTime.setText(batch.finishtime())
        logger.info('Main Form Popup Message clicked: %s', message)


def move_x():
    """
    Moves the object to a new x-coordinate based on the next location from the batch.

    This function retrieves the next location coordinates from the batch and moves
    """
    location = batch.locxy(batch.nextlocation())
    xymoveto('x', location[0])


def move_y():
    """
    Moves an object along the Y-axis to a specified location.

    The function determines the next location of the object and moves it
    to the corresponding Y-coordinate. It utilizes data from the `batch`
    object to calculate the target position.
    """
    location = batch.locxy(batch.nextlocation())
    xymoveto('y', location[1])

def menu_open_web_page(page):
    """
    Opens a specific web page or file based on the provided page identifier.

    This function dynamically generates URLs based on the given page identifier
    and the host configuration stored within the `settings` dictionary. It supports
    various categories such as status pages, log pages, and static files. Corresponding
    URLs are opened using the default web browser.
    """
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
    elif page == 'Help File':
        url = 'readme.pdf'
        webbrowser.open(url)
