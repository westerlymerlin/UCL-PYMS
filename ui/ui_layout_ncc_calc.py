# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ncccalc.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QApplication, QDialog,
    QFrame, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QSpinBox, QTableWidget, QTableWidgetItem,
    QWidget)
import main_rc

class Ui_dialogNccCalc(object):
    def setupUi(self, dialogNccCalc):
        if not dialogNccCalc.objectName():
            dialogNccCalc.setObjectName(u"dialogNccCalc")
        dialogNccCalc.resize(1000, 790)
        dialogNccCalc.setMinimumSize(QSize(1000, 790))
        dialogNccCalc.setMaximumSize(QSize(1000, 790))
        icon = QIcon()
        icon.addFile(u":/main/iconNccCalc.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        dialogNccCalc.setWindowIcon(icon)
        dialogNccCalc.setStyleSheet(u"font: 10pt \"Segoe UI\";")
        self.tableFileList = QTableWidget(dialogNccCalc)
        self.tableFileList.setObjectName(u"tableFileList")
        self.tableFileList.setGeometry(QRect(10, 59, 480, 691))
        self.tableFileList.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(85, 85, 255);\n"
"border-color: rgb(61, 61, 61);\n"
"alternate-background-color: rgb(225, 245, 255);\n"
"selection-color: rgb(255, 255, 255);")
        self.tableFileList.setFrameShape(QFrame.Box)
        self.tableFileList.setLineWidth(2)
        self.tableFileList.setMidLineWidth(0)
        self.tableFileList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableFileList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableFileList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableFileList.setAlternatingRowColors(True)
        self.tableFileList.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableFileList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableFileList.setColumnCount(0)
        self.tableFileList.horizontalHeader().setHighlightSections(False)
        self.tableFileList.verticalHeader().setVisible(False)
        self.tableBlankList = QTableWidget(dialogNccCalc)
        self.tableBlankList.setObjectName(u"tableBlankList")
        self.tableBlankList.setGeometry(QRect(510, 240, 480, 131))
        self.tableBlankList.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(85, 85, 255);\n"
"border-color: rgb(61, 61, 61);\n"
"alternate-background-color: rgb(225, 245, 255);\n"
"selection-color: rgb(255, 255, 255);")
        self.tableBlankList.setLineWidth(2)
        self.tableBlankList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableBlankList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableBlankList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableBlankList.setAlternatingRowColors(True)
        self.tableBlankList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.tableBlankList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableBlankList.horizontalHeader().setHighlightSections(False)
        self.tableBlankList.verticalHeader().setVisible(False)
        self.tableBlankList.verticalHeader().setHighlightSections(False)
        self.tableQList = QTableWidget(dialogNccCalc)
        self.tableQList.setObjectName(u"tableQList")
        self.tableQList.setGeometry(QRect(510, 80, 480, 131))
        self.tableQList.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(85, 85, 255);\n"
