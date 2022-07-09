# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cycleedit.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import main_rc

class Ui_dialogCycleEdit(object):
    def setupUi(self, dialogCycleEdit):
        if not dialogCycleEdit.objectName():
            dialogCycleEdit.setObjectName(u"dialogCycleEdit")
        dialogCycleEdit.resize(900, 700)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialogCycleEdit.sizePolicy().hasHeightForWidth())
        dialogCycleEdit.setSizePolicy(sizePolicy)
        dialogCycleEdit.setMinimumSize(QSize(900, 700))
        dialogCycleEdit.setMaximumSize(QSize(900, 700))
        icon = QIcon()
        icon.addFile(u":/main/iconPyMSRun.svg", QSize(), QIcon.Normal, QIcon.Off)
        dialogCycleEdit.setWindowIcon(icon)
        dialogCycleEdit.setStyleSheet(u"font: 10pt \"Segoe UI\";")
        self.tableSteps = QTableWidget(dialogCycleEdit)
        if (self.tableSteps.columnCount() < 3):
            self.tableSteps.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tableSteps.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tableSteps.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tableSteps.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.tableSteps.rowCount() < 10):
            self.tableSteps.setRowCount(10)
        self.tableSteps.setObjectName(u"tableSteps")
        self.tableSteps.setGeometry(QRect(20, 90, 530, 600))
        self.tableSteps.setStyleSheet(u"selection-background-color: rgb(197, 248, 255);\n"
"selection-color: rgb(0, 0, 0);\n"
"font: 10pt \"Segoe UI\";")
        self.tableSteps.setMidLineWidth(1)
        self.tableSteps.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableSteps.setDragDropOverwriteMode(False)
        self.tableSteps.setAlternatingRowColors(True)
        self.tableSteps.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableSteps.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableSteps.setTextElideMode(Qt.ElideLeft)
        self.tableSteps.setRowCount(10)
        self.tableSteps.setColumnCount(3)
        self.tableSteps.horizontalHeader().setVisible(True)
        self.tableSteps.horizontalHeader().setCascadingSectionResizes(False)
        self.tableSteps.horizontalHeader().setMinimumSectionSize(47)
        self.tableSteps.horizontalHeader().setDefaultSectionSize(130)
        self.tableSteps.verticalHeader().setVisible(False)
        self.comboCycles = QComboBox(dialogCycleEdit)
        self.comboCycles.setObjectName(u"comboCycles")
        self.comboCycles.setGeometry(QRect(20, 50, 300, 30))
        self.btnClose = QPushButton(dialogCycleEdit)
        self.btnClose.setObjectName(u"btnClose")
        self.btnClose.setGeometry(QRect(780, 660, 100, 35))
        self.textTime = QLineEdit(dialogCycleEdit)
        self.textTime.setObjectName(u"textTime")
        self.textTime.setGeometry(QRect(720, 120, 171, 30))
        self.label = QLabel(dialogCycleEdit)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(570, 120, 141, 30))
        self.label.setScaledContents(True)
        self.label_2 = QLabel(dialogCycleEdit)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(570, 180, 101, 30))
        self.label_2.setScaledContents(True)
        self.label_3 = QLabel(dialogCycleEdit)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(570, 240, 111, 30))
        self.label_3.setScaledContents(True)
        self.comboTarget = QComboBox(dialogCycleEdit)
        self.comboTarget.setObjectName(u"comboTarget")
        self.comboTarget.setGeometry(QRect(720, 180, 171, 30))
        self.comboCommand = QComboBox(dialogCycleEdit)
        self.comboCommand.setObjectName(u"comboCommand")
        self.comboCommand.setGeometry(QRect(720, 240, 171, 30))
        self.buttonAdd = QPushButton(dialogCycleEdit)
        self.buttonAdd.setObjectName(u"buttonAdd")
        self.buttonAdd.setGeometry(QRect(570, 370, 100, 35))
        self.buttonDelete = QPushButton(dialogCycleEdit)
        self.buttonDelete.setObjectName(u"buttonDelete")
        self.buttonDelete.setGeometry(QRect(780, 370, 100, 35))
        self.buttonSave = QPushButton(dialogCycleEdit)
        self.buttonSave.setObjectName(u"buttonSave")
        self.buttonSave.setGeometry(QRect(570, 430, 100, 35))
        self.buttonCancel = QPushButton(dialogCycleEdit)
        self.buttonCancel.setObjectName(u"buttonCancel")
        self.buttonCancel.setGeometry(QRect(780, 430, 100, 35))
        self.buttonUpdate = QPushButton(dialogCycleEdit)
        self.buttonUpdate.setObjectName(u"buttonUpdate")
        self.buttonUpdate.setGeometry(QRect(570, 310, 100, 35))
        self.label_4 = QLabel(dialogCycleEdit)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(30, 20, 91, 21))
        self.label_4.setScaledContents(True)

        self.retranslateUi(dialogCycleEdit)

        self.btnClose.setDefault(True)


        QMetaObject.connectSlotsByName(dialogCycleEdit)
    # setupUi

    def retranslateUi(self, dialogCycleEdit):
        dialogCycleEdit.setWindowTitle(QCoreApplication.translate("dialogCycleEdit", u"PyMS - Cycle Editor", None))
        ___qtablewidgetitem = self.tableSteps.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("dialogCycleEdit", u"Time(s)", None));
        ___qtablewidgetitem1 = self.tableSteps.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("dialogCycleEdit", u"Target", None));
        ___qtablewidgetitem2 = self.tableSteps.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("dialogCycleEdit", u"Command", None));
