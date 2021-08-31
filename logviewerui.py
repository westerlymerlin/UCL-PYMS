from PySide2.QtWidgets import *
from ui_logviewer import Ui_LogDialog
from settings import settings


class UiLogViewer(QDialog, Ui_LogDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnClose.clicked.connect(self.formclose)
        self.btnReload.clicked.connect(self.loadlog)
        self.label.setText('PyMS Log File')

    def loadlog(self):
        logfilepath = '%s%s.log' %(settings['logging']['logfilepath'],settings['logging']['logappname'])
        with open(logfilepath, 'r') as f:
            log = f.readlines()
        f.close()
        self.txtLog.clear()
        for logline in log:
            self.txtLog.insertPlainText(logline)

    def formclose(self):
        self.deleteLater()
