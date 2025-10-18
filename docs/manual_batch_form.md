# None

<a id="manual_batch_form"></a>

# manual\_batch\_form

Dialog for a Manual batch (used for testing the Helium line) has a default of 8 steps but more can be added
Author: Gary Twinn

<a id="manual_batch_form.sys"></a>

## sys

<a id="manual_batch_form.Qt"></a>

## Qt

<a id="manual_batch_form.QFont"></a>

## QFont

<a id="manual_batch_form.QDialog"></a>

## QDialog

<a id="manual_batch_form.QApplication"></a>

## QApplication

<a id="manual_batch_form.QTableWidgetItem"></a>

## QTableWidgetItem

<a id="manual_batch_form.QComboBox"></a>

## QComboBox

<a id="manual_batch_form.QLineEdit"></a>

## QLineEdit

<a id="manual_batch_form.Ui_dialogManualBatch"></a>

## Ui\_dialogManualBatch

<a id="manual_batch_form.settings"></a>

## settings

<a id="manual_batch_form.writesettings"></a>

## writesettings

<a id="manual_batch_form.batch"></a>

## batch

<a id="manual_batch_form.currentcycle"></a>

## currentcycle

<a id="manual_batch_form.logger"></a>

## logger

<a id="manual_batch_form.UiManualBatch"></a>

## UiManualBatch Objects

```python
class UiManualBatch(QDialog, Ui_dialogManualBatch)
```

Dialog Class

<a id="manual_batch_form.UiManualBatch.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="manual_batch_form.UiManualBatch.startup"></a>

#### startup

```python
def startup()
```

Initialise the form, if new set to blank but if the batch exists
populate sample names into the relevant locations

<a id="manual_batch_form.UiManualBatch.add_row"></a>

#### add\_row

```python
def add_row(rows_to_add)
```

Adds a specified number of rows to the table, each containing widgets for selecting cycles
and locations, as well as a description field. The rows are initialized with default cycle
and location choices, and style settings are applied.

<a id="manual_batch_form.UiManualBatch.load_batch_data"></a>

#### load\_batch\_data

```python
def load_batch_data()
```

if new set to blank but if the batch exists populate sample names into the relevant locations

<a id="manual_batch_form.UiManualBatch.task_combo_click"></a>

#### task\_combo\_click

```python
def task_combo_click()
```

Cycle type Combo box handler, enables the location and description if the task
is a sample based one (needs the laser)

<a id="manual_batch_form.UiManualBatch.formclose"></a>

#### formclose

```python
def formclose()
```

Form close handler

<a id="manual_batch_form.UiManualBatch.savechecks"></a>

#### savechecks

```python
def savechecks()
```

Tests to run before saving to ensure every sample has a valid name

