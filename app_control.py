"""
Settings module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function.
"""

import json
import datetime

VERSION = '3.2.11'
running = True
alarms = {'laserhost': 0, 'valvehost': 0, 'xyhost': 0, 'pumphost': 0, 'hidenhost': 0, 'laseralarm': 133}


def friendlydirname(sourcename: str) -> str:
    """Removes invalid characters from file names"""
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
    """Write settings to json file"""
    settings['LastSave'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with open('settings.json', 'w', encoding='utf-8') as outfile:
        json.dump(settings, outfile, indent=4, sort_keys=True)


def initialise():
    """Setup the settings structure with default values"""
    isettings = {
                "LastSave": "01/01/1900 01:00:00",
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
                    "timeoutseconds": 0.5
                },
                "Ncc": {
                    "HD_H": 0.01,
                    "ncc_filepath": "",
                    "q_dep_factor": 0.9999526,
                    "q_depletion_err": 4e-07,
                    "q_pipette_err": 0.07,
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
                    "laserhost": "http://192.168.2.6/api",
                    "laserhost-api-key": "changeme",
                    "pumphost": "http://192.168.2.5/api",
                    "pumphost-api-key": "changeme",
                    "valvehost": "http://192.168.2.3/api",
                    "valvehost-api-key": "changeme",
                    "xyhost": "http://192.168.2.4/api",
                    "xyhost-api-key": "changeme",
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
                    "power": 00.0
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
                "simplebatchform": {
                    "x": 600,
                    "y": 100
                },
                "vacuum": {
                    "ion": {
                        "current": 4.5e-09,
                        "high": 9.9e-08
                    },
                    "tank": {
                        "current": 0.00116,
                        "high": 0.0001
                    },
                    "turbo": {
                        "current": 3.41e-08,
                        "high": 9.9e-08
                    }
                },
                "xymanualform": {
                    "x": 1137,
                    "y": 870
                }
            }
    return isettings


def readsettings():
    """Read the json file"""
    try:
        with open('settings.json', 'r', encoding='utf-8') as json_file:
            jsettings = json.load(json_file)
            return jsettings
    except FileNotFoundError:
        print('File not found - settings.json')
        return {}


def loadsettings():
    """Replace the default settings with thsoe from the json files"""
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


settings = initialise()
loadsettings()
