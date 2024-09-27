"""
Laser Manual Form, used to manually control the Helium line laser ina  controlled manner
Author: Gary Twinn
"""

import sys
from PySide6.QtCore import Qt, QTimer, QThreadPool
from PySide6.QtWidgets import QDialog, QApplication
from ui.ui_layout_laser import Ui_dialogLaserControl
from app_control import settings
from host_queries import lasergetalarm
from host_commands import lasercommand, lasersetpower


class LaserFormUI(QDialog, Ui_dialogLaserControl):
    """The LaserFormUI class represents a dialog window for controlling a laser."""
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(settings['laserform']['x'], settings['laserform']['y'])
        self.laserpower = settings['laser']['power']
        self.sliderLaser.setValue(self.laserpower * 10)
        self.imgLaser.setVisible(False)
        self.btnClose.clicked.connect(self.formclose)
        self.sliderEnable.valueChanged.connect(self.enable_click)
        self.btnOn.clicked.connect(self.laser_click)
        self.sliderLaser.valueChanged.connect(self.slidermove)
        self.btnOn.setEnabled(False)
        self.thread_manager = QThreadPool()
        self.state = {'laser': 0, 'power': 0, 'status': 0}
        self.globaltimer = QTimer()
        self.globaltimer.setTimerType(Qt.TimerType.PreciseTimer)
        self.globaltimer.setInterval(1000)
        self.globaltimer.timeout.connect(self.update_laser)
        self.globaltimer.start()

    def formclose(self):
        """Form close event handler"""
        settings['laserform']['x'] = self.x()
        settings['laserform']['y'] = self.y()
        self.btnOn.setChecked(False)
        self.btnOn.setEnabled(False)
        self.laser_click()
        self.deleteLater()

    def slidermove(self):
        """Laser power slider event handler"""
        self.laserpower = self.sliderLaser.value()

    def enable_click(self):
        """Laser enable button event handler"""
        if self.sliderEnable.value() == 2:
            self.btnOn.setEnabled(True)
        else:
            self.btnOn.setChecked(False)
            self.btnOn.setEnabled(False)
            self.laser_click()

    def laser_click(self):
        """Laser on off event handler"""
        if self.btnOn.isChecked():
            settings['laser']['power'] = self.laserpower
            lasersetpower(self.laserpower)
            lasercommand('on')
        else:
            if self.state['laser'] == 1:
                lasercommand('off')

    def update_laser(self):
        """Update laser status and laser power"""
        self.state = lasergetalarm()
        print(self.state)
        if self.state['status'] == 133:
            self.lblStatus.setText('Laser On')
            self.sliderEnable.setToolTip('Slide down to enable ON button')
        else:
            self.lblStatus.setText('Laser Off')
            self.sliderEnable.setValue(0)
            self.sliderEnable.setToolTip('Laser is not ready, please switch it on, switch the key to 2 and press the yellow button')
        if self.state['laser'] == 1:
            self.imgLaser.setVisible(True)
        else:
            self.imgLaser.setVisible(False)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = LaserFormUI()
    dialog.show()
    sys.exit(app.exec())
