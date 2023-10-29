"""
UI form for viewing the logs
"""
from PySide6.QtWidgets import QDialog
from ui.ui_layout_log_viewer import Ui_LogDialog
from settings import settings


class UiLogViewer(QDialog, Ui_LogDialog):
    """Log viewer class"""
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnClose.clicked.connect(self.formclose)
        self.btnReload.clicked.connect(self.loadlog)
        self.label.setText('PyMS Log File')

    def loadlog(self):
        """Read the application log and format it"""
        logfilepath = '%s%s.log' %(settings['logging']['logfilepath'],settings['logging']['logappname'])
        with open(logfilepath, 'r', encoding='utf-8') as f:
            log = f.readlines()
        f.close()
        self.txtLog.clear()
        for logline in log:
            colour = '#75af02'
            if 'ERROR' in logline:
                colour = '#c70000'
            elif 'WARN' in logline:
                colour = '#f69003'
            elif 'DEBUG' in logline:
                colour = '#C0C0C0'
            self.txtLog.insertHtml(f'<span style=" color:{colour};">{logline}<br></span>')

    def formclose(self):
        """Close event for the form"""
        self.deleteLater()
