# None

<a id="laser_manual_form"></a>

# laser\_manual\_form

Laser Manual Form, used to manually control the Helium line laser ina  controlled manner
Author: Gary Twinn

<a id="laser_manual_form.sys"></a>

## sys

<a id="laser_manual_form.Qt"></a>

## Qt

<a id="laser_manual_form.QTimer"></a>

## QTimer

<a id="laser_manual_form.QThreadPool"></a>

## QThreadPool

<a id="laser_manual_form.QDialog"></a>

## QDialog

<a id="laser_manual_form.QApplication"></a>

## QApplication

<a id="laser_manual_form.Ui_dialogLaserControl"></a>

## Ui\_dialogLaserControl

<a id="laser_manual_form.settings"></a>

## settings

<a id="laser_manual_form.lasergetalarm"></a>

## lasergetalarm

<a id="laser_manual_form.lasercommand"></a>

## lasercommand

<a id="laser_manual_form.lasersetpower"></a>

## lasersetpower

<a id="laser_manual_form.LaserFormUI"></a>

## LaserFormUI Objects

```python
class LaserFormUI(QDialog, Ui_dialogLaserControl)
```

The LaserFormUI class represents a dialog window for controlling a laser.

<a id="laser_manual_form.LaserFormUI.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="laser_manual_form.LaserFormUI.formclose"></a>

#### formclose

```python
def formclose()
```

Form close event handler

<a id="laser_manual_form.LaserFormUI.slidermove"></a>

#### slidermove

```python
def slidermove()
```

Laser power slider event handler

<a id="laser_manual_form.LaserFormUI.enable_click"></a>

#### enable\_click

```python
def enable_click()
```

Laser enable button event handler

<a id="laser_manual_form.LaserFormUI.laser_click"></a>

#### laser\_click

```python
def laser_click()
```

Laser on off event handler

<a id="laser_manual_form.LaserFormUI.update_laser"></a>

#### update\_laser

```python
def update_laser()
```

Update laser status and laser power

