# None

<a id="new_batch_form"></a>

# new\_batch\_form

New Batch dialog
Author: Gary Twinn

<a id="new_batch_form.QDialog"></a>

## QDialog

<a id="new_batch_form.Ui_dialogNewBatch"></a>

## Ui\_dialogNewBatch

<a id="new_batch_form.UiManualBatch"></a>

## UiManualBatch

<a id="new_batch_form.UiPlanchet"></a>

## UiPlanchet

<a id="new_batch_form.batch"></a>

## batch

<a id="new_batch_form.settings"></a>

## settings

<a id="new_batch_form.UiBatch"></a>

## UiBatch Objects

```python
class UiBatch(QDialog, Ui_dialogNewBatch)
```

Dialog class to handle the form

<a id="new_batch_form.UiBatch.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="new_batch_form.UiBatch.formclose"></a>

#### formclose

```python
def formclose()
```

Form close event handler

<a id="new_batch_form.UiBatch.openbatcheck"></a>

#### openbatcheck

```python
def openbatcheck()
```

Check if there is already an open batch and offer the option of editing it

<a id="new_batch_form.UiBatch.newbatch"></a>

#### newbatch

```python
def newbatch()
```

Create a new simple batch or planchet and close this form

<a id="new_batch_form.UiBatch.editbatch"></a>

#### editbatch

```python
def editbatch()
```

Open the simple batch or planchet for editing and close this form

