from PySide6.QtWidgets import *
from ui.ui_laser import Ui_dialogLaserControl
from settings import settings
from host_queries import lasergetstatus
from host_commands import lasercommand, lasersetpower
import threading
import sys


class LaserFormUI(QDialog, Ui_dialogLaserControl):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(settings['laserform']['x'], settings['laserform']['y'])
        self.laserpower = settings['laser']['power']
        self.lblLaser.setText('%.1f' % self.laserpower)
        self.sliderLaser.setValue(self.laserpower * 10)
        self.imgLaser.setVisible(False)
        self.btnClose.clicked.connect(self.formclose)
        self.sliderEnable.valueChanged.connect(self.enable_click)
        self.btnOn.clicked.connect(self.laser_click)
        self.sliderLaser.valueChanged.connect(self.slidermove)
        self.btnOn.setEnabled(False)
        self.running = 1
        threading.Timer(1, self.timer).start()

    def timer(self):
        if self.running:
            timerthread = threading.Timer(1, self.timer)
            timerthread.start()
            laserthread = threading.Timer(0.05, self.update_laser)
            laserthread.start()

    def formclose(self):
        self.running = 0
        settings['laserform']['x'] = self.x()
        settings['laserform']['y'] = self.y()
        self.btnOn.setChecked(False)
        self.btnOn.setEnabled(False)
        self.laser_click()
        self.deleteLater()

    def slidermove(self):
        self.laserpower = self.sliderLaser.value() /10
        self.lblLaser.setText('%.1f' % self.laserpower)

    def enable_click(self):
        if self.sliderEnable.value() == 2:
            self.btnOn.setEnabled(True)
        else:
            self.btnOn.setChecked(False)
            self.btnOn.setEnabled(False)
            self.laser_click()

    def laser_click(self):
        if self.btnOn.isChecked():
            settings['laser']['power'] = self.laserpower
            lasersetpower(self.laserpower)
            lasercommand('on')
        else:
            lasercommand('off')

    def update_laser(self):
        state = lasergetstatus()
        self.imgLaser.setVisible(state['laser'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = LaserFormUI()
    dialog.show()
    sys.exit(app.exec())
