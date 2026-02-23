"""
Application Control module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function. Has global variables and routine for
calculating a file name and removing illegal character.
"""

from shutil import copyfile
import json
from base64 import b64decode, b64encode
import datetime

VERSION = '3.3.2'
running = True
alarms = {'laserhost': 0, 'valvehost': 0, 'xyhost': 0, 'pumphost': 0, 'hidenhost': 0, 'laseralarm': 133}


def friendlydirname(sourcename: str) -> str:
    """
    Transforms a given string into a filesystem-friendly directory name.

    This function modifies the input string by replacing invalid characters with a dash ('-')
    to ensure the string adheres to naming conventions suitable for directory/file storage.
    It also removes consecutive dashes created as a result of replacing invalid characters.
    """
    invalid_chars = ['/', '\\', ':', '*', '?', '<', '>', '"', '&', '%', '#', '$', "'", ',']
    for invalid_char in invalid_chars:
        sourcename = sourcename.replace(invalid_char, '-')
    # Remove subsequent dash characters effectively
    while '--' in sourcename:
        sourcename = sourcename.replace('--', '-')
    return sourcename


def setrunning(state):
    """Global signal to detect if app is running - used to kill off threads"""
    global running
    running = state


def writesettings():
    """
    Writes and saves the current settings to a JSON file.

    This function updates the 'LastSave' field in the settings dictionary with the
    current date and time in the format 'DD/MM/YYYY HH:MM:SS' and writes the
    updated dictionary to a file named 'settings.json'. The JSON file is saved
    with UTF-8 encoding and is formatted with an indent of 4 spaces and keys sorted
    in ascending order.
    """
    settings['LastSave'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with open('settings.json', 'w', encoding='utf-8') as outfile:
        json.dump(settings, outfile, indent=4, sort_keys=True)


def initialise():
    """
    Initializes the application settings and configurations.

    This function creates and returns a dictionary containing all default
    settings used in the application. These settings include configurations
    for mass spectrometry, laser parameters, logging, forms positioning,
    database paths, vacuum measurements, and API hosts.
    """
    isettings = {
        "LastSave": "01/01/1900 01:00:00",
        "app-name": "UCL PyMs",
        "email_recipients": "",
        "MassSpec": {
            "HD/H": 0.01,
            "datadirectory": "C:\\Users\\UCL Helium Line\\Documents\\Helium Line Data\\",
            "hidenMID": "C:\\Users\\UCL Helium Line\\Documents\\Hiden Analytical\\MASsoft10\\PyMS-MID.exp",
            "hidenProfile": "C:\\Users\\UCL Helium Line\\Documents\\Hiden Analytical\\MASsoft10\\PyMS-Profile.exp",
            "hidenRunfile": "C:\\Users\\UCL Helium Line\\Documents\\Hiden Analytical\\MASsoft10\\PyMS-Running.exp",
            "hidenhost": "127.0.0.1",
            "hidenport": 5026,
            "multiplier": 1e-12,
            "nextH": "HE19096R",
            "nextQ": 4500,
            "timeoutretries": 5,
            "timeoutseconds": 1.0,
            "socket_wait": 0.5
        },
        "Ncc": {
            "HD_H": 0.01,
            "ncc_filepath": "",
            "q_dep_factor": 0.9999526,
            "q_depletion_err": 4e-07,
            "q_pipette_err": 0.07,
            "q_offset": 0,
            "q_pipette_ncc": 10.23,
            "s_dep_factor": 0.99996107,
            "s_offset": 231,
            "s_pipette_ncc": 5.7,
            "ncc_start_seconds": 30
        },
        "cycleeditform": {
            "x": 100,
            "y": 100
        },
        "database": {
            "databasepath": ".\\database\\PyMs.db",
            "resultsdatabasepath": ".\\database\\HeliumResults.db"
        },
        "hosts": {
            "laserhost": "https://192.168.2.6/api",
            "pumphost": "https://192.168.2.5/api",
            "valvehost": "https://192.168.2.3/api",
            "xyhost": "https://192.168.2.4/api",
            "timeoutseconds": 1
        },
        "image": {
            "dynolite": "DinoCapture 2.0",
            "hiden-mid": "MASsoft 10 Professional",
            "hiden-mid-reheat": "MASsoft 10 Professional",
            "hiden-profile": "MASsoft 10 Professional",
            "microscope": "GXCapture-T",
            "microscope-reheat": "GXCapture-T"
        },
        "laser": {
            "power": 00.0,
            "ignorestatus": 1
        },
        "laserform": {
            "x": 100,
            "y": 100
        },
        "logging": {
            "logappname": "PyMS",
            "logfilepath": ".\\logs\\",
            "level": "INFO"
        },
        "mainform": {
            "x": 100,
            "y": 100
        },
        "ncccalcform": {
            "x": 100,
            "y": 100
        },
        "newbatchform": {
            "x": 600,
            "y": 100
        },
        "planchetform": {
            "x": 600,
            "y": 100
        },
        "manualbatchform": {
            "x": 600,
            "y": 100
        },
        "vacuum": {
            "ion": {
                "current": 4.5e-09,
                "high": 9.9e-08,
                "units": "mbar"
            },
            "tank": {
                "current": 0.00116,
                "high": 0.0001,
                "units": "mbar"
            },
            "turbo": {
                "current": 3.41e-08,
                "high": 9.9e-08,
                "units": "mbar"
            },
            "N2": {"current": 1,
                   "high": 9.0,
                   "low": 5.0,
                   "units": "bar"
                   }
        },
        "xymanualform": {
            "x": 1137,
            "y": 870
        }
    }
    return isettings


def readsettings():
    """
    Reads settings from a JSON file and loads them into a dictionary.

    This function attempts to read a JSON configuration file named 'settings.json'
    from the current working directory. If the file is successfully found and read,
    it returns the parsed JSON data as a dictionary. If the file does not exist,
    it returns an empty dictionary.
    """
    try:
        with open('settings.json', 'r', encoding='utf-8') as json_file:
            jsettings = json.load(json_file)
            return jsettings
    except FileNotFoundError:
        print('File not found - settings.json')
        return {}


def loadsettings():
    """
    This function reads configuration settings from an external source using the `readsettings`
    function and updates the global `settings` dictionary. It handles multi-level dictionary
    structures by iterating through their keys and updating corresponding values if found in
    the external settings. If a key is missing in the external source, a message is printed,
    and the current value in `settings` remains unchanged.

    """
    global settings
    fsettings = readsettings()
    for item in settings.keys():
        if isinstance(settings[item], dict):
            for subitem in settings[item]:
                if isinstance(settings[item][subitem], dict):
                    for subsubitem in settings[item][subitem]:
                        try:
                            settings[item][subitem][subsubitem] = fsettings[item][subitem][subsubitem]
                            # print('settings[%s][%s][%s] = %s' % (item, subitem, subsubitem, settings[item][subitem][subsubitem]))
                        except KeyError:
                            print('settings[%s][%s][%s] Not found in json file' % (item, subitem, subsubitem))
                else:
                    try:
                        settings[item][subitem] = fsettings[item][subitem]
                        # print('settings[%s][%s] = %s' % (item, subitem, settings[item][subitem]))
                    except KeyError:
                        print('settings[%s][%s] Not found in json file' % (item, subitem))
        else:
            try:
                settings[item] = fsettings[item]
                # print('settings[%s] = %s' % (item, settings[item]))
            except KeyError:
                print('settings[%s] Not found in json file using default' % item)

def load_secrets():
    """
    Load secrets from a file and decode them.

    This function reads a file named 'SECRETS', decodes its contents using Base64,
    and then parses the resulting JSON. It is used to securely retrieve stored
    configuration or sensitive data. The file is expected to contain secrets
    encoded in a specific format.
    """
    try:
        with open('SECRETS', 'r', encoding='utf-8') as s_file:
            raw_secrets = s_file.read()
        s_file.close()
        return json.loads(b64decode(raw_secrets))
    except FileNotFoundError:
        print('SECRETS file not found - using empty secrets')
        return {}

def update_secret(key, value):
    """
    Updates the secret storage by adding or updating a key-value pair. The method also creates a
    backup of the existing storage file before writing the updated encoded secrets back to the file.
    """
    global SECRETS
    SECRETS[key] = value
    new_secret = b64encode(json.dumps(SECRETS).encode('utf-8')).decode('utf-8')
    copyfile('SECRETS', 'SECRETS.bak')
    with open('SECRETS', 'w', encoding='utf-8') as s_file:
        s_file.write(new_secret)
    s_file.close()

def list_secret_keys():
    """Prints a list of all secret keys in the SECRETS file."""
    return(list(SECRETS.keys()))

SECRETS = load_secrets()
settings = initialise()
loadsettings()

