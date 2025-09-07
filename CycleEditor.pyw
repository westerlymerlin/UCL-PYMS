
"""
CycleEditor - Measurement Cycle Configuration Tool

This is a standalone utility application for configuring and editing measurement cycles
used by the PyMS (Python Mass Spectrometry Control System). The CycleEditor provides
a dedicated interface for:

- Creating and modifying measurement cycle definitions
- Configuring cycle parameters and sequences
- Managing cycle templates and presets
- Testing and validating cycle configurations
- Importing/exporting cycle definitions

The application uses PySide6 (Qt) for the GUI framework and integrates with the PyMS
system's cycle management infrastructure. This tool allows users to prepare measurement
cycles independently of the main PyMS control interface, enabling better workflow
separation and cycle preparation.

Usage: Run this application to open the cycle editing interface when measurement
cycles need to be created or modified outside of the main PyMS control session.

Author: Gary Twinn
"""
import sys
from PySide6.QtWidgets import QApplication
from app_control import VERSION
from logmanager import logger
from ui.cycle_edit_form import CycleEditUI

logger.info('****** Cycle editor version %s started ******', VERSION)
app = QApplication(sys.argv)
mainform = CycleEditUI()
mainform.show()

sys.exit(app.exec())
