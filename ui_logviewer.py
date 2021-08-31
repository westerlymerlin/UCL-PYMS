# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'logviewer.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import main_rc

class Ui_LogDialog(object):
    def setupUi(self, LogDialog):
        if not LogDialog.objectName():
            LogDialog.setObjectName(u"LogDialog")
        LogDialog.resize(1200, 990)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LogDialog.sizePolicy().hasHeightForWidth())
        LogDialog.setSizePolicy(sizePolicy)
        LogDialog.setMinimumSize(QSize(1200, 990))
        LogDialog.setMaximumSize(QSize(1200, 990))
        icon = QIcon()
        icon.addFile(u":/main/iconGTRun.svg", QSize(), QIcon.Normal, QIcon.Off)
        LogDialog.setWindowIcon(icon)
        LogDialog.setStyleSheet(u"font: 10pt \"Segoe UI\";")
        self.txtLog = QPlainTextEdit(LogDialog)
        self.txtLog.setObjectName(u"txtLog")
        self.txtLog.setGeometry(QRect(10, 50, 1181, 891))
        font = QFont()
        font.setFamily(u"Consolas")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.txtLog.setFont(font)
        self.txtLog.setStyleSheet(u"font: 10pt \"Consolas\";")
        self.txtLog.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.txtLog.setReadOnly(True)
        self.label = QLabel(LogDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 15, 211, 21))
        self.btnReload = QPushButton(LogDialog)
        self.btnReload.setObjectName(u"btnReload")
        self.btnReload.setGeometry(QRect(1010, 950, 80, 35))
        self.btnClose = QPushButton(LogDialog)
        self.btnClose.setObjectName(u"btnClose")
        self.btnClose.setGeometry(QRect(1110, 950, 80, 35))

        self.retranslateUi(LogDialog)

        self.btnClose.setDefault(True)


        QMetaObject.connectSlotsByName(LogDialog)
    # setupUi

    def retranslateUi(self, LogDialog):
        LogDialog.setWindowTitle(QCoreApplication.translate("LogDialog", u"PyMS - Application File Viewer", None))
        self.label.setText(QCoreApplication.translate("LogDialog", u"PyMS File", None))
        self.btnReload.setText(QCoreApplication.translate("LogDialog", u"Refresh", None))
        self.btnClose.setText(QCoreApplication.translate("LogDialog", u"Close", None))
    # retranslateUi

