from PySide6.QtWidgets import *
from ui_simplebatch import Ui_dialogSimpleBatch
from settings import settings
from batchclass import batch
from cycleclass import currentcycle


class UiSimpleBatch(QDialog, Ui_dialogSimpleBatch):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(settings['simplebatchform']['x'], settings['simplebatchform']['y'])
        self.recordnumber = -1

    def startup(self):
        self.comboTask1.activated.connect(lambda: self.taskcomboclick(1))
        self.comboTask2.activated.connect(lambda: self.taskcomboclick(2))
        self.comboTask3.activated.connect(lambda: self.taskcomboclick(3))
        self.comboTask4.activated.connect(lambda: self.taskcomboclick(4))
        self.comboTask5.activated.connect(lambda: self.taskcomboclick(5))
        self.btnSave.clicked.connect(self.savechecks)
        self.btnClose.clicked.connect(self.formclose)
        self.comboTask1.addItems(currentcycle.cycles)
        self.comboTask2.addItems(currentcycle.cycles)
        self.comboTask3.addItems(currentcycle.cycles)
        self.comboTask4.addItems(currentcycle.cycles)
        self.comboTask5.addItems(currentcycle.cycles)
        self.comboLocation1.addItems(currentcycle.locations)
        self.comboLocation2.addItems(currentcycle.locations)
        self.comboLocation3.addItems(currentcycle.locations)
        self.comboLocation4.addItems(currentcycle.locations)
        self.comboLocation5.addItems(currentcycle.locations)
        self.lineDescription.setText(batch.description)
        self.lineDate.setText(batch.date)
        if len(batch.runnumber) > 4:
            self.comboTask5.setCurrentText(batch.cycle[4])
            self.comboLocation5.setCurrentText(batch.location[4])
            self.lineSample5.setText(batch.identifier[4])
        if len(batch.runnumber) > 3:
            self.comboTask4.setCurrentText(batch.cycle[3])
            self.comboLocation4.setCurrentText(batch.location[3])
            self.lineSample4.setText(batch.identifier[3])
        if len(batch.runnumber) > 2:
            self.comboTask3.setCurrentText(batch.cycle[2])
            self.comboLocation3.setCurrentText(batch.location[2])
            self.lineSample3.setText(batch.identifier[2])
        if len(batch.runnumber) > 1:
            self.comboTask2.setCurrentText(batch.cycle[1])
            self.comboLocation2.setCurrentText(batch.location[1])
            self.lineSample2.setText(batch.identifier[1])
        if len(batch.runnumber) > 0:
            self.comboTask1.setCurrentText(batch.cycle[0])
            self.comboLocation1.setCurrentText(batch.location[0])
            self.lineSample1.setText(batch.identifier[0])
            self.lineDate.setText(batch.date)
            self.lineDescription.setText(batch.description)
            self.setWindowTitle('Unfinished steps from batch # %i' % batch.id)
            for i in range(1, 6):
                self.taskcomboclick(i)

    def formclose(self):
        settings['simplebatchform']['x'] = self.x()
        settings['simplebatchform']['y'] = self.y()
        self.deleteLater()

    def taskcomboclick(self, index):
        if index == 1:
            if self.comboTask1.currentText() == 'End':
                self.comboTask2.setCurrentIndex(0)
                self.comboTask2.setEnabled(False)
                self.btnSave.setEnabled(False)
                self.taskcomboclick(2)
            else:
                self.comboTask2.setEnabled(True)
                self.btnSave.setEnabled(True)
            if self.comboTask1.currentText() >= 'Sample':
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
            if self.comboTask2.currentText() >= 'Sample':
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
            if self.comboTask3.currentText() >= 'Sample':
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
            if self.comboTask4.currentText() >= 'Sample':
                self.comboLocation4.setEnabled(True)
                self.lineSample4.setEnabled(True)
            else:
                self.comboLocation4.setEnabled(False)
                self.lineSample4.setEnabled(False)
        elif index == 5:
            if self.comboTask5.currentText() >= 'Sample':
                self.comboLocation5.setEnabled(True)
                self.lineSample5.setEnabled(True)
            else:
                self.comboLocation5.setEnabled(False)
                self.lineSample5.setEnabled(False)

    def savechecks(self):
        try:
            taskbatch = [[self.comboTask1.currentText(), self.comboLocation1.currentText(), self.lineSample1.text()],
                         [self.comboTask2.currentText(), self.comboLocation2.currentText(), self.lineSample2.text()],
                         [self.comboTask3.currentText(), self.comboLocation3.currentText(), self.lineSample3.text()],
                         [self.comboTask4.currentText(), self.comboLocation4.currentText(), self.lineSample4.text()],
                         [self.comboTask5.currentText(), self.comboLocation5.currentText(), self.lineSample5.text()]]
            errormessage = []
            if len(self.lineDescription.text()) == 0:
                errormessage.append('There is no decription for this batch')
            for index, task in enumerate(taskbatch):
                if task[0][:6] != 'Sample':
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
                    print(index, len(batch.runnumber))
                    if index < len(batch.runnumber):
                        if task[0] == 'End':
                            print('mark as end')
                            batch.status[index] = 2
                        else:
                            print('update existing')
                            batch.cycle[index] = task[0]
                            batch.location[index] = task[1]
                            batch.identifier[index] = task[2]
                    else:
                        if task[0] != 'End':
                            print('adnew')
                            batch.addstep(task[0], task[1], task[2])
                    index = index + 1
                batch.save()
                self.deleteLater()
        except:
            print('Simple form save error')

#  app = QApplication(sys.argv)
#  dialog = UiSimpleBatch()
#  dialog.startup()
#  dialog.show()
#  sys.exit(app.exec_())
