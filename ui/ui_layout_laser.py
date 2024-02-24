# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'laser.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QApplication, QDial, QDialog, QFrame,
    QLabel, QSizePolicy, QSlider, QToolButton,
    QWidget)
import main_rc

class Ui_dialogLaserControl(object):
    def setupUi(self, dialogLaserControl):
        if not dialogLaserControl.objectName():
            dialogLaserControl.setObjectName(u"dialogLaserControl")
        dialogLaserControl.resize(242, 234)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialogLaserControl.sizePolicy().hasHeightForWidth())
        dialogLaserControl.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/main/iconPyMSRun.svg", QSize(), QIcon.Normal, QIcon.Off)
        dialogLaserControl.setWindowIcon(icon)
        dialogLaserControl.setStyleSheet(u"font: 10pt \"Segoe UI\";")
        self.imgLaser = QLabel(dialogLaserControl)
        self.imgLaser.setObjectName(u"imgLaser")
        self.imgLaser.setGeometry(QRect(20, 20, 133, 133))
        self.imgLaser.setStyleSheet(u"image: url(:/main/laser.png);")
        self.label = QLabel(dialogLaserControl)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(77, 160, 81, 20))
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.btnClose = QToolButton(dialogLaserControl)
        self.btnClose.setObjectName(u"btnClose")
        self.btnClose.setGeometry(QRect(170, 200, 63, 31))
        icon1 = QIcon()
        icon1.addFile(u":/laser/laserform_close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnClose.setIcon(icon1)
        self.btnClose.setIconSize(QSize(61, 31))
        self.btnOn = QToolButton(dialogLaserControl)
        self.btnOn.setObjectName(u"btnOn")
        self.btnOn.setGeometry(QRect(100, 200, 63, 31))
        self.btnOn.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/laser/laserform_on_disabled.png", QSize(), QIcon.Disabled, QIcon.Off)
        icon2.addFile(u":/laser/laserform_on_disabled.png", QSize(), QIcon.Disabled, QIcon.On)
        icon2.addFile(u":/laser/laserform_on.png", QSize(), QIcon.Active, QIcon.Off)
        icon2.addFile(u":/laser/laserform_off.png", QSize(), QIcon.Active, QIcon.On)
        self.btnOn.setIcon(icon2)
        self.btnOn.setIconSize(QSize(61, 31))
        self.btnOn.setCheckable(True)
        self.btnOn.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.lblLaser = QLabel(dialogLaserControl)
        self.lblLaser.setObjectName(u"lblLaser")
        self.lblLaser.setGeometry(QRect(170, 160, 61, 21))
        self.lblLaser.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"font: 14pt \"Segoe UI\";")
        self.lblLaser.setFrameShape(QFrame.Box)
        self.lblLaser.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.sliderEnable = QSlider(dialogLaserControl)
        self.sliderEnable.setObjectName(u"sliderEnable")
        self.sliderEnable.setGeometry(QRect(160, 53, 22, 41))
        self.sliderEnable.setStyleSheet(u"")
        self.sliderEnable.setMaximum(2)
        self.sliderEnable.setSingleStep(1)
        self.sliderEnable.setPageStep(1)
        self.sliderEnable.setOrientation(Qt.Vertical)
        self.sliderEnable.setInvertedAppearance(True)
        self.sliderEnable.setTickPosition(QSlider.NoTicks)
        self.sliderEnable.setTickInterval(10)
        self.sliderLaser = QDial(dialogLaserControl)
        self.sliderLaser.setObjectName(u"sliderLaser")
        self.sliderLaser.setGeometry(QRect(24, 18, 116, 133))
        self.sliderLaser.setFocusPolicy(Qt.WheelFocus)
        self.sliderLaser.setToolTipDuration(-1)
        self.sliderLaser.setMaximum(999)
        self.sliderLaser.setSingleStep(1)
        self.sliderLaser.setPageStep(1)
        self.sliderLaser.setValue(500)
        self.sliderLaser.setSliderPosition(500)
        self.sliderLaser.setWrapping(False)
        self.sliderLaser.setNotchTarget(100.000000000000000)
        self.sliderLaser.setNotchesVisible(False)
        self.label_2 = QLabel(dialogLaserControl)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(185, 50, 49, 16))
        self.label_3 = QLabel(dialogLaserControl)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(185, 80, 49, 16))
        self.imgSlider = QLabel(dialogLaserControl)
        self.imgSlider.setObjectName(u"imgSlider")
        self.imgSlider.setGeometry(QRect(1, 5, 160, 160))
        self.imgSlider.setStyleSheet(u"image: url(:/laser/laserform_slider.png);")
        self.imgSlider.setAlignment(Qt.AlignCenter)
        self.imgSlider.setTextInteractionFlags(Qt.NoTextInteraction)
        self.lblStatus = QLabel(dialogLaserControl)
        self.lblStatus.setObjectName(u"lblStatus")
        self.lblStatus.setGeometry(QRect(128, 10, 101, 20))
        self.lblStatus.setStyleSheet(u"")
        self.lblStatus.setFrameShape(QFrame.NoFrame)
        self.lblStatus.setFrameShadow(QFrame.Plain)
        self.lblStatus.setTextFormat(Qt.PlainText)
        self.lblStatus.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lblStatus.setTextInteractionFlags(Qt.NoTextInteraction)
        self.imgSlider.raise_()
        self.sliderLaser.raise_()
        self.label.raise_()
        self.btnClose.raise_()
        self.btnOn.raise_()
        self.lblLaser.raise_()
        self.sliderEnable.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.imgLaser.raise_()
        self.lblStatus.raise_()

        self.retranslateUi(dialogLaserControl)

        QMetaObject.connectSlotsByName(dialogLaserControl)
    # setupUi

    def retranslateUi(self, dialogLaserControl):
        dialogLaserControl.setWindowTitle(QCoreApplication.translate("dialogLaserControl", u"Laser Manual Control", None))
        self.imgLaser.setText("")
        self.label.setText(QCoreApplication.translate("dialogLaserControl", u"Laser Power", None))
        self.btnClose.setText("")
        self.btnOn.setText("")
        self.lblLaser.setText(QCoreApplication.translate("dialogLaserControl", u"0", None))
        self.label_2.setText(QCoreApplication.translate("dialogLaserControl", u"Disabled", None))
        self.label_3.setText(QCoreApplication.translate("dialogLaserControl", u"Enabled", None))
        self.imgSlider.setText("")
        self.lblStatus.setText("")
    # retranslateUi

