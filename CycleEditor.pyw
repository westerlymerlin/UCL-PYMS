"""
Cycle Editor Application
Author: Gary Twinn
"""
import sys
from PySide6.QtWidgets import QApplication
from ui.cycle_edit_form import CycleEditUI

app = QApplication(sys.argv)
mainform = CycleEditUI()
mainform.show()

sys.exit(app.exec())