"""
NCC Calculation Form
Author: Gary Twinn
"""
import sys
from PySide6.QtWidgets import QApplication, QDialog, QFrame, QTableWidgetItem, QTableWidgetSelectionRange, QFileDialog
from PySide6.QtCharts import (QChart, QChartView, QScatterSeries)
from PySide6.QtCore import Qt, QRect, QMargins
from PySide6.QtGui import QFont, QColor
import numpy
from ui.ui_layout_ncc_calc import Ui_dialogNccCalc
from app_control import settings, writesettings
from logmanager import logger
from ncc_calc import ncc, singlefilereader


class NccCalcUI(QDialog, Ui_dialogNccCalc):
    """
    This class is a QDialog that implements the user interface for the NCC Calculator application.
    """
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
        self.tableBlankList.setColumnWidth(2, 115)
        self.tableBlankList.setColumnWidth(3, 110)
        self.tableQList.setColumnCount(5)
        self.tableQList.setHorizontalHeaderItem(0, self.columnheader('4He Pipette', 'l'))
        self.tableQList.setHorizontalHeaderItem(1, self.columnheader('3He Pipette', 'l'))
        self.tableQList.setHorizontalHeaderItem(2, self.columnheader('4He/3He', 'r'))
        self.tableQList.setHorizontalHeaderItem(3, self.columnheader('predicted', 'r'))
        self.tableQList.setHorizontalHeaderItem(4, self.columnheader('%', 'r'))
        self.tableQList.horizontalHeader().setStyleSheet("::section {""background-color: rgb(0, 85, 255); }")
        self.tableQList.setColumnWidth(0, 100)
        self.tableQList.setColumnWidth(1, 100)
        self.tableQList.setColumnWidth(2, 90)
        self.tableQList.setColumnWidth(3, 90)
        self.tableQList.setColumnWidth(4, 70)
        self.tableQList.itemDoubleClicked.connect(self.qclick)
        self.blank_mean = 0
        self.blank_stderr = 0
        self.readncc(self.filepath)
        self.list_count = 3
        self.value_max = 10
        self.value_count = 7
        self.m43chartview = QChartView(self)
        self.m43chartview.setGeometry(QRect(510, 480, 230, 135))
        self.m43chartview.setStyleSheet('background-color: rgb(255, 255, 255);border-color: rgb(94, 94, 94);')
        self.m43chartview.setFrameShape(QFrame.Box)
        self.m43chartview.setToolTip('4He/3He ratio\nred line is bestfit')
        self.m1chartview = QChartView(self)
        self.m1chartview.setGeometry(QRect(760, 480, 230, 135))
        self.m1chartview.setStyleSheet('background-color: rgb(255, 255, 255);border-color: rgb(94, 94, 94);')
        self.m1chartview.setFrameShape(QFrame.Box)
        self.m3chartview = QChartView(self)
        self.m3chartview.setGeometry(QRect(510, 640, 230, 135))
        self.m3chartview.setStyleSheet('background-color: rgb(255, 255, 255);border-color: rgb(94, 94, 94);')
        self.m3chartview.setFrameShape(QFrame.Box)
        self.m4chartview = QChartView(self)
        self.m4chartview.setGeometry(QRect(760, 640, 230, 135))
        self.m4chartview.setStyleSheet('background-color: rgb(255, 255, 255);border-color: rgb(94, 94, 94);')
        self.m4chartview.setFrameShape(QFrame.Box)
        self.spinSeconds.setValue(settings['Ncc']['ncc_start_seconds'])
        self.spinSeconds.valueChanged.connect(self.secondchanged)

    def formclose(self):
        """Close event handler for the form"""
        settings['ncccalcform']['x'] = self.x()
        settings['ncccalcform']['y'] = self.y()
        writesettings()
        self.deleteLater()

    def columnheader(self, headertext, align):
        """Column header event handler"""
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
        """Read NCC files"""
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

    def secondchanged(self):
        settings['Ncc']['ncc_start_seconds'] = self.spinSeconds.value()
        writesettings()
        self.refreshlist()

    def blankselectionhanler(self):
        """Line Blank selection handler"""
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
        """NCC CSV File generator"""
        ncc.set_blank(self.blank_mean, self.blank_stderr)
        ncc.blankcorrect()
        ncc.calculate_ncc()
        ncc.write_ncc_file()

    def choose_source_dir(self):
        """Source folder selector"""
        self.filepath = QFileDialog.getExistingDirectory(None, 'Open Helium Data folder', self.filepath)
        ncc.reset()
        self.readncc(self.filepath)

    def create_scatterchart(self, dataset, bestfit):
        """Chart creation function"""
        colour = QColor()
        colour.setRgb(100, 100, 255)
        margins = QMargins()
        margins.setTop(-52)
        margins.setBottom(0)
        margins.setLeft(-6)
        margins.setRight(-2)
        chart = QChart()
        series = QScatterSeries(chart)
        series.setMarkerSize(5)
        series.setColor(colour)
        colour.setRgb(255, 100, 100)
        for datapoint in dataset:
            series.append(datapoint[0], datapoint[1])
        if bestfit:
            series.setBestFitLineColor(colour)
            series.setBestFitLineVisible(True)
        chart.addSeries(series)
        chart.createDefaultAxes()
        font = QFont()
        font.setFamily('Segoe UI')
        font.setPointSize(7)
        axis_x = chart.axes(Qt.Horizontal)[0]
        axis_x.setMin(settings['Ncc']['ncc_start_seconds'] - 5)
        axis_x.setLabelsFont(font)
        axis_x.setLabelFormat("%i")
        axis_y = chart.axes(Qt.Vertical)[0]
        y_range = yvalues(dataset)
        axis_y.setMin(y_range[0])
        axis_y.setMax(y_range[1])
        if y_range[1] == 1:
            axis_y.setLabelFormat("%.1f")
        else:
            axis_y.setLabelFormat("%i")
        axis_y.setLabelsFont(font)

        chart.setMargins(margins)
        return chart

    def getfiledata(self):
        """He file charter"""
        if len(self.tableFileList.selectedItems()) > 0:
            filename = ncc.nccfilepath + '\\' + self.tableFileList.selectedItems()[0].text()
            m1, m3, m4, m43 = singlefilereader(filename)
            self.m43chartview.setChart(self.create_scatterchart(m43, True))
            self.m1chartview.setChart(self.create_scatterchart(m1, False))
            self.m3chartview.setChart(self.create_scatterchart(m3, False))
            self.m4chartview.setChart(self.create_scatterchart(m4, False))

    def refreshlist(self):
        """File list refresher"""
        ncc.reset()
        self.readncc(self.filepath)

    def qclick(self):
        """Q-standard click handler, writes out the Q-standadrd data to a file 'qdata.csv'"""
        filename = ncc.nccfilepath + '\\' + 'qdata.csv'
        with open(filename, 'w', encoding='utf-8') as qfile:
            #  print('4He Count, 3He Count, 4He/3He, Predicted', file=qfile)
            for line in range(self.tableQList.rowCount()):
                datarow = '%s, %s, %s, %s' % (self.tableQList.item(line, 0).text(),
                                              self.tableQList.item(line, 1).text(),
                                              self.tableQList.item(line, 2).text(),
                                              self.tableQList.item(line, 3).text())
                logger.debug('qdata: %s', datarow)
                print(datarow, file=qfile)
            qfile.close()


def yvalues(dataset):
    yvals = []
    for point in dataset:
        yvals.append(point[1])
    return [int(min(yvals)), int(max(yvals)) + 1]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = NccCalcUI()
    dialog.show()
    sys.exit(app.exec())
