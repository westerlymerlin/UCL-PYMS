# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'newbatch.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
    QRadioButton, QSizePolicy, QWidget)
import main_rc

class Ui_dialogNewBatch(object):
    def setupUi(self, dialogNewBatch):
        if not dialogNewBatch.objectName():
            dialogNewBatch.setObjectName(u"dialogNewBatch")
        dialogNewBatch.setWindowModality(Qt.ApplicationModal)
        dialogNewBatch.resize(970, 200)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialogNewBatch.sizePolicy().hasHeightForWidth())
        dialogNewBatch.setSizePolicy(sizePolicy)
        dialogNewBatch.setMinimumSize(QSize(970, 200))
        dialogNewBatch.setMaximumSize(QSize(970, 200))
        icon = QIcon()
        icon.addFile(u":/main/iconGTRun.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        dialogNewBatch.setWindowIcon(icon)
        dialogNewBatch.setStyleSheet(u"font: 10pt \"Segoe UI\";")
        self.btnClose = QPushButton(dialogNewBatch)
        self.btnClose.setObjectName(u"btnClose")
        self.btnClose.setGeometry(QRect(880, 170, 75, 23))
        self.btnClose.setFocusPolicy(Qt.TabFocus)
        self.btnNew = QPushButton(dialogNewBatch)
        self.btnNew.setObjectName(u"btnNew")
        self.btnNew.setGeometry(QRect(790, 170, 75, 23))
        self.radioNewSimple = QRadioButton(dialogNewBatch)
        self.radioNewSimple.setObjectName(u"radioNewSimple")
        self.radioNewSimple.setGeometry(QRect(30, 20, 921, 21))
        self.radioNewSimple.setChecked(False)
        self.radioNewPlanchet = QRadioButton(dialogNewBatch)
        self.radioNewPlanchet.setObjectName(u"radioNewPlanchet")
        self.radioNewPlanchet.setGeometry(QRect(30, 50, 941, 17))
        self.radioNewPlanchet.setChecked(True)
        self.btnEdit = QPushButton(dialogNewBatch)
        self.btnEdit.setObjectName(u"btnEdit")
        self.btnEdit.setGeometry(QRect(700, 170, 75, 23))
        self.lblMessage = QLabel(dialogNewBatch)
        self.lblMessage.setObjectName(u"lblMessage")
        self.lblMessage.setGeometry(QRect(40, 80, 911, 81))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.lblMessage.setFont(font)
        self.lblMessage.setStyleSheet(u"color: rgb(255, 0, 0);")
        self.lblMessage.setScaledContents(True)
        self.lblMessage.setWordWrap(True)
        QWidget.setTabOrder(self.btnEdit, self.btnNew)
        QWidget.setTabOrder(self.btnNew, self.btnClose)
        QWidget.setTabOrder(self.btnClose, self.radioNewSimple)
        QWidget.setTabOrder(self.radioNewSimple, self.radioNewPlanchet)

        self.retranslateUi(dialogNewBatch)

        QMetaObject.connectSlotsByName(dialogNewBatch)
    # setupUi

    def retranslateUi(self, dialogNewBatch):
        dialogNewBatch.setWindowTitle(QCoreApplication.translate("dialogNewBatch", u"New Batch", None))
        self.btnClose.setText(QCoreApplication.translate("dialogNewBatch", u"Cancel", None))
#if QT_CONFIG(tooltip)
        self.btnNew.setToolTip(QCoreApplication.translate("dialogNewBatch", u"create a new batch (will discard the current batch)", None))
#endif // QT_CONFIG(tooltip)
        self.btnNew.setText(QCoreApplication.translate("dialogNewBatch", u"New", None))
        self.radioNewSimple.setText(QCoreApplication.translate("dialogNewBatch", u"Simple Batch (up to 8 steps). Allows user to define Line Blanks and Q-Standards as well as samples.", None))
        self.radioNewPlanchet.setText(QCoreApplication.translate("dialogNewBatch", u"New Planchet. Allows the definition of each sample within a planchet, automatilally adds Line Blanks and Q-Standards. ", None))
#if QT_CONFIG(tooltip)
        self.btnEdit.setToolTip(QCoreApplication.translate("dialogNewBatch", u"Edit the current batch", None))
#endif // QT_CONFIG(tooltip)
        self.btnEdit.setText(QCoreApplication.translate("dialogNewBatch", u"Edit", None))
        self.lblMessage.setText("")
    # retranslateUi

