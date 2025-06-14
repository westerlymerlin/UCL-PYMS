# None

<a id="manual_xy_form"></a>

# manual\_xy\_form

Manual XY-Form
Author: Gary Twinn

<a id="manual_xy_form.sqlite3"></a>

## sqlite3

<a id="manual_xy_form.sleep"></a>

## sleep

<a id="manual_xy_form.sys"></a>

## sys

<a id="manual_xy_form.Qt"></a>

## Qt

<a id="manual_xy_form.QTimer"></a>

## QTimer

<a id="manual_xy_form.QThreadPool"></a>

## QThreadPool

<a id="manual_xy_form.QApplication"></a>

## QApplication

<a id="manual_xy_form.QDialog"></a>

## QDialog

<a id="manual_xy_form.Ui_dialogXYSetup"></a>

## Ui\_dialogXYSetup

<a id="manual_xy_form.settings"></a>

## settings

<a id="manual_xy_form.xyread"></a>

## xyread

<a id="manual_xy_form.xymove"></a>

## xymove

<a id="manual_xy_form.xymoveto"></a>

## xymoveto

<a id="manual_xy_form.currentcycle"></a>

## currentcycle

<a id="manual_xy_form.batch"></a>

## batch

<a id="manual_xy_form.ManualXyForm"></a>

## ManualXyForm Objects

```python
class ManualXyForm(QDialog, Ui_dialogXYSetup)
```

ManualXyForm(QDialog, Ui_dialogXYSetup)
This class represents the manual XY form dialog.
It allows the user to manually control the X and Y positions of a device.

<a id="manual_xy_form.ManualXyForm.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="manual_xy_form.ManualXyForm.formclose"></a>

#### formclose

```python
def formclose()
```

Close event

<a id="manual_xy_form.ManualXyForm.timer"></a>

#### timer

```python
def timer()
```

Timer function to update the display of X and Y positions

<a id="manual_xy_form.ManualXyForm.update_xy"></a>

#### update\_xy

```python
def update_xy()
```

Display the current X and Y positions

<a id="manual_xy_form.ManualXyForm.gotopress"></a>

#### gotopress

```python
def gotopress()
```

Goto Button event handler

<a id="manual_xy_form.ManualXyForm.gotonextpress"></a>

#### gotonextpress

```python
def gotonextpress()
```

Goto Next Button event handler

<a id="manual_xy_form.ManualXyForm.movepress"></a>

#### movepress

```python
def movepress(direction)
```

Move button handler - used by arrow buttons

<a id="manual_xy_form.ManualXyForm.stopall"></a>

#### stopall

```python
def stopall()
```

Stop all button event handler

<a id="manual_xy_form.ManualXyForm.savelocation"></a>

#### savelocation

```python
def savelocation()
```

Saves current x and y values to current planchet location in the database, used when calibrating
the planchet

