"""
PyMS Application
Author: Gary Twinn
"""
import sys
from PySide6.QtWidgets import QApplication
from logmanager import logger
from app_control import setrunning, VERSION
from ui.main_form import UiMain

logger.info('****** PyMS version %s started ******', VERSION)
setrunning(True)
app = QApplication(sys.argv)
mainform = UiMain()
mainform.show()

sys.exit(app.exec())