"border-color: rgb(61, 61, 61);\n"
"alternate-background-color: rgb(225, 245, 255);\n"
"selection-color: rgb(255, 255, 255);")
        self.tableQList.setFrameShape(QFrame.Box)
        self.tableQList.setLineWidth(2)
        self.tableQList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableQList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableQList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableQList.setDefaultDropAction(Qt.IgnoreAction)
        self.tableQList.setAlternatingRowColors(True)
        self.tableQList.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableQList.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableQList.setTextElideMode(Qt.ElideLeft)
        self.tableQList.setWordWrap(False)
        self.tableQList.horizontalHeader().setHighlightSections(False)
        self.tableQList.verticalHeader().setVisible(False)
        self.tableQList.verticalHeader().setHighlightSections(False)
        self.label = QLabel(dialogNccCalc)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(510, 220, 71, 16))
        self.label.setStyleSheet(u"font: 600 10pt \"Segoe UI\";")
        self.label_2 = QLabel(dialogNccCalc)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(510, 60, 141, 16))
        self.label_2.setStyleSheet(u"font: 600 10pt \"Segoe UI\";")
        self.labelFilePath = QLabel(dialogNccCalc)
        self.labelFilePath.setObjectName(u"labelFilePath")
        self.labelFilePath.setGeometry(QRect(110, 20, 831, 20))
        self.btnFileOpen = QPushButton(dialogNccCalc)
        self.btnFileOpen.setObjectName(u"btnFileOpen")
        self.btnFileOpen.setGeometry(QRect(10, 20, 75, 24))
        self.btnFileOpen.setAutoDefault(False)
        self.label_3 = QLabel(dialogNccCalc)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(510, 380, 421, 16))
        self.label_3.setStyleSheet(u"font: 600 10pt \"Segoe UI\";")
        self.lblBlanckCorrect = QLabel(dialogNccCalc)
        self.lblBlanckCorrect.setObjectName(u"lblBlanckCorrect")
        self.lblBlanckCorrect.setGeometry(QRect(510, 400, 480, 21))
        self.lblBlanckCorrect.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.lblBlanckCorrect.setFrameShape(QFrame.Box)
        self.lblBlanckCorrect.setFrameShadow(QFrame.Sunken)
        self.lblBlanckCorrect.setLineWidth(1)
        self.lblBlanckCorrect.setTextFormat(Qt.PlainText)
        self.lblBlanckCorrect.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.btnNcc = QPushButton(dialogNccCalc)
        self.btnNcc.setObjectName(u"btnNcc")
        self.btnNcc.setGeometry(QRect(910, 430, 75, 24))
        self.btnNcc.setFlat(False)
        self.label_4 = QLabel(dialogNccCalc)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(721, 430, 181, 24))
        self.label_4.setStyleSheet(u"font: 600 10pt \"Segoe UI\";")
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_5 = QLabel(dialogNccCalc)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(510, 464, 91, 16))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setWeight(QFont.DemiBold)
        font.setItalic(False)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet(u"font: 600 10pt \"Segoe UI\";")
        self.label_6 = QLabel(dialogNccCalc)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(760, 464, 91, 16))
        self.label_6.setStyleSheet(u"font: 600 10pt \"Segoe UI\";")
        self.label_7 = QLabel(dialogNccCalc)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(510, 624, 91, 16))
        self.label_7.setStyleSheet(u"font: 600 10pt \"Segoe UI\";")
        self.label_8 = QLabel(dialogNccCalc)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(760, 624, 91, 16))
        self.label_8.setStyleSheet(u"font: 600 10pt \"Segoe UI\";")
        self.btnRefresh = QPushButton(dialogNccCalc)
        self.btnRefresh.setObjectName(u"btnRefresh")
        self.btnRefresh.setGeometry(QRect(400, 753, 75, 24))
        self.btnRefresh.setFlat(False)
        self.spinSeconds = QSpinBox(dialogNccCalc)
        self.spinSeconds.setObjectName(u"spinSeconds")
        self.spinSeconds.setGeometry(QRect(656, 430, 81, 24))
        self.spinSeconds.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.label_9 = QLabel(dialogNccCalc)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(532, 430, 116, 24))
        self.label_9.setStyleSheet(u"font: 600 10pt \"Segoe UI\";")
        self.label_9.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.retranslateUi(dialogNccCalc)

        QMetaObject.connectSlotsByName(dialogNccCalc)
    # setupUi

    def retranslateUi(self, dialogNccCalc):
        dialogNccCalc.setWindowTitle(QCoreApplication.translate("dialogNccCalc", u"PyMS ncc calculator", None))
#if QT_CONFIG(tooltip)
        self.tableFileList.setToolTip(QCoreApplication.translate("dialogNccCalc", u"Click on a file to show graphs of the data set", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.tableBlankList.setToolTip(QCoreApplication.translate("dialogNccCalc", u"<html><head/><body><p>Select line blanks to use to blank correct the 3He and 4He readings.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.tableQList.setToolTip(QCoreApplication.translate("dialogNccCalc", u"<html><head/><body><p>4He/3He is the measured ratio</p><p>Predicted is based on the number of times the Q (4He) and 3He pipettes have been used </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("dialogNccCalc", u"Line Blanks", None))
        self.label_2.setText(QCoreApplication.translate("dialogNccCalc", u"Q-Standards", None))
        self.labelFilePath.setText(QCoreApplication.translate("dialogNccCalc", u"FilePath", None))
#if QT_CONFIG(tooltip)
        self.btnFileOpen.setToolTip(QCoreApplication.translate("dialogNccCalc", u"Click to open the helium files", None))
#endif // QT_CONFIG(tooltip)
        self.btnFileOpen.setText(QCoreApplication.translate("dialogNccCalc", u"open", None))
        self.label_3.setText(QCoreApplication.translate("dialogNccCalc", u"Corrected Value for ncc calculations", None))
        self.lblBlanckCorrect.setText(QCoreApplication.translate("dialogNccCalc", u"blank", None))
#if QT_CONFIG(tooltip)
        self.btnNcc.setToolTip(QCoreApplication.translate("dialogNccCalc", u"<html><head/><body><p>Click to generate a PyMS_ncc.csv file</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btnNcc.setText(QCoreApplication.translate("dialogNccCalc", u"NCC", None))
        self.label_4.setText(QCoreApplication.translate("dialogNccCalc", u"Press to generate NCC file", None))
        self.label_5.setText(QCoreApplication.translate("dialogNccCalc", u"<html><head/><body><p><span style=\" vertical-align:super;\">4</span>He/<span style=\" vertical-align:super;\">3</span>He</p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("dialogNccCalc", u"H", None))
        self.label_7.setText(QCoreApplication.translate("dialogNccCalc", u"<html><head/><body><p><span style=\" vertical-align:super;\">3</span>He</p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("dialogNccCalc", u"<html><head/><body><p><span style=\" vertical-align:super;\">4</span>He</p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.btnRefresh.setToolTip(QCoreApplication.translate("dialogNccCalc", u"<html><head/><body><p>Click to generate a PyMS_ncc.csv file</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btnRefresh.setText(QCoreApplication.translate("dialogNccCalc", u"Refresh", None))
        self.label_9.setText(QCoreApplication.translate("dialogNccCalc", u"Seconds to skip", None))
    # retranslateUi

