"""
Planchet entry form
Author: Gary Twinn
"""
import sys
from PySide6.QtWidgets import QDialog, QApplication
from ui.ui_layout_planchet_batch import Ui_dialogPlanchet
from app_control import settings
from batchclass import batch
from cycleclass import currentcycle


class UiPlanchet(QDialog, Ui_dialogPlanchet):
    """Form class for the planchet"""
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(settings['planchetform']['x'], settings['planchetform']['y'])
        self.recordnumber = -1

    def startup(self):
        """Initialise the planchet, if new set to blank but if the batch exists populate sample names int the planchet
         locations"""
        self.btnClose.clicked.connect(self.formclose)
        self.btnSave.clicked.connect(self.savechecks)
        self.comboTask1.addItems(cycle for cycle in currentcycle.samples)
        self.comboTask1.setCurrentText('Apatite + Reheat')
        self.lineDate.setText(batch.date)
        if len(batch.runnumber) > 0:
            self.lineDescription.setText(batch.description)
            self.setWindowTitle('Unfinished steps from planchet # %i' % batch.id)
            self.lineS1.setText(batch.getlocationsample('S1'))
            self.lineS2.setText(batch.getlocationsample('S2'))
            self.lineS3.setText(batch.getlocationsample('S2'))
            self.lineA1.setText(batch.getlocationsample('A1'))
            self.lineA2.setText(batch.getlocationsample('A2'))
            self.lineA3.setText(batch.getlocationsample('A3'))
            self.lineA4.setText(batch.getlocationsample('A4'))
            self.lineA5.setText(batch.getlocationsample('A5'))
            self.lineA6.setText(batch.getlocationsample('A6'))
            self.lineA7.setText(batch.getlocationsample('A7'))
            self.lineB1.setText(batch.getlocationsample('B1'))
            self.lineB2.setText(batch.getlocationsample('B2'))
            self.lineB3.setText(batch.getlocationsample('B3'))
            self.lineB4.setText(batch.getlocationsample('B4'))
            self.lineB5.setText(batch.getlocationsample('B5'))
            self.lineB6.setText(batch.getlocationsample('B6'))
            self.lineB7.setText(batch.getlocationsample('B7'))
            self.lineC1.setText(batch.getlocationsample('C1'))
            self.lineC2.setText(batch.getlocationsample('C2'))
            self.lineC3.setText(batch.getlocationsample('C3'))
            self.lineC4.setText(batch.getlocationsample('C4'))
            self.lineC5.setText(batch.getlocationsample('C5'))
            self.lineC6.setText(batch.getlocationsample('C6'))
            self.lineC7.setText(batch.getlocationsample('C7'))
            self.lineD1.setText(batch.getlocationsample('D1'))
            self.lineD2.setText(batch.getlocationsample('D2'))
            self.lineD3.setText(batch.getlocationsample('D3'))
            self.lineD4.setText(batch.getlocationsample('D4'))
            self.lineD5.setText(batch.getlocationsample('D5'))
            self.lineD6.setText(batch.getlocationsample('D6'))
            self.lineD7.setText(batch.getlocationsample('D7'))
            self.lineE1.setText(batch.getlocationsample('E1'))
            self.lineE2.setText(batch.getlocationsample('E2'))
            self.lineE3.setText(batch.getlocationsample('E3'))
            self.lineE4.setText(batch.getlocationsample('E4'))
            self.lineE5.setText(batch.getlocationsample('E5'))
            self.lineE6.setText(batch.getlocationsample('E6'))
            self.lineE7.setText(batch.getlocationsample('E7'))
            self.lineF1.setText(batch.getlocationsample('F1'))
            self.lineF2.setText(batch.getlocationsample('F2'))
            self.lineF3.setText(batch.getlocationsample('F3'))
            self.lineF4.setText(batch.getlocationsample('F4'))
            self.lineF5.setText(batch.getlocationsample('F5'))
            self.lineF6.setText(batch.getlocationsample('F6'))
            self.lineF7.setText(batch.getlocationsample('F7'))
            self.lineG1.setText(batch.getlocationsample('G1'))
            self.lineG2.setText(batch.getlocationsample('G2'))
            self.lineG3.setText(batch.getlocationsample('G3'))
            self.lineG4.setText(batch.getlocationsample('G4'))
            self.lineG5.setText(batch.getlocationsample('G5'))
            self.lineG6.setText(batch.getlocationsample('G6'))
            self.lineG7.setText(batch.getlocationsample('G7'))
            self.lineS4.setText(batch.getlocationsample('S4'))
            self.lineS5.setText(batch.getlocationsample('S5'))
            self.lineS6.setText(batch.getlocationsample('S6'))

    def formclose(self):
        """Form close event handler"""
        settings['planchetform']['x'] = self.x()
        settings['planchetform']['y'] = self.y()
        self.deleteLater()

    def savechecks(self):
        """Tests to run before saving to ensure every sample has a valid name"""
        errormessage = []
        if len(self.lineDescription.text()) == 0:
            errormessage.append('There is no decription for this planchet')
        taskbatch = []
        if self.lineS1.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'S1', self.lineS1.text()])
        if self.lineS2.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'S2', self.lineS2.text()])
        if self.lineS3.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'S3', self.lineS3.text()])
        if self.lineA1.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'A1', self.lineA1.text()])
        if self.lineA2.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'A2', self.lineA2.text()])
        if self.lineA3.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'A3', self.lineA3.text()])
        if self.lineA4.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'A4', self.lineA4.text()])
        if self.lineA5.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'A5', self.lineA5.text()])
        if self.lineA6.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'A6', self.lineA6.text()])
        if self.lineA7.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'A7', self.lineA7.text()])
        if self.lineB1.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'B1', self.lineB1.text()])
        if self.lineB2.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'B2', self.lineB2.text()])
        if self.lineB3.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'B3', self.lineB3.text()])
        if self.lineB4.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'B4', self.lineB4.text()])
        if self.lineB5.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'B5', self.lineB5.text()])
        if self.lineB6.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'B6', self.lineB6.text()])
        if self.lineB7.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'B7', self.lineB7.text()])
        if self.lineC1.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'C1', self.lineC1.text()])
        if self.lineC2.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'C2', self.lineC2.text()])
        if self.lineC3.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'C3', self.lineC3.text()])
        if self.lineC4.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'C4', self.lineC4.text()])
        if self.lineC5.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'C5', self.lineC5.text()])
        if self.lineC6.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'C6', self.lineC6.text()])
        if self.lineC7.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'C7', self.lineC7.text()])
        if self.lineD1.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'D1', self.lineD1.text()])
        if self.lineD2.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'D2', self.lineD2.text()])
        if self.lineD3.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'D3', self.lineD3.text()])
        if self.lineD4.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'D4', self.lineD4.text()])
        if self.lineD5.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'D5', self.lineD5.text()])
        if self.lineD6.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'D6', self.lineD6.text()])
        if self.lineD7.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'D7', self.lineD7.text()])
        if self.lineE1.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'E1', self.lineE1.text()])
        if self.lineE2.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'E2', self.lineE2.text()])
        if self.lineE3.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'E3', self.lineE3.text()])
        if self.lineE4.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'E4', self.lineE4.text()])
        if self.lineE5.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'E5', self.lineE5.text()])
        if self.lineE6.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'E6', self.lineE6.text()])
        if self.lineE7.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'E7', self.lineE7.text()])
        if self.lineF1.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'F1', self.lineF1.text()])
        if self.lineF2.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'F2', self.lineF2.text()])
        if self.lineF3.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'F3', self.lineF3.text()])
        if self.lineF4.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'F4', self.lineF4.text()])
        if self.lineF5.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'F5', self.lineF5.text()])
        if self.lineF6.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'F6', self.lineF6.text()])
        if self.lineF7.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'F7', self.lineF7.text()])
        if self.lineG1.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'G1', self.lineG1.text()])
        if self.lineG2.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'G2', self.lineG2.text()])
        if self.lineG3.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'G3', self.lineG3.text()])
        if self.lineG4.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'G4', self.lineG4.text()])
        if self.lineG5.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'G5', self.lineG5.text()])
        if self.lineG6.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'G6', self.lineG6.text()])
        if self.lineG7.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'G7', self.lineG7.text()])
        if self.lineS4.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'S4', self.lineS4.text()])
        if self.lineS5.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'S5', self.lineS5.text()])
        if self.lineS6.text() != '':
            taskbatch.append([self.comboTask1.currentText(), 'S6', self.lineS6.text()])
        if len(taskbatch) == 0:
            errormessage.append('There are no samples defined in the planchet')
        if len(errormessage) > 0:
            errormessage.append('This batch has not been saved ')
            self.labelError.setText('\n'.join(errormessage))
            return
        batch.new('planchet', self.lineDescription.text())
        for task in taskbatch:
            batch.addstep(task[0], task[1], task[2])
        batch.save()
        self.deleteLater()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = UiPlanchet()
    dialog.startup()
    dialog.show()
    sys.exit(app.exec())
