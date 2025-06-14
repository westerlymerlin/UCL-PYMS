# None

<a id="ncc_calc_form"></a>

# ncc\_calc\_form

NCC Calculation Form
Author: Gary Twinn

<a id="ncc_calc_form.sys"></a>

## sys

<a id="ncc_calc_form.QApplication"></a>

## QApplication

<a id="ncc_calc_form.QDialog"></a>

## QDialog

<a id="ncc_calc_form.QFrame"></a>

## QFrame

<a id="ncc_calc_form.QTableWidgetItem"></a>

## QTableWidgetItem

<a id="ncc_calc_form.QTableWidgetSelectionRange"></a>

## QTableWidgetSelectionRange

<a id="ncc_calc_form.QFileDialog"></a>

## QFileDialog

<a id="ncc_calc_form.QChart"></a>

## QChart

<a id="ncc_calc_form.QChartView"></a>

## QChartView

<a id="ncc_calc_form.QScatterSeries"></a>

## QScatterSeries

<a id="ncc_calc_form.Qt"></a>

## Qt

<a id="ncc_calc_form.QRect"></a>

## QRect

<a id="ncc_calc_form.QMargins"></a>

## QMargins

<a id="ncc_calc_form.QFont"></a>

## QFont

<a id="ncc_calc_form.QColor"></a>

## QColor

<a id="ncc_calc_form.numpy"></a>

## numpy

<a id="ncc_calc_form.Ui_dialogNccCalc"></a>

## Ui\_dialogNccCalc

<a id="ncc_calc_form.settings"></a>

## settings

<a id="ncc_calc_form.writesettings"></a>

## writesettings

<a id="ncc_calc_form.logger"></a>

## logger

<a id="ncc_calc_form.ncc"></a>

## ncc

<a id="ncc_calc_form.singlefilereader"></a>

## singlefilereader

<a id="ncc_calc_form.NccCalcUI"></a>

## NccCalcUI Objects

```python
class NccCalcUI(QDialog, Ui_dialogNccCalc)
```

This class is a QDialog that implements the user interface for the NCC Calculator application.

<a id="ncc_calc_form.NccCalcUI.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="ncc_calc_form.NccCalcUI.formclose"></a>

#### formclose

```python
def formclose()
```

Close event handler for the form

<a id="ncc_calc_form.NccCalcUI.columnheader"></a>

#### columnheader

```python
def columnheader(headertext, align)
```

Column header event handler

<a id="ncc_calc_form.NccCalcUI.readncc"></a>

#### readncc

```python
def readncc(filepath)
```

Read NCC files

<a id="ncc_calc_form.NccCalcUI.secondchanged"></a>

#### secondchanged

```python
def secondchanged()
```

Change the seconds to skip on the helium line data

<a id="ncc_calc_form.NccCalcUI.blankselectionhanler"></a>

#### blankselectionhanler

```python
def blankselectionhanler()
```

Line Blank selection handler

<a id="ncc_calc_form.NccCalcUI.generate_ncc_file"></a>

#### generate\_ncc\_file

```python
def generate_ncc_file()
```

NCC CSV File generator

<a id="ncc_calc_form.NccCalcUI.choose_source_dir"></a>

#### choose\_source\_dir

```python
def choose_source_dir()
```

Source folder selector

<a id="ncc_calc_form.NccCalcUI.create_scatterchart"></a>

#### create\_scatterchart

```python
def create_scatterchart(dataset, bestfit)
```

Chart creation function

<a id="ncc_calc_form.NccCalcUI.getfiledata"></a>

#### getfiledata

```python
def getfiledata()
```

He file charter

<a id="ncc_calc_form.NccCalcUI.refreshlist"></a>

#### refreshlist

```python
def refreshlist()
```

File list refresher

<a id="ncc_calc_form.NccCalcUI.qclick"></a>

#### qclick

```python
def qclick()
```

Q-standard click handler, writes out the Q-standadrd data to a file 'qdata.csv'

<a id="ncc_calc_form.yvalues"></a>

#### yvalues

```python
def yvalues(dataset)
```

Return max and min of y values

