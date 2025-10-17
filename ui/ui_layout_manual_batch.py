# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'manualbatch.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QFrame,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpinBox, QTableWidget, QTableWidgetItem,
    QWidget)
import main_rc

class Ui_dialogManualBatch(object):
    def setupUi(self, dialogManualBatch):
        if not dialogManualBatch.objectName():
            dialogManualBatch.setObjectName(u"dialogManualBatch")
        dialogManualBatch.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialogManualBatch.setEnabled(True)
        dialogManualBatch.resize(808, 550)
        dialogManualBatch.setMinimumSize(QSize(808, 550))
        dialogManualBatch.setMaximumSize(QSize(810, 550))
        icon = QIcon()
        icon.addFile(u":/main/iconGTRun.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        dialogManualBatch.setWindowIcon(icon)
        dialogManualBatch.setStyleSheet(u"font: 10pt \"Segoe UI\";")
        self.labelError = QLabel(dialogManualBatch)
        self.labelError.setObjectName(u"labelError")
        self.labelError.setGeometry(QRect(20, 460, 571, 71))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.labelError.setFont(font)
        self.labelError.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.labelError.setScaledContents(True)
        self.labelError.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.labelError.setWordWrap(True)
        self.label_9 = QLabel(dialogManualBatch)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(10, 50, 171, 30))
        self.label_9.setScaledContents(True)
        self.lineDescription = QLineEdit(dialogManualBatch)
        self.lineDescription.setObjectName(u"lineDescription")
        self.lineDescription.setGeometry(QRect(190, 50, 611, 30))
        self.label_10 = QLabel(dialogManualBatch)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(10, 10, 171, 30))
        self.label_10.setScaledContents(True)
        self.lineDate = QLineEdit(dialogManualBatch)
        self.lineDate.setObjectName(u"lineDate")
        self.lineDate.setEnabled(True)
        self.lineDate.setGeometry(QRect(190, 10, 611, 30))
        self.lineDate.setStyleSheet(u"")
        self.lineDate.setReadOnly(True)
        self.tableBatchList = QTableWidget(dialogManualBatch)
        if (self.tableBatchList.columnCount() < 3):
            self.tableBatchList.setColumnCount(3)
        if (self.tableBatchList.rowCount() < 1):
            self.tableBatchList.setRowCount(1)
        self.tableBatchList.setObjectName(u"tableBatchList")
        self.tableBatchList.setGeometry(QRect(10, 100, 791, 341))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableBatchList.sizePolicy().hasHeightForWidth())
        self.tableBatchList.setSizePolicy(sizePolicy)
        self.tableBatchList.setStyleSheet(u"background-color: rgba(255, 255, 255, 255);\n"
"gridline-color: rgb(61, 61, 61);\n"
"alternate-background-color: rgb(225, 245, 255);\n"
"border-color: rgb(0, 0, 0);")
        self.tableBatchList.setFrameShape(QFrame.Shape.Box)
        self.tableBatchList.setFrameShadow(QFrame.Shadow.Plain)
        self.tableBatchList.setLineWidth(1)
        self.tableBatchList.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableBatchList.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tableBatchList.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.tableBatchList.setAlternatingRowColors(True)
        self.tableBatchList.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableBatchList.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.tableBatchList.setRowCount(1)
        self.tableBatchList.setColumnCount(3)
        self.tableBatchList.horizontalHeader().setVisible(False)
        self.tableBatchList.horizontalHeader().setHighlightSections(False)
        self.tableBatchList.verticalHeader().setVisible(False)
        self.tableBatchList.verticalHeader().setHighlightSections(False)
        self.spinAddRows = QSpinBox(dialogManualBatch)
        self.spinAddRows.setObjectName(u"spinAddRows")
        self.spinAddRows.setGeometry(QRect(710, 450, 88, 31))
        self.spinAddRows.setValue(1)
        self.btnAddRows = QPushButton(dialogManualBatch)
        self.btnAddRows.setObjectName(u"btnAddRows")
        self.btnAddRows.setGeometry(QRect(620, 450, 80, 31))
        self.btnAddRows.setAutoDefault(False)
        self.btnSave = QPushButton(dialogManualBatch)
        self.btnSave.setObjectName(u"btnSave")
        self.btnSave.setGeometry(QRect(620, 510, 80, 31))
        self.btnClose = QPushButton(dialogManualBatch)
        self.btnClose.setObjectName(u"btnClose")
        self.btnClose.setGeometry(QRect(710, 510, 80, 31))
        QWidget.setTabOrder(self.lineDescription, self.lineDate)

        self.retranslateUi(dialogManualBatch)

        self.btnAddRows.setDefault(True)
        self.btnSave.setDefault(True)
        self.btnClose.setDefault(True)


        QMetaObject.connectSlotsByName(dialogManualBatch)
    # setupUi

    def retranslateUi(self, dialogManualBatch):
        dialogManualBatch.setWindowTitle(QCoreApplication.translate("dialogManualBatch", u"New Manual Batch", None))
        self.labelError.setText("")
        self.label_9.setText(QCoreApplication.translate("dialogManualBatch", u"Description", None))
        self.label_10.setText(QCoreApplication.translate("dialogManualBatch", u"Date Created", None))
        self.btnAddRows.setText(QCoreApplication.translate("dialogManualBatch", u"Add Rows", None))
        self.btnSave.setText(QCoreApplication.translate("dialogManualBatch", u"Save", None))
        self.btnClose.setText(QCoreApplication.translate("dialogManualBatch", u"Close", None))
    # retranslateUi

