from PySide6.QtWidgets import *
from PySide6.QtCharts import (QChart, QChartView, QScatterSeries)
from PySide6.QtCore import Qt, QRect, QMargins
from PySide6.QtGui import QFont, QColor
from ui_ncccalc import Ui_dialogNccCalc
import numpy
from settings import settings, writesettings
import sys
from ncc_calc import ncc


class NccCalcUI(QDialog, Ui_dialogNccCalc):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(settings['ncccalcform']['x'], settings['ncccalcform']['y'])
        self.btnFileOpen.clicked.connect(self.choose_source_dir)
        self.btnNcc.clicked.connect(self.generate_ncc_file)
        self.btnRefresh.clicked.connect(self.refreshlist)
        self.tableBlankList.itemSelectionChanged.connect(self.blankselectionhanler)
        self.tableFileList.itemSelectionChanged.connect(self.getfiledata)
        self.filepath = settings['Ncc']['ncc_filepath']
        self.tableFileList.setColumnCount(4)
        self.tableFileList.setHorizontalHeaderItem(0, self.columnheader('File', 'l'))
        self.tableFileList.setHorizontalHeaderItem(1, self.columnheader('Date', 'l'))
        self.tableFileList.setHorizontalHeaderItem(2, self.columnheader('Description', 'l'))
        self.tableFileList.setHorizontalHeaderItem(3, self.columnheader('4He/3He', 'r'))
        self.tableFileList.horizontalHeader().setStyleSheet("::section {""background-color: rgb(0, 85, 255); }")
        self.tableFileList.setColumnWidth(0, 80)
        self.tableFileList.setColumnWidth(1, 150)
        self.tableFileList.setColumnWidth(2, 150)
        self.tableFileList.setColumnWidth(3, 70)
        self.tableBlankList.setColumnCount(4)
        self.tableBlankList.setHorizontalHeaderItem(0, self.columnheader('File', 'l'))
        self.tableBlankList.setHorizontalHeaderItem(1, self.columnheader('Description', 'l'))
        self.tableBlankList.setHorizontalHeaderItem(2, self.columnheader('4He/3He', 'r'))
        self.tableBlankList.setHorizontalHeaderItem(3, self.columnheader('σ', 'r'))
        self.tableBlankList.horizontalHeader().setStyleSheet("::section {""background-color: rgb(0, 85, 255); }")
        self.tableBlankList.setColumnWidth(0, 80)
        self.tableBlankList.setColumnWidth(1, 150)
        self.tableBlankList.setColumnWidth(2, 90)
        self.tableBlankList.setColumnWidth(3, 90)
        self.tableQList.setColumnCount(5)
        self.tableQList.setHorizontalHeaderItem(0, self.columnheader('4He Pipette', 'l'))
        self.tableQList.setHorizontalHeaderItem(1, self.columnheader('3He Pipette', 'l'))
        self.tableQList.setHorizontalHeaderItem(2, self.columnheader('4He/3He', 'r'))
        self.tableQList.setHorizontalHeaderItem(3, self.columnheader('predicted', 'r'))
        self.tableQList.setHorizontalHeaderItem(4, self.columnheader('%', 'r'))
        self.tableQList.horizontalHeader().setStyleSheet("::section {""background-color: rgb(0, 85, 255); }")
        self.tableQList.setColumnWidth(0, 90)
        self.tableQList.setColumnWidth(1, 90)
        self.tableQList.setColumnWidth(2, 80)
        self.tableQList.setColumnWidth(3, 80)
        self.tableQList.setColumnWidth(4, 65)
        self.blank_mean = 0
        self.blank_stderr = 0
        self.readncc(self.filepath)
        self.list_count = 3
        self.value_max = 10
        self.value_count = 7
        self.m43chartview = QChartView(self)
        self.m43chartview.setGeometry(QRect(510, 480, 210, 140))
        self.m43chartview.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.m43chartview.setFrameShape(QFrame.Box)
        self.m43chartview.setToolTip('4He/3He ratio\nred line is bestfit')
        self.m1chartview = QChartView(self)
        self.m1chartview.setGeometry(QRect(730, 480, 210, 140))
        self.m1chartview.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.m1chartview.setFrameShape(QFrame.Box)
        self.m3chartview = QChartView(self)
        self.m3chartview.setGeometry(QRect(510, 640, 210, 140))
        self.m3chartview.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.m3chartview.setFrameShape(QFrame.Box)
        self.m4chartview = QChartView(self)
        self.m4chartview.setGeometry(QRect(730, 640, 210, 140))
        self.m4chartview.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.m4chartview.setFrameShape(QFrame.Box)

    def formclose(self):
        settings['ncccalcform']['x'] = self.x()
        settings['ncccalcform']['y'] = self.y()
        writesettings()
        self.deleteLater()

    def columnheader(self, headertext, align):
        item = QTableWidgetItem(headertext)
        if align == 'r':
            item.setTextAlignment(Qt.AlignRight)
        elif align == 'l':
            item.setTextAlignment(Qt.AlignLeft)
        font = QFont()
        font.setBold(True)
        item.setFont(font)
        colour = QColor()
        colour.setRgb(255, 255, 255)
        item.setForeground(colour)
        return item

    def readncc(self, filepath):
        ncc.readdirectory(filepath)
        settings['ncccalcform']['x'] = self.x()
        settings['ncccalcform']['y'] = self.y()
        settings['Ncc']['ncc_filepath'] = filepath
        writesettings()
        self.labelFilePath.setText(filepath)
        self.tableFileList.setRowCount(0)
        self.tableQList.setRowCount(0)
        self.tableBlankList.setRowCount(0)
        for i in range(len(ncc.files_names)):
            x = self.tableFileList.rowCount()
            self.tableFileList.insertRow(x)
            newfileitem = QTableWidgetItem(ncc.files_names[i])
            newtimeitem = QTableWidgetItem(ncc.files_dates[i])
            newdescriptionitem = QTableWidgetItem(ncc.files_descriptions[i])
            newresultsitem = QTableWidgetItem('%.3f' % ncc.files_he34ratios[i])
            newresultsitem.setTextAlignment(Qt.AlignRight)
            self.tableFileList.setItem(x, 0, newfileitem)
            self.tableFileList.setItem(x, 1, newtimeitem)
            self.tableFileList.setItem(x, 2, newdescriptionitem)
            self.tableFileList.setItem(x, 3, newresultsitem)
        for i in range(len(ncc.blanks_names)):
            x = self.tableBlankList.rowCount()
            self.tableBlankList.insertRow(x)
            newfileitem = QTableWidgetItem(ncc.blanks_names[i])
            newdescriptionitem = QTableWidgetItem('Line Blank')
            newresultsitem = QTableWidgetItem('%.6f' % ncc.blanks_he34ratios[i])
            newresultsitem.setTextAlignment(Qt.AlignRight)
            newerritem = QTableWidgetItem('%.6f' % ncc.blanks_he34sterrs[i])
            newerritem.setTextAlignment(Qt.AlignRight)
            self.tableBlankList.setItem(x, 0, newfileitem)
            self.tableBlankList.setItem(x, 1, newdescriptionitem)
            self.tableBlankList.setItem(x, 2, newresultsitem)
            self.tableBlankList.setItem(x, 3, newerritem)
            selrange = QTableWidgetSelectionRange(0, 0, len(ncc.blanks_names)-1, 3)
            self.tableBlankList.setRangeSelected(selrange, True)
        for i in range(len(ncc.qs_qnumbers)):
            x = self.tableQList.rowCount()
            self.tableQList.insertRow(x)
            qpredicted = ncc.calculate_estimated_qbestfit(ncc.qs_qnumbers[i], ncc.qs_he3_shots[i])
            newfileitem = QTableWidgetItem('%s' % ncc.qs_qnumbers[i])
            newdescriptionitem = QTableWidgetItem('%s' % ncc.qs_he3_shots[i])
            newresultsitem = QTableWidgetItem('%.3f' % ncc.qs_he34ratios[i])
            newresultsitem.setTextAlignment(Qt.AlignRight)
            newpitem = QTableWidgetItem('%.3f' % qpredicted)
            newpitem.setTextAlignment(Qt.AlignRight)
            newppercent = QTableWidgetItem('%.2f' % ((1-(ncc.qs_he34ratios[i]/qpredicted))*100))
            newppercent.setTextAlignment(Qt.AlignRight)
            self.tableQList.setItem(x, 0, newfileitem)
            self.tableQList.setItem(x, 1, newdescriptionitem)
            self.tableQList.setItem(x, 2, newresultsitem)
            self.tableQList.setItem(x, 3, newpitem)
            self.tableQList.setItem(x, 4, newppercent)

    def blankselectionhanler(self):
        counter = 0
        blank_ratios = []
        blank_errs = []
        for item in self.tableBlankList.selectedItems():
            if counter == 2:
                blank_ratios.append(float(item.text()))
            if counter == 3:
                blank_errs.append(float(item.text()))
            if counter == 4:
                counter = 0
            counter += 1
        if len(blank_ratios) > 0:
            self.blank_mean = numpy.mean(blank_ratios)
            self.blank_stderr = numpy.mean(blank_errs)
            self.lblBlanckCorrect.setText('mean = %.6f,     σ ± %.6f' % (self.blank_mean, self.blank_stderr))
            self.btnNcc.setEnabled(True)
        else:
            self.blank_mean = 0
            self.blank_stderr = 0
            self.btnNcc.setEnabled(False)
            self.lblBlanckCorrect.setText('No blanks selected')

    def generate_ncc_file(self):
        ncc.set_blank(self.blank_mean, self.blank_stderr)
        ncc.blankcorrect()
        ncc.calculate_ncc()
        ncc.write_ncc_file()

    def choose_source_dir(self):
        self.filepath = QFileDialog.getExistingDirectory(None, 'Open Helium Data folder', self.filepath)
        ncc.reset()
        self.readncc(self.filepath)

    def create_scatterchart(self, dataset, bestfit):
        colour = QColor()
        colour.setRgb(100, 100, 255)
        margins = QMargins()
        margins.setTop(-52)
        margins.setBottom(0)
        margins.setLeft(0)
        margins.setRight(-2)
        chart = QChart()
        series = QScatterSeries(chart)
        series.setMarkerSize(8)
        series.setColor(colour)
        colour.setRgb(255, 100, 100)
        for datapoint in dataset:
            series.append(datapoint[0], datapoint[1])
        if bestfit:
            series.setBestFitLineColor(colour)
            series.setBestFitLineVisible(True)
        chart.addSeries(series)
        chart.createDefaultAxes()
        axis_x = chart.axes(Qt.Horizontal)[0]
        axis_x.setMin(0)
        axis_x.setMax(200)
        axis_x.setLabelFormat("%i")
        axis_y = chart.axes(Qt.Vertical)[0]
        axis_y.setLabelFormat("%.2f")
        chart.setMargins(margins)
        return chart

    def getfiledata(self):
        if len(self.tableFileList.selectedItems()) > 0:
            filename = ncc.nccfilepath + '\\' + self.tableFileList.selectedItems()[0].text()
            m1, m3, m4, m43 = ncc.singlefilereader(filename)
            self.m43chartview.setChart(self.create_scatterchart(m43, True))
            self.m1chartview.setChart(self.create_scatterchart(m1, False))
            self.m3chartview.setChart(self.create_scatterchart(m3, False))
            self.m4chartview.setChart(self.create_scatterchart(m4, False))

    def refreshlist(self):
        ncc.reset()
        self.readncc(self.filepath)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = NccCalcUI()
    dialog.show()
    sys.exit(app.exec())
