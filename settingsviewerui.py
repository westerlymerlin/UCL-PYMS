from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from ui_logviewer import Ui_LogDialog
from settings import settings, writesettings
import sys


class UiSettingsViewer(QDialog, Ui_LogDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnClose.clicked.connect(self.formclose)
        self.btnReload.setVisible(False)
        self.txtLog.setVisible(False)
        self.label.setText('PyMS Settings File')
        self.settingstable = QTableWidget(self)
        self.settingstable.setGeometry(10, 50, 1181, 891)
        self.settingstable.setColumnCount(2)
        self.settingstable.setColumnWidth(0, 300)
        self.settingstable.setColumnWidth(1, 859)
        self.settingstable.setEditTriggers(QAbstractItemView.CurrentChanged)
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(10)
        font1.setBold(True)
        newitem = QTableWidgetItem('Setting')
        newitem.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter)
        newitem.setFont(font1)
        self.settingstable.setHorizontalHeaderItem(0, newitem)
        self.settingstable.verticalHeader().setVisible(False)
        newvalue = QTableWidgetItem('Value')
        newvalue.setTextAlignment(Qt.AlignLeading | Qt.AlignVCenter)
        newvalue.setFont(font1)
        self.settingstable.setHorizontalHeaderItem(1, newvalue)
        self.settingstable.setAlternatingRowColors(True)
        self.settingstable.itemChanged.connect(self.settingchanged)
        self.loading = 1
        self.changed = 0


    def loadsettings(self):
        for item in settings.keys():
            if type(settings[item]) == dict:
                for subitem in settings[item]:
                    if type(settings[item][subitem]) == dict:
                        for subsubitem in settings[item][subitem]:
                            row = self.settingstable.rowCount()
                            self.settingstable.insertRow(row)
                            newitem = QTableWidgetItem('%s,    %s,    %s' % (item, subitem, subsubitem))
                            newitem.setFlags(Qt.ItemIsEnabled)
                            newvalue = QTableWidgetItem('%s' % settings[item][subitem][subsubitem])
                            self.settingstable.setItem(row, 0, newitem)
                            self.settingstable.setItem(row, 1, newvalue)
                    else:
                        row = self.settingstable.rowCount()
                        self.settingstable.insertRow(row)
                        newitem = QTableWidgetItem('%s,    %s' % (item, subitem))
                        newitem.setFlags(Qt.ItemIsEnabled)
                        newvalue = QTableWidgetItem('%s' % settings[item][subitem])
                        self.settingstable.setItem(row, 0, newitem)
                        self.settingstable.setItem(row, 1, newvalue)
            else:
                row = self.settingstable.rowCount()
                self.settingstable.insertRow(row)
                newitem = QTableWidgetItem('%s' % item)
                newitem.setFlags(Qt.ItemIsEnabled)
                newvalue = QTableWidgetItem('%s' % settings[item])
                if item == 'LastSave':
                    newvalue.setFlags(Qt.ItemIsEnabled)
                self.settingstable.setItem(row, 0, newitem)
                self.settingstable.setItem(row, 1, newvalue)
        self.loading = 0


    def settingchanged(self, cell):
        if self.loading == 0:
            settings_ref = self.settingstable.item(cell.row(), 0).text().split(',    ')
            oldval = ''
            newval = cell.data(Qt.EditRole)
            try:
                if len(settings_ref) == 3:
                    oldval = settings[settings_ref[0]][settings_ref[1]][settings_ref[2]]
                    if type(oldval) == float:
                        settings[settings_ref[0]][settings_ref[1]][settings_ref[2]] = float(newval)
                    elif type(oldval) == int:
                        settings[settings_ref[0]][settings_ref[1]][settings_ref[2]] = int(newval)
                    else:
                        settings[settings_ref[0]][settings_ref[1]][settings_ref[2]] = newval
                if len(settings_ref) == 2:
                    oldval = settings[settings_ref[0]][settings_ref[1]]
                    if type(oldval) == float:
                        settings[settings_ref[0]][settings_ref[1]] = float(newval)
                    elif type(oldval) == int:
                        settings[settings_ref[0]][settings_ref[1]] = int(newval)
                    else:
                        settings[settings_ref[0]][settings_ref[1]] = newval
                if len(settings_ref) == 1:
                    oldval = settings[settings_ref[0]]
                    if type(oldval) == float:
                        settings[settings_ref[0]] = float(newval)
                    elif type(oldval) == int:
                        settings[settings_ref[0]] = int(newval)
                    else:
                        settings[settings_ref[0]] = newval
                writesettings()
                print('Manual Settings Update %s, %s from %s to %s' % (settings_ref, type(oldval), oldval, newval))
            except ValueError:
                print('Manual Settings Update Fail %s, %s from %s to %s' % (settings_ref, type(oldval), oldval, newval))

    def formclose(self):
        self.deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = UiSettingsViewer()
    dialog.loadsettings()
    dialog.show()
    sys.exit(app.exec())
