# None

<a id="settings_viewer_form"></a>

# settings\_viewer\_form

Settings viewer / editor form. allows user to edit setting values manually. settings are then saves in the
settings.json file
Author: Gary Twinn

<a id="settings_viewer_form.QDialog"></a>

## QDialog

<a id="settings_viewer_form.QAbstractItemView"></a>

## QAbstractItemView

<a id="settings_viewer_form.QTableWidget"></a>

## QTableWidget

<a id="settings_viewer_form.QTableWidgetItem"></a>

## QTableWidgetItem

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

