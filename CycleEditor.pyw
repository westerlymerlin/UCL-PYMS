"""
Cycle Editor Application
Author: Gary Twinn
"""
from PySide6.QtWidgets import QApplication
from ui.cycle_edit_form import CycleEditUI
import sys

app = QApplication(sys.argv)
mainform = CycleEditUI()
mainform.show()

sys.exit(app.exec())