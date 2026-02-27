# None

<a id="app_control"></a>

# app\_control

Application Control module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function. Has global variables and routine for
calculating a file name and removing illegal character.

<a id="app_control.copyfile"></a>

## copyfile

<a id="app_control.json"></a>

## json

<a id="app_control.b64decode"></a>

## b64decode

<a id="app_control.b64encode"></a>

## b64encode

<a id="app_control.datetime"></a>

## datetime

<a id="app_control.VERSION"></a>

#### VERSION

<a id="app_control.RUNNING"></a>

#### RUNNING

<a id="app_control.alarms"></a>

#### alarms

<a id="app_control.friendlydirname"></a>

#### friendlydirname

```python
def friendlydirname(sourcename: str) -> str
```

Transforms a given string into a filesystem-friendly directory name.

This function modifies the input string by replacing invalid characters with a dash ('-')
to ensure the string adheres to naming conventions suitable for directory/file storage.
It also removes consecutive dashes created as a result of replacing invalid characters.

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

Writes and saves the current settings to a JSON file.

This function updates the 'LastSave' field in the settings dictionary with the
current date and time in the format 'DD/MM/YYYY HH:MM:SS' and writes the
updated dictionary to a file named 'settings.json'. The JSON file is saved
with UTF-8 encoding and is formatted with an indent of 4 spaces and keys sorted
in ascending order.

<a id="app_control.initialise"></a>

#### initialise

```python
def initialise()
```

Initializes the application settings and configurations.

This function creates and returns a dictionary containing all default
settings used in the application. These settings include configurations
for mass spectrometry, laser parameters, logging, forms positioning,
database paths, vacuum measurements, and API hosts.

<a id="app_control.readsettings"></a>

#### readsettings

```python
def readsettings()
```

Reads settings from a JSON file and loads them into a dictionary.

This function attempts to read a JSON configuration file named 'settings.json'
from the current working directory. If the file is successfully found and read,
it returns the parsed JSON data as a dictionary. If the file does not exist,
it returns an empty dictionary.

<a id="app_control.loadsettings"></a>

#### loadsettings

```python
def loadsettings()
```

This function reads configuration settings from an external source using the `readsettings`
function and updates the global `settings` dictionary. It handles multi-level dictionary
structures by iterating through their keys and updating corresponding values if found in
the external settings. If a key is missing in the external source, a message is printed,
and the current value in `settings` remains unchanged.

<a id="app_control.load_secrets"></a>

#### load\_secrets

```python
def load_secrets()
```

Load secrets from a file and decode them.

This function reads a file named 'SECRETS', decodes its contents using Base64,
and then parses the resulting JSON. It is used to securely retrieve stored
configuration or sensitive data. The file is expected to contain secrets
encoded in a specific format.

<a id="app_control.update_secret"></a>

#### update\_secret

```python
def update_secret(key, value)
```

Updates the secret storage by adding or updating a key-value pair. The method also creates a
backup of the existing storage file before writing the updated encoded secrets back to the file.

<a id="app_control.list_secret_keys"></a>

#### list\_secret\_keys

```python
def list_secret_keys()
```

Returns a list of all secret keys in the SECRETS file.

<a id="app_control.SECRETS"></a>

#### SECRETS

<a id="app_control.settings"></a>

#### settings

