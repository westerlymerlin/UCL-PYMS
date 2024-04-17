"""
UI form for viewing the logs
"""
from PySide6.QtWidgets import QDialog, QApplication
from logmanager import logger
from ui.ui_layout_log_viewer import Ui_LogDialog
from app_control import settings


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
        logger.debug('Reading the log file %s', logfilepath)
        with open(logfilepath, 'r', encoding='utf-8') as f:
            log = f.readlines()
        f.close()
        logger.debug('File read %s lines', len(log))
        self.txtLog.clear()

        for logline in log:
            colour = '#75af02'
            if 'ERROR' in logline:
                colour = '#c70000'
            elif 'WARN' in logline:
                colour = '#f69003'
            elif 'DEBUG' in logline:
                colour = '#C0C0C0'
            self.txtLog.insertHtml('<span style=" color:%s;">%s<br></span>' % (colour, logline))

    def formclose(self):
        """Close event for the form"""
        self.deleteLater()


if __name__ == "__main__":
    app = QApplication([])
    log_viewer = UiLogViewer()
    log_viewer.show()
    log_viewer.loadlog()
    app.exec()
