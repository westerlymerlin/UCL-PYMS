from PySide2.QtWidgets import QApplication
from logmanager import *
from settings import version, setrunning
from mainUIForm import UiMain

print("Starting PyMs Version %s" % version)
setrunning(True)
app = QApplication(sys.argv)
mainform = UiMain()
mainform.show()

sys.exit(app.exec_())
