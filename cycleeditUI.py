from PySide6.QtWidgets import *
from ui_cycleedit import Ui_dialogCycleEdit
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
        self.loadcycles()
        self.cycle = []
        self.comboCycles.activated.connect(self.combochange)
        self.comboTarget.activated.connect(lambda: self.commandselector(self.comboTarget.currentText()))
        self.buttonSave.clicked.connect(self.save_button_clicked)
        self.buttonAdd.clicked.connect(self.add_button_clicked)
        self.buttonCancel.clicked.connect(self.cancel_button_clicked)
        self.buttonDelete.clicked.connect(self.delete_button_clicked)
        self.buttonUpdate.clicked.connect(self.update_button_clicked)
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
        self.combochange()

    def formclose(self):
        settings['cycleeditform']['x'] = self.x()
        settings['cycleeditform']['y'] = self.y()
        writesettings()
        self.deleteLater()

    def loadcycles(self):
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = 'SELECT id, name, description from cycles WHERE enabled = 1'
        cursor_obj.execute(sql_query)
        returnobjects = cursor_obj.fetchall()
        for cycle in returnobjects:
            self.cycleids.append(cycle[0])
            self.cyclenames.append(cycle[1])
            self.cycledescriptions.append(cycle[2])
        database.close()
        self.comboCycles.addItems(self.cyclenames)
        self.combochange()

    def combochange(self):
        self.currentid = '%s' % (self.comboCycles.currentIndex() + 1)
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = """SELECT * from cyclesteps WHERE id  = ?"""
        cursor_obj.execute(sql_query, self.currentid)
        self.cycle = cursor_obj.fetchall()
        self.lbl_description.setText(self.cycledescriptions[self.comboCycles.currentIndex()])
        self.refreshtable()
        self.rowselect()

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

    def save_button_clicked(self):
        database = sqlite3.connect(settings['database']['databasepath'])
        cursor_obj = database.cursor()
        sql_query = """DELETE from cyclesteps WHERE id  = ?"""
        cursor_obj.execute(sql_query, self.currentid)
        sql_query = """INSERT into cyclesteps (id, time, target, command) VALUES (?, ?, ?, ?)"""
        for row in self.cycle:
            print(row)
            cursor_obj.execute(sql_query, row)
        database.commit()
        cursor_obj.execute("""VACUUM""")

    def cancel_button_clicked(self):
        self.combochange()

    def commandselector(self, target):
        self.comboCommand.clear()
        if target[:5] == 'valve':
            self.comboCommand.addItems(['open', 'close'])
        elif target[:7] == 'pipette':
            self.comboCommand.addItems(['load', 'unload', 'close'])
        elif target[:5] == 'laser':
            self.comboCommand.addItems(['on', 'off', 'setpower', 'checkalarms'])
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
    sys.exit(app.exec_())
