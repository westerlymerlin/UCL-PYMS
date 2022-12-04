from PySide6.QtWidgets import QApplication
from logmanager import *
from settings import setrunning
from mainUIForm import UiMain

setrunning(True)
app = QApplication(sys.argv)
mainform = UiMain()
mainform.show()

sys.exit(app.exec())
