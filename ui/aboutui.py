from PySide6.QtWidgets import *
from ui.ui_about import Ui_AboutDialog
from settings import version


class UiAbout(QDialog, QMainWindow, Ui_AboutDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        htmltxt = self.txtAbout.toHtml()
        htmltxt = htmltxt.replace('xxxxx', version)
        self.txtAbout.setHtml(htmltxt)
