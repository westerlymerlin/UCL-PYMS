"""
NCC Viwer application
Author: Gary Twinn
"""
import sys
from PySide6.QtWidgets import QApplication
from logmanager import logger
from app_control import VERSION
from ui.ncc_calc_form import NccCalcUI

logger.info('****** Ncc Viewer version %s started ******', VERSION)
app = QApplication(sys.argv)
mainform = NccCalcUI()
mainform.show()

sys.exit(app.exec())
