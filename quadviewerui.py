from PySide2.QtWidgets import *
from ui_quadviewer import Ui_dialogQuadViewer
from msFileclass import ms
from settings import settings


class UiQuadViwer(QDialog, QMainWindow, Ui_dialogQuadViewer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.multiplier = 1 / settings['MassSpec']['multiplier']
        self.btnClose.clicked.connect(self.formclose)
        self.btnReload.clicked.connect(self.readms)
        self.running = True
        self.readms()

    def formclose(self):
        self.running = False
        self.deleteLater()

    def readms(self):
        self.lineDateTime.setText('press')
        self.lineDateTime.setText(str(ms.quaddata[1]))
        self.lineM1.setText('%.5e' % ms.quaddata[7])
        self.lineM3.setText('%.5e' % ms.quaddata[8])
        self.lineM4.setText('%.5e' % ms.quaddata[9])
        self.lineM5.setText('%.5e' % ms.quaddata[10])
        self.lineM40.setText('%.5e' % ms.quaddata[11])
        Hd = 0.01 * ms.quaddata[7] * self.multiplier
        self.lineHD.setText('%.4f' % Hd)
        he3 = ((ms.quaddata[8] * self.multiplier) - Hd)
        self.line3He.setText('%.4f' % he3)
        he_ratio = ((ms.quaddata[9]*self.multiplier) / he3) * 1000
        self.line4He.setText('%.4f' % he_ratio)
        logfilename = '%sQuadViewer.txt' % settings['MassSpec']['datadirectory']
        with open(logfilename, 'a') as outfile:
            print('===========\t==========',file=outfile)
            print('Sample Time\t%s' % ms.quaddata[1], file=outfile)
            print('M1 Quad\t\t%s' % ms.quaddata[7] , file=outfile)
            print('M3 Quad\t\t%s' % ms.quaddata[8] ,file=outfile)
            print('M4 Quad\t\t%s' % ms.quaddata[9] ,file=outfile)
            print('M5 Quad\t\t%s' % ms.quaddata[10] ,file=outfile)
            print('M40 Quad\t%s' % ms.quaddata[11], file=outfile)
            print('Hd\t\t%s' % Hd, file=outfile)
            print('3Hd\t\t%s' % he3, file=outfile)
            print('4He / 3He\t%s' % he_ratio, file=outfile)
        outfile.close()




