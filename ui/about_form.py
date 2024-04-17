"""
About Dialog
"""
from datetime import datetime
from PySide6.QtWidgets import QDialog, QMainWindow
from ui.ui_layout_about import Ui_AboutDialog
from app_control import VERSION


class UiAbout(QDialog, QMainWindow, Ui_AboutDialog):
    """
    A class representing the About Dialog UI.

    Inherits from QDialog, QMainWindow, and Ui_AboutDialog.

    Methods:
        __init__()

    Attributes:
        None
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        htmltxt = self.txtAbout.toHtml()
        htmltxt = htmltxt.replace('xxxxx', VERSION)
        htmltxt = htmltxt.replace('yyyy', datetime.now().strftime('%Y'))
        self.txtAbout.setHtml(htmltxt)
