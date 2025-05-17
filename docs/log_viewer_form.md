# Contents for: log_viewer_form

* [log\_viewer\_form](#log_viewer_form)
  * [QDialog](#log_viewer_form.QDialog)
  * [QApplication](#log_viewer_form.QApplication)
  * [logger](#log_viewer_form.logger)
  * [Ui\_LogDialog](#log_viewer_form.Ui_LogDialog)
  * [settings](#log_viewer_form.settings)
  * [UiLogViewer](#log_viewer_form.UiLogViewer)
    * [\_\_init\_\_](#log_viewer_form.UiLogViewer.__init__)
    * [loadlog](#log_viewer_form.UiLogViewer.loadlog)
    * [formclose](#log_viewer_form.UiLogViewer.formclose)

<a id="log_viewer_form"></a>

# log\_viewer\_form

UI form for viewing the logs

<a id="log_viewer_form.QDialog"></a>

## QDialog

<a id="log_viewer_form.QApplication"></a>

## QApplication

<a id="log_viewer_form.logger"></a>

## logger

<a id="log_viewer_form.Ui_LogDialog"></a>

## Ui\_LogDialog

<a id="log_viewer_form.settings"></a>

## settings

<a id="log_viewer_form.UiLogViewer"></a>

## UiLogViewer Objects

```python
class UiLogViewer(QDialog, Ui_LogDialog)
```

Log viewer class

<a id="log_viewer_form.UiLogViewer.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="log_viewer_form.UiLogViewer.loadlog"></a>

#### loadlog

```python
def loadlog()
```

Read the application log and format it

<a id="log_viewer_form.UiLogViewer.formclose"></a>

#### formclose

```python
def formclose()
```

Close event for the form

