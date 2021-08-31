from PySide2.QtWidgets import *
from ui_newbatch import Ui_dialogNewBatch
from settings import settings
from simpleBatchForm import UiSimpleBatch
from planchetform import UiPlanchet
from batchclass import batch


class UiBatch(QDialog, Ui_dialogNewBatch):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(settings['newbatchform']['x'], settings['newbatchform']['y'])
        self.btnClose.clicked.connect(self.formclose)
        self.btnNew.clicked.connect(self.newbatch)
        self.btnEdit.clicked.connect(self.editbatch)
        if batch.id == -1:
            self.btnEdit.setVisible(False)

    def formclose(self):
        settings['newbatchform']['x'] = self.x()
        settings['newbatchform']['y'] = self.y()
        self.deleteLater()

    def openbatcheck(self):
        if batch.type == 'simple' and batch.id != -1:
            self.radioNewSimple.setChecked(True)
            self.radioNewPlanchet.setChecked(False)
            self.lblMessage.setText('There is already a simple batch # %s loaded, do you want to \n'
                                    'Edit it or click New to cancel the current and create a new one?' % batch.id)
        elif batch.type == 'planchet' and batch.id != -1:
            self.radioNewSimple.setChecked(False)
            self.radioNewPlanchet.setChecked(True)
            self.lblMessage.setText('There is already a planchet # %s loaded, do you want to\n'
                                    'Edit it or click New to cancel the current and create a new one?' % batch.id)

    def newbatch(self):
        if self.radioNewSimple.isChecked():
            batch.new('simple', '')
            self.simpledialog = UiSimpleBatch()
            self.simpledialog.setModal(True)
            self.simpledialog.startup()
            self.simpledialog.show()
        else:
            batch.new('planchet', '')
            self.simpledialog = UiPlanchet()
            self.simpledialog.setModal(True)
            self.simpledialog.startup()
            self.simpledialog.show()
        self.close()

    def editbatch(self):
        if self.radioNewSimple.isChecked():
            self.simpledialog = UiSimpleBatch()
            self.simpledialog.setModal(True)
            self.simpledialog.startup()
            self.simpledialog.show()
        else:
            self.simpledialog = UiPlanchet()
            self.simpledialog.setModal(True)
            self.simpledialog.startup()
            self.simpledialog.show()
        self.close()
