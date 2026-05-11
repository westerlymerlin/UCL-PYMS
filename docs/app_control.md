# None

<a id="app_control"></a>

# app\_control

Application Control module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function. Has global variables and routine for
calculating a file name and removing illegal character.

<a id="app_control.copyfile"></a>

## copyfile

<a id="app_control.move"></a>

## move

<a id="app_control.json"></a>

## json

<a id="app_control.b64decode"></a>

## b64decode

<a id="app_control.b64encode"></a>

## b64encode

<a id="app_control.datetime"></a>

## datetime

<a id="app_control.yaml"></a>

## yaml

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

<a id="app_control.write_config"></a>

#### write\_config

```python
def write_config()
```

Writes the current settings to a YAML file. If a config file already exists, a backup
of the file is created before overwriting it. Updates the 'LastSave' timestamp in the
settings to the current date and time before saving.

<a id="app_control.backup_write_config"></a>

#### backup\_write\_config

```python
def backup_write_config()
```

Creates a backup of the current configuration file by renaming it to 'config.bak'.
This function is called before any changes are made to the configuration file to
ensure that a previous version is available for reference or restoration.

<a id="app_control.read_config_file"></a>

#### read\_config\_file

```python
def read_config_file()
```

Reads configuration data from a YAML file. If a YAML file is not found,
the function attempts to load configuration data from a old JSON file, converts it
to YAML format, and creates a new YAML file. If neither file is found, it returns
an empty dictionary with default settings.

<a id="app_control.initialise"></a>

#### initialise

```python
def initialise()
```

Initialises the application settings and configurations.

This function creates and returns a dictionary containing all default
settings used in the application. These settings include configurations
for mass spectrometry, laser parameters, logging, forms positioning,
database paths, vacuum measurements, and API hosts.

<a id="app_control.load_config"></a>

#### load\_config

```python
def load_config()
```

This function reads configuration data from the config file and attempts
to update the global `settings` dictionary. It uses a nested dictionary structure
to manage settings at multiple levels of hierarchy. If any setting is not
found in the external source, a default value remains. The function ensures that
any changes trigger a call to backup the configuration for persistence.

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

Returns a list of all key values in the SECRETS file.

<a id="app_control.SECRETS"></a>

#### SECRETS

<a id="app_control.settings"></a>

#### settings

