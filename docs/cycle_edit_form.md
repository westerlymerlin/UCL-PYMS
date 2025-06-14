# None

<a id="cycle_edit_form"></a>

# cycle\_edit\_form

UI Form for Editing Cycles
Author: Gary Twinn

<a id="cycle_edit_form.sys"></a>

## sys

<a id="cycle_edit_form.sqlite3"></a>

## sqlite3

<a id="cycle_edit_form.QDialog"></a>

## QDialog

<a id="cycle_edit_form.QApplication"></a>

## QApplication

<a id="cycle_edit_form.QTableWidgetItem"></a>

## QTableWidgetItem

<a id="cycle_edit_form.QMessageBox"></a>

## QMessageBox

<a id="cycle_edit_form.QInputDialog"></a>

## QInputDialog

<a id="cycle_edit_form.QLineEdit"></a>

## QLineEdit

<a id="cycle_edit_form.Ui_dialogCycleEdit"></a>

## Ui\_dialogCycleEdit

<a id="cycle_edit_form.settings"></a>

## settings

<a id="cycle_edit_form.writesettings"></a>

## writesettings

<a id="cycle_edit_form.VERSION"></a>

## VERSION

<a id="cycle_edit_form.logger"></a>

## logger

<a id="cycle_edit_form.listkey"></a>

#### listkey

```python
def listkey(item)
```

:param item: the item to extract the key from
:return: the key of the item

<a id="cycle_edit_form.CycleEditUI"></a>

## CycleEditUI Objects

```python
class CycleEditUI(QDialog, Ui_dialogCycleEdit)
```

Initializes the CycleEditUI class.

This class is responsible for managing the cycle editing user interface.

Args:
    None

Returns:
    None

<a id="cycle_edit_form.CycleEditUI.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="cycle_edit_form.CycleEditUI.formclose"></a>

#### formclose

```python
def formclose()
```

Form close event

<a id="cycle_edit_form.CycleEditUI.loadcycles"></a>

#### loadcycles

```python
def loadcycles()
```

Load cycles from database

<a id="cycle_edit_form.CycleEditUI.combochange"></a>

#### combochange

```python
def combochange()
```

Combobox change event

<a id="cycle_edit_form.CycleEditUI.sample_check"></a>

#### sample\_check

```python
def sample_check()
```

Check if cycle is for a cycle and needs laser power setting

<a id="cycle_edit_form.CycleEditUI.laserchange"></a>

#### laserchange

```python
def laserchange()
```

Detect a change in the laser power

<a id="cycle_edit_form.CycleEditUI.refreshtable"></a>

#### refreshtable

```python
def refreshtable()
```

Update the cycle table with the current cycle

<a id="cycle_edit_form.CycleEditUI.rowselect"></a>

#### rowselect

```python
def rowselect()
```

Detect a row selection

<a id="cycle_edit_form.CycleEditUI.add_button_clicked"></a>

#### add\_button\_clicked

```python
def add_button_clicked()
```

Add button event handler

<a id="cycle_edit_form.CycleEditUI.update_button_clicked"></a>

#### update\_button\_clicked

```python
def update_button_clicked()
```

Update button event handler

<a id="cycle_edit_form.CycleEditUI.delete_button_clicked"></a>

#### delete\_button\_clicked

```python
def delete_button_clicked()
```

Delete button event handler

<a id="cycle_edit_form.CycleEditUI.save_steps_button_clicked"></a>

#### save\_steps\_button\_clicked

```python
def save_steps_button_clicked()
```

Save seteps button event handler

<a id="cycle_edit_form.CycleEditUI.save_cycle_button_clicked"></a>

#### save\_cycle\_button\_clicked

```python
def save_cycle_button_clicked()
```

Save cycle button event handler

<a id="cycle_edit_form.CycleEditUI.duplicate_cycle_button_clicked"></a>

#### duplicate\_cycle\_button\_clicked

```python
def duplicate_cycle_button_clicked()
```

Duplicate Cycle button event handler

<a id="cycle_edit_form.CycleEditUI.revert_button_clicked"></a>

#### revert\_button\_clicked

```python
def revert_button_clicked()
```

revert button event handler

<a id="cycle_edit_form.CycleEditUI.commandselector"></a>

#### commandselector

```python
def commandselector(target)
```

command parser

