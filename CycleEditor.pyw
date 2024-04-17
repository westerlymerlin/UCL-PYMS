"""
Cycle Editor Application
Author: Gary Twinn
"""
import sys
from PySide6.QtWidgets import QApplication
from app_control import VERSION
from logmanager import logger
from ui.cycle_edit_form import CycleEditUI

logger.info('****** Cycle editer version %s started ******', VERSION)
app = QApplication(sys.argv)
mainform = CycleEditUI()
mainform.show()

sys.exit(app.exec())
