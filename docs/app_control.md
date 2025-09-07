# None

<a id="app_control"></a>

# app\_control

Application Control module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function. Has global variables and routine for
calculating a file name and removing illegal character.

<a id="app_control.json"></a>

## json

<a id="app_control.datetime"></a>

## datetime

<a id="app_control.VERSION"></a>

#### VERSION

<a id="app_control.running"></a>

#### running

<a id="app_control.alarms"></a>

#### alarms

<a id="app_control.friendlydirname"></a>

#### friendlydirname

```python
def friendlydirname(sourcename: str) -> str
```

Removes invalid characters from file names

<a id="app_control.setrunning"></a>

#### setrunning

```python
def setrunning(state)
```

Global signal to detect if app is running - used to kill off threads

<a id="app_control.writesettings"></a>

#### writesettings

```python
def writesettings()
```

Write settings to json file

<a id="app_control.initialise"></a>

#### initialise

```python
def initialise()
```

Setup the settings structure with default values

<a id="app_control.readsettings"></a>

#### readsettings

```python
def readsettings()
```

Read the json file

<a id="app_control.loadsettings"></a>

#### loadsettings

```python
def loadsettings()
```

Replace the default settings with those from the json files

<a id="app_control.settings"></a>

#### settings