#if QT_CONFIG(tooltip)
        self.comboCycles.setToolTip(QCoreApplication.translate("dialogCycleEdit", u"Coose the cycle type to edit", None))
#endif // QT_CONFIG(tooltip)
        self.btnClose.setText(QCoreApplication.translate("dialogCycleEdit", u"Close", None))
        self.label.setText(QCoreApplication.translate("dialogCycleEdit", u"Timeslot (seconds)", None))
        self.label_2.setText(QCoreApplication.translate("dialogCycleEdit", u"Target", None))
        self.label_3.setText(QCoreApplication.translate("dialogCycleEdit", u"Command", None))
#if QT_CONFIG(tooltip)
        self.buttonAdd.setToolTip(QCoreApplication.translate("dialogCycleEdit", u"Add the task as a new one", None))
#endif // QT_CONFIG(tooltip)
        self.buttonAdd.setText(QCoreApplication.translate("dialogCycleEdit", u"Add New", None))
#if QT_CONFIG(tooltip)
        self.buttonDelete.setToolTip(QCoreApplication.translate("dialogCycleEdit", u"Delete selected task", None))
#endif // QT_CONFIG(tooltip)
        self.buttonDelete.setText(QCoreApplication.translate("dialogCycleEdit", u"Delete", None))
#if QT_CONFIG(tooltip)
        self.buttonSave.setToolTip(QCoreApplication.translate("dialogCycleEdit", u"Save thesee changes to the database", None))
#endif // QT_CONFIG(tooltip)
        self.buttonSave.setText(QCoreApplication.translate("dialogCycleEdit", u"Save", None))
#if QT_CONFIG(tooltip)
        self.buttonCancel.setToolTip(QCoreApplication.translate("dialogCycleEdit", u"Cencel all changes and revert to exisitng cycle", None))
#endif // QT_CONFIG(tooltip)
        self.buttonCancel.setText(QCoreApplication.translate("dialogCycleEdit", u"Revert", None))
#if QT_CONFIG(tooltip)
        self.buttonUpdate.setToolTip(QCoreApplication.translate("dialogCycleEdit", u"Update existing task", None))
#endif // QT_CONFIG(tooltip)
        self.buttonUpdate.setText(QCoreApplication.translate("dialogCycleEdit", u"Update", None))
        self.label_4.setText(QCoreApplication.translate("dialogCycleEdit", u"Cycle", None))
    # retranslateUi

