from PySide6.QtWidgets import QApplication
from ui.nccCalcUI import NccCalcUI
import sys

app = QApplication(sys.argv)
mainform = NccCalcUI()
mainform.show()

sys.exit(app.exec())