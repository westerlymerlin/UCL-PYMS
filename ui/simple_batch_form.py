"""
Dialog for a simple batch (used for tesing the Helium line) has a maximum of 5 stepa
Author: Gary Twinn
"""
import sys
from PySide6.QtWidgets import QDialog, QApplication
from ui.ui_layout_simple_batch import Ui_dialogSimpleBatch
from app_control import settings
from batchclass import batch
from cycleclass import currentcycle
from logmanager import logger


class UiSimpleBatch(QDialog, Ui_dialogSimpleBatch):
    """Dialog Class"""
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(settings['simplebatchform']['x'], settings['simplebatchform']['y'])
        self.recordnumber = -1

    def startup(self):
        """Initialise the form, if new set to blank but if the batch exists populate sample names into the relavent
         locations"""
        self.comboTask1.activated.connect(lambda: self.taskcomboclick(1))
        self.comboTask2.activated.connect(lambda: self.taskcomboclick(2))
        self.comboTask3.activated.connect(lambda: self.taskcomboclick(3))
        self.comboTask4.activated.connect(lambda: self.taskcomboclick(4))
        self.comboTask5.activated.connect(lambda: self.taskcomboclick(5))
        self.comboTask6.activated.connect(lambda: self.taskcomboclick(6))
        self.comboTask7.activated.connect(lambda: self.taskcomboclick(7))
        self.comboTask8.activated.connect(lambda: self.taskcomboclick(8))
        self.btnSave.clicked.connect(self.savechecks)
        self.btnClose.clicked.connect(self.formclose)
        self.comboTask1.addItems(currentcycle.cycles)
        self.comboTask2.addItems(currentcycle.cycles)
        self.comboTask3.addItems(currentcycle.cycles)
        self.comboTask4.addItems(currentcycle.cycles)
        self.comboTask5.addItems(currentcycle.cycles)
        self.comboTask6.addItems(currentcycle.cycles)
        self.comboTask7.addItems(currentcycle.cycles)
        self.comboTask8.addItems(currentcycle.cycles)
        self.comboLocation1.addItems(currentcycle.locations)
        self.comboLocation2.addItems(currentcycle.locations)
        self.comboLocation3.addItems(currentcycle.locations)
        self.comboLocation4.addItems(currentcycle.locations)
        self.comboLocation5.addItems(currentcycle.locations)
        self.comboLocation6.addItems(currentcycle.locations)
        self.comboLocation7.addItems(currentcycle.locations)
        self.comboLocation8.addItems(currentcycle.locations)
        self.lineDescription.setText(batch.description)
        self.lineDate.setText(batch.date)
        if len(batch.runnumber) > 7:
            self.comboTask8.setCurrentText(batch.cycle[7])
            self.comboLocation8.setCurrentText(batch.location[7])
            self.lineSample8.setText(batch.identifier[7])
            self.taskcomboclick(8)
        if len(batch.runnumber) > 6:
            self.comboTask7.setCurrentText(batch.cycle[6])
            self.comboLocation7.setCurrentText(batch.location[6])
            self.lineSample7.setText(batch.identifier[6])
            self.taskcomboclick(7)
        if len(batch.runnumber) > 5:
            self.comboTask6.setCurrentText(batch.cycle[5])
            self.comboLocation6.setCurrentText(batch.location[5])
            self.lineSample6.setText(batch.identifier[5])
            self.taskcomboclick(6)
        if len(batch.runnumber) > 4:
            self.comboTask5.setCurrentText(batch.cycle[4])
            self.comboLocation5.setCurrentText(batch.location[4])
            self.lineSample5.setText(batch.identifier[4])
            self.taskcomboclick(5)
        if len(batch.runnumber) > 3:
            self.comboTask4.setCurrentText(batch.cycle[3])
            self.comboLocation4.setCurrentText(batch.location[3])
            self.lineSample4.setText(batch.identifier[3])
            self.taskcomboclick(4)
        if len(batch.runnumber) > 2:
            self.comboTask3.setCurrentText(batch.cycle[2])
            self.comboLocation3.setCurrentText(batch.location[2])
            self.lineSample3.setText(batch.identifier[2])
            self.taskcomboclick(3)
        if len(batch.runnumber) > 1:
            self.comboTask2.setCurrentText(batch.cycle[1])
            self.comboLocation2.setCurrentText(batch.location[1])
            self.lineSample2.setText(batch.identifier[1])
            self.taskcomboclick(2)
        if len(batch.runnumber) > 0:
            self.comboTask1.setCurrentText(batch.cycle[0])
            self.comboLocation1.setCurrentText(batch.location[0])
            self.lineSample1.setText(batch.identifier[0])
            self.lineDate.setText(batch.date)
            self.lineDescription.setText(batch.description)
            self.setWindowTitle('Unfinished steps from batch # %i' % batch.id)
            self.taskcomboclick(1)
    def formclose(self):
        """Form close handler"""
        settings['simplebatchform']['x'] = self.x()
        settings['simplebatchform']['y'] = self.y()
        self.deleteLater()

    def taskcomboclick(self, index):
        """Combo box handler"""
        if index == 1:
            if self.comboTask1.currentText() == 'End':
                self.comboTask2.setCurrentIndex(0)
                self.comboTask2.setEnabled(False)
                self.btnSave.setEnabled(False)
                self.taskcomboclick(2)
            else:
                self.comboTask2.setEnabled(True)
                self.btnSave.setEnabled(True)
            if currentcycle.sample(self.comboTask1.currentText()):
                self.comboLocation1.setEnabled(True)
                self.lineSample1.setEnabled(True)
            else:
                self.comboLocation1.setEnabled(False)
                self.lineSample1.setEnabled(False)
        elif index == 2:
            if self.comboTask2.currentText() == 'End':
                self.comboTask3.setCurrentIndex(0)
                self.comboTask3.setEnabled(False)
                self.taskcomboclick(3)
            else:
                self.comboTask3.setEnabled(True)
            if currentcycle.sample(self.comboTask2.currentText()):
                self.comboLocation2.setEnabled(True)
                self.lineSample2.setEnabled(True)
            else:
                self.comboLocation2.setEnabled(False)
                self.lineSample2.setEnabled(False)
        elif index == 3:
            if self.comboTask3.currentText() == 'End':
                self.comboTask4.setCurrentIndex(0)
                self.comboTask4.setEnabled(False)
                self.taskcomboclick(4)
            else:
                self.comboTask4.setEnabled(True)
            if currentcycle.sample(self.comboTask3.currentText()):
                self.comboLocation3.setEnabled(True)
                self.lineSample3.setEnabled(True)
            else:
                self.comboLocation3.setEnabled(False)
                self.lineSample3.setEnabled(False)
        elif index == 4:
            if self.comboTask4.currentText() == 'End':
                self.comboTask5.setCurrentIndex(0)
                self.comboTask5.setEnabled(False)
                self.taskcomboclick(5)
            else:
                self.comboTask5.setEnabled(True)
            if currentcycle.sample(self.comboTask4.currentText()):
                self.comboLocation4.setEnabled(True)
                self.lineSample4.setEnabled(True)
            else:
                self.comboLocation4.setEnabled(False)
                self.lineSample4.setEnabled(False)
        elif index == 5:
            if self.comboTask5.currentText() == 'End':
                self.comboTask6.setCurrentIndex(0)
                self.comboTask6.setEnabled(False)
                self.taskcomboclick(6)
            else:
                self.comboTask6.setEnabled(True)
            if currentcycle.sample(self.comboTask5.currentText()):
                self.comboLocation5.setEnabled(True)
                self.lineSample5.setEnabled(True)
            else:
                self.comboLocation5.setEnabled(False)
                self.lineSample5.setEnabled(False)
        elif index == 6:
            if self.comboTask6.currentText() == 'End':
                self.comboTask7.setCurrentIndex(0)
                self.comboTask7.setEnabled(False)
                self.taskcomboclick(7)
            else:
                self.comboTask7.setEnabled(True)
            if currentcycle.sample(self.comboTask6.currentText()):
                self.comboLocation6.setEnabled(True)
                self.lineSample6.setEnabled(True)
            else:
                self.comboLocation6.setEnabled(False)
                self.lineSample6.setEnabled(False)
        elif index == 7:
            if self.comboTask7.currentText() == 'End':
                self.comboTask8.setCurrentIndex(0)
                self.comboTask8.setEnabled(False)
                self.taskcomboclick(7)
            else:
                self.comboTask8.setEnabled(True)
            if currentcycle.sample(self.comboTask6.currentText()):
                self.comboLocation7.setEnabled(True)
                self.lineSample7.setEnabled(True)
            else:
                self.comboLocation7.setEnabled(False)
                self.lineSample7.setEnabled(False)
        elif index == 8:
            if currentcycle.sample(self.comboTask5.currentText()):
                self.comboLocation8.setEnabled(True)
                self.lineSample8.setEnabled(True)
            else:
                self.comboLocation8.setEnabled(False)
                self.lineSample8.setEnabled(False)

    def savechecks(self):
        """Tests to run before saving to ensure every sample has a valid name"""
        try:
            taskbatch = [[self.comboTask1.currentText(), self.comboLocation1.currentText(), self.lineSample1.text()],
                         [self.comboTask2.currentText(), self.comboLocation2.currentText(), self.lineSample2.text()],
                         [self.comboTask3.currentText(), self.comboLocation3.currentText(), self.lineSample3.text()],
                         [self.comboTask4.currentText(), self.comboLocation4.currentText(), self.lineSample4.text()],
                         [self.comboTask5.currentText(), self.comboLocation5.currentText(), self.lineSample5.text()],
                         [self.comboTask6.currentText(), self.comboLocation6.currentText(), self.lineSample6.text()],
                         [self.comboTask7.currentText(), self.comboLocation7.currentText(), self.lineSample7.text()],
                         [self.comboTask8.currentText(), self.comboLocation8.currentText(), self.lineSample8.text()]]
            errormessage = []
            if len(self.lineDescription.text()) == 0:
                errormessage.append('There is no decription for this batch')
            for index, task in enumerate(taskbatch):
                if currentcycle.sample(task[0]) == 0:
                    task[1] = ''
                    task[2] = ''
                else:
                    if task[2] == '':
                        errormessage.append('Task %i does not have a sample reference' % (index + 1))
            if len(errormessage) > 0:
                errormessage.append('This batch has not been saved')
                self.labelError.setText('\n'.join(errormessage))
                return
            if batch.id == -1:
                batch.new('simple', self.lineDescription.text().strip())
                for task in taskbatch:
                    if task[0] != 'End':
                        batch.addstep(task[0], task[1], task[2])
                batch.save()
                self.deleteLater()
            else:
                batch.description = self.lineDescription.text()
                index = 0
                for task in taskbatch:
                    logger.debug('Simple Batch save: %s %s', index, len(batch.runnumber))
                    if index < len(batch.runnumber):
                        if task[0] == 'End':
                            logger.debug('Simple Batch save: mark as end')
                            batch.status[index] = 2
                        else:
                            logger.debug('Simple Batch save: update existing')
                            batch.cycle[index] = task[0]
                            batch.location[index] = task[1]
                            batch.identifier[index] = task[2]
                    else:
                        if task[0] != 'End':
                            logger.debug('Simple Batch save: adnew')
                            batch.addstep(task[0], task[1], task[2])
                    index = index + 1
                batch.save()
                self.deleteLater()
        except:
            logger.error('Simple Batch save: save error')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = UiSimpleBatch()
    dialog.startup()
    print(currentcycle.samples)
    dialog.show()
    sys.exit(app.exec())
