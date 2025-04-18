# Contents for: simple_batch_form

* [simple\_batch\_form](#simple_batch_form)
  * [sys](#simple_batch_form.sys)
  * [QDialog](#simple_batch_form.QDialog)
  * [QApplication](#simple_batch_form.QApplication)
  * [Ui\_dialogSimpleBatch](#simple_batch_form.Ui_dialogSimpleBatch)
  * [settings](#simple_batch_form.settings)
  * [batch](#simple_batch_form.batch)
  * [currentcycle](#simple_batch_form.currentcycle)
  * [logger](#simple_batch_form.logger)
  * [UiSimpleBatch](#simple_batch_form.UiSimpleBatch)
    * [\_\_init\_\_](#simple_batch_form.UiSimpleBatch.__init__)
    * [startup](#simple_batch_form.UiSimpleBatch.startup)
    * [formclose](#simple_batch_form.UiSimpleBatch.formclose)
    * [taskcomboclick](#simple_batch_form.UiSimpleBatch.taskcomboclick)
    * [savechecks](#simple_batch_form.UiSimpleBatch.savechecks)

<a id="simple_batch_form"></a>

# simple\_batch\_form

Dialog for a simple batch (used for tesing the Helium line) has a maximum of 5 stepa
Author: Gary Twinn

<a id="simple_batch_form.sys"></a>

## sys

<a id="simple_batch_form.QDialog"></a>

## QDialog

<a id="simple_batch_form.QApplication"></a>

## QApplication

<a id="simple_batch_form.Ui_dialogSimpleBatch"></a>

## Ui\_dialogSimpleBatch

<a id="simple_batch_form.settings"></a>

## settings

<a id="simple_batch_form.batch"></a>

## batch

<a id="simple_batch_form.currentcycle"></a>

## currentcycle

<a id="simple_batch_form.logger"></a>

## logger

<a id="simple_batch_form.UiSimpleBatch"></a>

## UiSimpleBatch Objects

```python
class UiSimpleBatch(QDialog, Ui_dialogSimpleBatch)
```

Dialog Class

<a id="simple_batch_form.UiSimpleBatch.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="simple_batch_form.UiSimpleBatch.startup"></a>

#### startup

```python
def startup()
```

Initialise the form, if new set to blank but if the batch exists populate sample names into the relavent
locations

<a id="simple_batch_form.UiSimpleBatch.formclose"></a>

#### formclose

```python
def formclose()
```

Form close handler

<a id="simple_batch_form.UiSimpleBatch.taskcomboclick"></a>

#### taskcomboclick

```python
def taskcomboclick(index)
```

Combo box handler

<a id="simple_batch_form.UiSimpleBatch.savechecks"></a>

#### savechecks

```python
def savechecks()
```

Tests to run before saving to ensure every sample has a valid name

