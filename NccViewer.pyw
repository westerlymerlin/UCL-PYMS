"""
NCC Viewer - Standalone application for viewing and calculating Noble gas Correction Coefficients.

This module serves as the main entry point for the NCC Viewer application, a PySide6-based
GUI tool that allows users to process helium isotope measurement data and calculate
correction coefficients for noble gas mass spectrometry analysis.

The application provides functionality to:
- Load and process helium measurement data files
- Calculate blank corrections and NCC values
- Display results in a user-friendly interface
- Export calculated coefficients for use in data analysis

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
