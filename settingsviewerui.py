from PySide6.QtWidgets import *
from ui_logviewer import Ui_LogDialog


class UiSettingsViewer(QDialog, Ui_LogDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnClose.clicked.connect(self.formclose)
        self.btnReload.setVisible(False)
        self.label.setText('PyMS Settings File')

    def loadfile(self):
        filepath = 'settings.json'
        with open(filepath, 'r') as f:
            log = f.readlines()
        f.close()
        self.txtLog.clear()
        for logline in log:
            self.txtLog.insertPlainText(logline)

    def formclose(self):
        self.deleteLater()
