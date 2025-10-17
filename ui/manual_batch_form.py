"""
Dialog for a Manual batch (used for testing the Helium line) has a default of 8 steps but more can be added
Author: Gary Twinn
"""
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QDialog, QApplication, QTableWidgetItem, QComboBox, QLineEdit
from ui.ui_layout_manual_batch import Ui_dialogManualBatch
from app_control import settings, writesettings
from batchclass import batch
from cycleclass import currentcycle
from logmanager import logger


class UiManualBatch(QDialog, Ui_dialogManualBatch):
    """Dialog Class"""
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(settings['manualbatchform']['x'], settings['manualbatchform']['y'])

    def startup(self):
        """Initialise the form, if new set to blank but if the batch exists
         populate sample names into the relevant locations"""
        self.btnSave.clicked.connect(self.savechecks)
        self.btnClose.clicked.connect(self.formclose)
        self.btnAddRows.clicked.connect(lambda: self.add_row(self.spinAddRows.value()))
        font1 = QFont()
        font1.setFamilies(['Segoe UI'])
        font1.setPointSize(10)
        font1.setBold(True)
        column_0_header = QTableWidgetItem()
        column_0_header.setTextAlignment(Qt.AlignLeading | Qt.AlignVCenter)
        column_0_header.setFont(font1)
        column_0_header.setText('Cycle')
        column_1_header = QTableWidgetItem()
        column_1_header.setTextAlignment(Qt.AlignLeading | Qt.AlignVCenter)
        column_1_header.setFont(font1)
        column_1_header.setText('Location')
        column_2_header = QTableWidgetItem('Sample Description')
        column_2_header.setTextAlignment(Qt.AlignLeading | Qt.AlignVCenter)
        column_2_header.setFont(font1)
        self.tableBatchList.setColumnCount(3)
        self.tableBatchList.setRowCount(0)
        self.tableBatchList.verticalHeader().setVisible(True)
        self.tableBatchList.horizontalHeader().setVisible(True)
        self.tableBatchList.setHorizontalHeaderItem(0, column_0_header)
        self.tableBatchList.setHorizontalHeaderItem(1, column_1_header)
        self.tableBatchList.setHorizontalHeaderItem(2, column_2_header)
        self.tableBatchList.setColumnWidth(0, 200)
        self.tableBatchList.setColumnWidth(1, 100)
        self.tableBatchList.setColumnWidth(2, 450)
        self.add_row(max(8, len(batch.runnumber) + 1))
        self.load_batch_data()


    def add_row(self, rows_to_add):
        """
        Adds a specified number of rows to the table, each containing widgets for selecting cycles
        and locations, as well as a description field. The rows are initialized with default cycle
        and location choices, and style settings are applied.
        """
        cycle_list = currentcycle.cycles
        location_list = currentcycle.locations
        row_cycle_list = []
        row_location_list = []
        row_description_list = []
        for _ in range(rows_to_add):
            row_cycle_list.append(QComboBox())
            row_cycle_list[-1].addItems(cycle_list)
            row_cycle_list[-1].activated.connect(self.task_combo_click)
            row_cycle_list[-1].setStyleSheet('background-color: rgba(255, 255, 255, 0);')
            row_location_list.append(QComboBox())
            row_location_list[-1].addItems(location_list)
            row_location_list[-1].setEnabled(False)
            row_location_list[-1].setStyleSheet('background-color: rgba(255, 255, 255, 0);')
            row_description_list.append(QLineEdit())
            row_description_list[-1].setEnabled(False)
            row_description_list[-1].setStyleSheet('background-color: rgba(255, 255, 255, 0);')
            self.tableBatchList.insertRow(self.tableBatchList.rowCount())
            self.tableBatchList.setCellWidget(self.tableBatchList.rowCount()-1, 0, row_cycle_list[-1])
            self.tableBatchList.setCellWidget(self.tableBatchList.rowCount()-1, 1, row_location_list[-1])
            self.tableBatchList.setCellWidget(self.tableBatchList.rowCount()-1, 2, row_description_list[-1])


    def load_batch_data(self):
        """if new set to blank but if the batch exists populate sample names into the relevant locations"""
        if len(batch.runnumber) >0:
            self.lineDescription.setText(batch.description)
            self.lineDate.setText(batch.date)
            for i in range(len(batch.runnumber)):
                self.tableBatchList.cellWidget(i, 0).setCurrentText(batch.cycle[i])
                self.tableBatchList.cellWidget(i, 1).setCurrentText(batch.location[i])
                self.tableBatchList.cellWidget(i, 2).setText(batch.identifier[i])
                if currentcycle.sample(batch.cycle[i]):
                    self.tableBatchList.cellWidget(i, 1).setEnabled(True)
                    self.tableBatchList.cellWidget(i, 2).setEnabled(True)


    def task_combo_click(self):
        """Cycle type Combo box handler, enables the location and description if the task
         is a sample based one (needs the laser)"""
        row = self.tableBatchList.currentRow()
        column = self.tableBatchList.currentColumn()
        value = self.tableBatchList.cellWidget(row, column).currentText()
        if currentcycle.sample(value):
            self.tableBatchList.cellWidget(row, 1).setEnabled(True)
            self.tableBatchList.cellWidget(row, 2).setEnabled(True)
        else:
            self.tableBatchList.cellWidget(row, 1).setEnabled(False)
            self.tableBatchList.cellWidget(row, 2).setEnabled(False)

    def formclose(self):
        """Form close handler"""
        settings['manualbatchform']['x'] = self.x()
        settings['manualbatchform']['y'] = self.y()
        writesettings()
        self.deleteLater()



    def savechecks(self):
        """Tests to run before saving to ensure every sample has a valid name"""
        try:
            taskbatch = []
            for row in range(self.tableBatchList.rowCount()):
                if self.tableBatchList.cellWidget(row, 0).currentText() != 'End':
                    taskbatch.append([self.tableBatchList.cellWidget(row, 0).currentText(),
                                  self.tableBatchList.cellWidget(row, 1).currentText(),
                                  self.tableBatchList.cellWidget(row, 2).text()])
            errormessage = []
            if len(self.lineDescription.text()) == 0:
                errormessage.append('There is no description for this batch')
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
                    logger.debug('Manual Batch save: %s %s', index, len(batch.runnumber))
                    if index < len(batch.runnumber):
                        if task[0] == 'End':
                            logger.debug('Manual Batch save: mark as end')
                            batch.status[index] = 2
                        else:
                            logger.debug('Manual Batch save: update existing')
                            batch.cycle[index] = task[0]
                            batch.location[index] = task[1]
                            batch.identifier[index] = task[2]
                    else:
                        if task[0] != 'End':
                            logger.debug('Manual Batch save: addnew')
                            batch.addstep(task[0], task[1], task[2])
                    index = index + 1
                batch.save()
                self.deleteLater()
        except:
            logger.error('Manual Batch save: save error')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = UiManualBatch()
    dialog.startup()
    dialog.show()
    sys.exit(app.exec())
