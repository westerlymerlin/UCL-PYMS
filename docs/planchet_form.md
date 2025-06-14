# None

<a id="planchet_form"></a>

# planchet\_form

Planchet entry form
Author: Gary Twinn

<a id="planchet_form.sys"></a>

## sys

<a id="planchet_form.QDialog"></a>

## QDialog

<a id="planchet_form.QApplication"></a>

## QApplication

<a id="planchet_form.Ui_dialogPlanchet"></a>

## Ui\_dialogPlanchet

<a id="planchet_form.settings"></a>

## settings

<a id="planchet_form.batch"></a>

## batch

<a id="planchet_form.currentcycle"></a>

## currentcycle

<a id="planchet_form.UiPlanchet"></a>

## UiPlanchet Objects

```python
class UiPlanchet(QDialog, Ui_dialogPlanchet)
```

Form class for the planchet

<a id="planchet_form.UiPlanchet.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="planchet_form.UiPlanchet.startup"></a>

#### startup

```python
def startup()
```

Initialise the planchet, if new set to blank but if the batch exists populate sample names int the planchet
locations

<a id="planchet_form.UiPlanchet.formclose"></a>

#### formclose

```python
def formclose()
```

Form close event handler

<a id="planchet_form.UiPlanchet.savechecks"></a>

#### savechecks

```python
def savechecks()
```

Tests to run before saving to ensure every sample has a valid name

