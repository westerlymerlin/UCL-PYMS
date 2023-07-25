from PySide6.QtWidgets import *
from ui.ui_cycleedit import Ui_dialogCycleEdit
from settings import settings, writesettings
import sqlite3
import sys


def listkey(item):
    return item[1]


class CycleEditUI(QDialog, Ui_dialogCycleEdit):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(settings['cycleeditform']['x'], settings['cycleeditform']['y'])
        self.btnClose.clicked.connect(self.formclose)
        self.tableSteps.clicked.connect(self.rowselect)
        self.cycleids = []
        self.currentid = 0
        self.cyclenames = []
        self.cycledescriptions = []
        self.cycleenableds = []
        self.cyclelaserpowers = []
        self.cycleissamples = []
        self.loadcycles()
        self.cycle = []
        self.comboCycles.activated.connect(self.combochange)
        self.comboTarget.activated.connect(lambda: self.commandselector(self.comboTarget.currentText()))
        self.btnSaveSteps.clicked.connect(self.save_steps_button_clicked)
        self.btnSaveCycle.clicked.connect(self.save_cycle_button_clicked)
        self.btnDuplicate.clicked.connect(self.duplicate_cycle_button_clicked)
        self.btnAdd.clicked.connect(self.add_button_clicked)
        self.btnRevert.clicked.connect(self.revert_button_clicked)
        self.btnDelete.clicked.connect(self.delete_button_clicked)
        self.btnUpdate.clicked.connect(self.update_button_clicked)
        self.chkSample.clicked.connect(self.sample_check)
        self.tableSteps.setColumnWidth(0, 127)
        self.tableSteps.setColumnWidth(1, 190)
        self.tableSteps.setColumnWidth(2, 190)
        database = sqlite3.connect(settings['database']['databasepath'])
        cursorobj = database.cursor()
        sql_query = 'SELECT distinct target from cyclesteps order by target'
        cursorobj.execute(sql_query)
        returnobjects = cursorobj.fetchall()
        for target in returnobjects:
            self.comboTarget.addItems(target)
        database.close()
        self.txtLaserPower.editingFinished.connect(self.laserchange)
        self.combochange()

    def formclose(self):
        settings['cycleeditform']['x'] = self.x()
        settings['cycleeditform']['y'] = self.y()
        writesettings()
        self.deleteLater()

    def loadcycles(self):
        initvalue = self.comboCycles.currentText()
        self.cycleids = []
        self.currentid = 0
        self.cyclenames = []
        self.cycledescriptions = []
        self.cycleenableds = []
        self.cyclelaserpowers = []
        self.cycleissamples = []
        self.cycle = []
        self.comboCycles.clear()
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = 'SELECT id, name, description, laserpower, enabled, issample from cycles'
        cursor_obj.execute(sql_query)
        returnobjects = cursor_obj.fetchall()
        for cycle in returnobjects:
            self.cycleids.append(cycle[0])
            self.cyclenames.append(cycle[1])
            self.cycledescriptions.append(cycle[2])
            self.cyclelaserpowers.append(cycle[3])
            self.cycleenableds.append(cycle[4])
            self.cycleissamples.append(cycle[5])
        database.close()
        self.comboCycles.addItems(self.cyclenames)
        self.comboCycles.setCurrentText(initvalue)
        self.combochange()

    def combochange(self):
        self.currentid = self.comboCycles.currentIndex() + 1
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = 'SELECT * from cyclesteps WHERE id  = %s' % self.currentid
        # print(sql_query)
        cursor_obj.execute(sql_query)
        self.cycle = cursor_obj.fetchall()
        self.txtDescription.setPlainText(self.cycledescriptions[self.comboCycles.currentIndex()])
        self.chkEnabled.setChecked(self.cycleenableds[self.comboCycles.currentIndex()])
        self.chkSample.setChecked(self.cycleissamples[self.comboCycles.currentIndex()])
        self.sample_check()
        self.refreshtable()
        self.rowselect()
        database.close()

    def sample_check(self):
        if self.chkSample.isChecked():
            self.txtLaserPower.setText('%.1f' % self.cyclelaserpowers[self.comboCycles.currentIndex()])
            self.txtLaserPower.setEnabled(True)
        else:
            self.txtLaserPower.setText('0.0')
            self.txtLaserPower.setEnabled(False)

    def laserchange(self):
        try:
            laservalue = float(self.txtLaserPower.text())
            if laservalue > 99.9 or laservalue < 0:
                self.sample_check()
                return
            self.txtLaserPower.setText('%.1f' % round(laservalue, 1))
        except ValueError:
            self.sample_check()


    def refreshtable(self):
        self.tableSteps.setRowCount(0)
        for row in self.cycle:
            x = self.tableSteps.rowCount()
            self.tableSteps.insertRow(x)
            newtime_item = QTableWidgetItem(str(row[1]))
            newtarget_item = QTableWidgetItem(row[2])
            newcommand_item = QTableWidgetItem(row[3])
            self.tableSteps.setItem(x, 0, newtime_item)
            self.tableSteps.setItem(x, 1, newtarget_item)
            self.tableSteps.setItem(x, 2, newcommand_item)
        self.tableSteps.selectRow(0)

    def rowselect(self):
        self.textTime.setText(self.tableSteps.item(self.tableSteps.currentRow(), 0).text())
        target = self.tableSteps.item(self.tableSteps.currentRow(), 1).text()
        command = self.tableSteps.item(self.tableSteps.currentRow(), 2).text()
        self.commandselector(target)
        self.comboTarget.setCurrentText(target)
        self.comboCommand.setCurrentText(command)

    def add_button_clicked(self):
        for row in self.cycle:
            if row[1] == int(self.textTime.text()):
                QMessageBox.warning(self, "Error", "You cannot have two commands at the same time \n"
                                                   "you were specifying the %s second time slot. \n"
                                                   "Please choose another time slot, this edit has not been saved."
                                    % row[1])
                return
        self.cycle.append((int(self.currentid), int(self.textTime.text()), self.comboTarget.currentText(),
                           self.comboCommand.currentText()))
        self.cycle = sorted(self.cycle, key=listkey)
        self.refreshtable()

    def update_button_clicked(self):
        if self.cycle[self.tableSteps.currentRow()][1] != int(self.textTime.text()):
            for row in self.cycle:
                if row[1] == int(self.textTime.text()):
                    QMessageBox.warning(self, "Error", "You cannot have two commands at the same time \n"
                                                       "you were specifying the %s second time slot. \n"
                                                       "Please choose another time slot, this edit has not been saved."
                                        % row[1])
                    return
        self.cycle[self.tableSteps.currentRow()] = (int(self.currentid), int(self.textTime.text()),
                                                    self.comboTarget.currentText(), self.comboCommand.currentText())
        self.cycle = sorted(self.cycle, key=listkey)
        self.refreshtable()

    def delete_button_clicked(self):
        self.cycle.pop(self.tableSteps.currentRow())
        self.refreshtable()

    def save_steps_button_clicked(self):
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = 'DELETE from cyclesteps WHERE id  = %' % self.currentid
        cursor_obj.execute(sql_query)
        sql_query = 'INSERT into cyclesteps (id, time, target, command) VALUES (?, ?, ?, ?)'
        for row in self.cycle:
            # print(row)
            cursor_obj.execute(sql_query, row)
        database.commit()
        cursor_obj.execute('VACUUM')
        database.close()

    def save_cycle_button_clicked(self):
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = 'UPDATE cycles Set description = ?, laserpower = ?, enabled = ?, issample = ? WHERE id = ?'
        datarow = (self.txtDescription.toPlainText(), float(self.txtLaserPower.text()), self.chkEnabled.isChecked(), self.chkSample.isChecked(), self.currentid)
        print(datarow)
        cursor_obj.execute(sql_query, datarow)
        database.commit()
        database.close()
        self.loadcycles()

    def duplicate_cycle_button_clicked(self):
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = 'INSERT into cycles (name, description, laserpower, enabled, issample) VALUES (?, ?, ?, ?, ?)'
        newcycle = QInputDialog.getText(self, 'Create a new cycle', 'Enter a new meaningful name for the new cycle', QLineEdit.Normal, self.comboCycles.currentText() + ' (copy)' )
        if not newcycle[0]:
            return
        for cycle in self.cyclenames:
            if newcycle[0].strip() == cycle:
                return
        datarow = (newcycle[0], 'Enter a new description', float(self.txtLaserPower.text()), self.chkEnabled.isChecked(), self.chkSample.isChecked())
        cursor_obj.execute(sql_query, datarow)
        newid = cursor_obj.lastrowid
        database.commit()
        sql_query = 'INSERT into cyclesteps (id, time, target, command) VALUES (?, ?, ?, ?)'
        for row in self.cycle:
            datarow = (newid, row[1], row[2], row[3])
            cursor_obj.execute(sql_query, datarow)
        database.commit()
        database.close()
        self.loadcycles()


    def revert_button_clicked(self):
        self.combochange()

    def commandselector(self, target):
        self.comboCommand.clear()
        if target[:5] == 'valve':
            self.comboCommand.addItems(['open', 'close'])
        elif target[:7] == 'pipette':
            self.comboCommand.addItems(['load', 'unload', 'close'])
        elif target[:5] == 'laser':
            if self.chkSample.isChecked():
                self.comboCommand.addItems(['on', 'off', 'setpower', 'checkalarms'])
            else:
                self.comboCommand.addItems(['checkalarms'])
        elif target[:4] == 'quad':
            self.comboCommand.addItems(['starttimer', 'starttimer-reheat', 'writefile', 'hiden-startmid',
                                        'hiden-startprofile', 'hiden-stop'])
        elif target[:7] == 'xytable':
            self.comboCommand.addItems(['move'])
        elif target[:5] == 'image':
            self.comboCommand.addItems(['dynolite', 'microscope', 'microscope-reheat', 'hiden-mid', 'hiden-mid-reheat',
                                        'hiden-profile'])
        elif target[:9] == 'pyrometer':
            self.comboCommand.addItems(['read'])
        elif target[:3] == 'end':
            self.comboCommand.addItems(['end'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = CycleEditUI()
    dialog.show()
    sys.exit(app.exec())
