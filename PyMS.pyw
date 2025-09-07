"""
PyMS - Python Mass Spectrometry Control System

This is the main entry point for the PyMS application, a comprehensive control system
for mass spectrometry operations. The application provides a GUI interface for:

- Batch processing and sample management
- Laser control (Helium line laser)
- XY positioning and movement control
- Valve and pump monitoring
- Mass spectrometer operations
- Real-time status monitoring and logging

The application uses PySide6 (Qt) for the GUI framework and includes modules for:
- Hardware communication and control
- Database operations for sample tracking
- Automated measurement cycles
- Manual control interfaces
- Data logging and visualization

Author: Gary Twinn
"""
import sys
from PySide6.QtWidgets import QApplication
from logmanager import logger
from app_control import setrunning, VERSION
from ui.main_form import UiMain

logger.info('****** PyMS version %s started ******', VERSION)
setrunning(True)
app = QApplication(sys.argv)
mainform = UiMain()
mainform.show()

sys.exit(app.exec())
