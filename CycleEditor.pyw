from PySide6.QtWidgets import QApplication
from ui.cycleeditUI import CycleEditUI
import sys

app = QApplication(sys.argv)
mainform = CycleEditUI()
mainform.show()

sys.exit(app.exec())