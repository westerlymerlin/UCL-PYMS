# Contents for: settings_viewer_form

* [settings\_viewer\_form](#settings_viewer_form)
  * [sys](#settings_viewer_form.sys)
  * [QDialog](#settings_viewer_form.QDialog)
  * [QAbstractItemView](#settings_viewer_form.QAbstractItemView)
  * [QTableWidget](#settings_viewer_form.QTableWidget)
  * [QTableWidgetItem](#settings_viewer_form.QTableWidgetItem)
  * [QApplication](#settings_viewer_form.QApplication)
  * [Qt](#settings_viewer_form.Qt)
  * [QFont](#settings_viewer_form.QFont)
  * [Ui\_LogDialog](#settings_viewer_form.Ui_LogDialog)
  * [settings](#settings_viewer_form.settings)
  * [writesettings](#settings_viewer_form.writesettings)
  * [logger](#settings_viewer_form.logger)
  * [UiSettingsViewer](#settings_viewer_form.UiSettingsViewer)
    * [\_\_init\_\_](#settings_viewer_form.UiSettingsViewer.__init__)
    * [loadsettings](#settings_viewer_form.UiSettingsViewer.loadsettings)
    * [settingchanged](#settings_viewer_form.UiSettingsViewer.settingchanged)
    * [formclose](#settings_viewer_form.UiSettingsViewer.formclose)

<a id="settings_viewer_form"></a>

# settings\_viewer\_form

Settings Viewer form
Author: Gary Twinn

<a id="settings_viewer_form.sys"></a>

## sys

<a id="settings_viewer_form.QDialog"></a>

## QDialog

<a id="settings_viewer_form.QAbstractItemView"></a>

## QAbstractItemView

<a id="settings_viewer_form.QTableWidget"></a>

## QTableWidget

<a id="settings_viewer_form.QTableWidgetItem"></a>

## QTableWidgetItem

<a id="settings_viewer_form.QApplication"></a>

## QApplication

<a id="settings_viewer_form.Qt"></a>

## Qt

<a id="settings_viewer_form.QFont"></a>

## QFont

<a id="settings_viewer_form.Ui_LogDialog"></a>

## Ui\_LogDialog

<a id="settings_viewer_form.settings"></a>

## settings

<a id="settings_viewer_form.writesettings"></a>

## writesettings

<a id="settings_viewer_form.logger"></a>

## logger

<a id="settings_viewer_form.UiSettingsViewer"></a>

## UiSettingsViewer Objects

```python
class UiSettingsViewer(QDialog, Ui_LogDialog)
```

Initialise the settings viewer form

<a id="settings_viewer_form.UiSettingsViewer.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="settings_viewer_form.UiSettingsViewer.loadsettings"></a>

#### loadsettings

```python
def loadsettings()
```

Load the settings into a table

<a id="settings_viewer_form.UiSettingsViewer.settingchanged"></a>

#### settingchanged

```python
def settingchanged(cell)
```

If a setting has changed write it back to the settings file

<a id="settings_viewer_form.UiSettingsViewer.formclose"></a>

#### formclose

```python
def formclose()
```

Form close handler

