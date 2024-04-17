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
        """Initialise the form, if new set to blank but if the batch exists populate sample names into relevant
         locations"""
        self.configure_tasks_and_locations()
        self.btnSave.clicked.connect(self.savechecks)
        self.btnClose.clicked.connect(self.formclose)
        self.lineDescription.setText(batch.description)
        self.lineDate.setText(batch.date)
        self.update_ui_for_batch_info()

    def configure_tasks_and_locations(self):
        """"setup the individual combo boxes"""
        for i in range(1, 9):
            getattr(self, f'comboTask{i}').activated.connect(lambda index=i: self.task_combo_click(index))
            getattr(self, f'comboTask{i}').addItems(currentcycle.cycles)
            getattr(self, f'comboLocation{i}').addItems(currentcycle.locations)

    def update_ui_for_batch_info(self):
        """Add in infor from the current batch"""
        for i in range(1, 9):
            if len(batch.runnumber) > i - 1:
                getattr(self, f'comboTask{i}').setCurrentText(batch.cycle[i - 1])
                getattr(self, f'comboLocation{i}').setCurrentText(batch.location[i - 1])
                getattr(self, f'lineSample{i}').setText(batch.identifier[i - 1])
            self.task_combo_click(i)
        if batch.runnumber:
            self.setWindowTitle('Unfinished steps from batch # %i' % batch.id)

    def formclose(self):
        """Form close handler"""
        settings['simplebatchform']['x'] = self.x()
        settings['simplebatchform']['y'] = self.y()
        self.deleteLater()

    def task_combo_click(self, index):
        """ Handles the clicking of the task combo boxes. """
        combos_task = [
            self.comboTask1, self.comboTask2, self.comboTask3, self.comboTask4,
            self.comboTask5, self.comboTask6, self.comboTask7, self.comboTask8
        ]
        combos_location = [
            self.comboLocation1, self.comboLocation2, self.comboLocation3,
            self.comboLocation4, self.comboLocation5, self.comboLocation6,
            self.comboLocation7, self.comboLocation8
        ]
        lines_sample = [
            self.lineSample1, self.lineSample2, self.lineSample3, self.lineSample4,
            self.lineSample5, self.lineSample6, self.lineSample7, self.lineSample8
        ]
        self.handle_combo_click(index, combos_task, combos_location, lines_sample)

    def handle_combo_click(self, index, combos_task, combos_location, lines_sample):
        """ setup combo boxes """
        if combos_task[index - 1].currentText() == 'End':
            try:
                combos_task[index].setCurrentIndex(0)
                combos_task[index].setEnabled(False)
                self.btnSave.setEnabled(False)
                self.handle_combo_click(index + 1, combos_task, combos_location, lines_sample)
            except IndexError:
                pass
        else:
            try:
                combos_task[index].setEnabled(True)
                self.btnSave.setEnabled(True)
            except IndexError:
                pass

        if currentcycle.sample(combos_task[index - 1].currentText()):
            combos_location[index - 1].setEnabled(True)
            lines_sample[index - 1].setEnabled(True)
        else:
            combos_location[index - 1].setEnabled(False)
            lines_sample[index - 1].setEnabled(False)

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
