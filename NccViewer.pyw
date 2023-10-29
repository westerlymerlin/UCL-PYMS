"""
NCC Viwer application
Author: Gary Twinn
"""
import sys
from PySide6.QtWidgets import QApplication
from ui.ncc_calc_form import NccCalcUI

app = QApplication(sys.argv)
mainform = NccCalcUI()
mainform.show()

sys.exit(app.exec())
