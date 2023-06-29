import json
import datetime

version = '2.3.2'
running = True
alarms = {'laserhost': 0, 'valvehost': 0, 'xyhost': 0, 'pumphost': 0, 'hidenhost': 0, 'laseralarm': 133}

def friendlydirname(sourcename):
    sourcename = sourcename.replace('/', '-')
    sourcename = sourcename.replace('\\', '-')
    sourcename = sourcename.replace(':', '-')
    sourcename = sourcename.replace('*', '-')
    sourcename = sourcename.replace('?', 'Q')
    sourcename = sourcename.replace('<', '-')
    sourcename = sourcename.replace('>', '-')
    sourcename = sourcename.replace('"', '-')
    sourcename = sourcename.replace('&', '-')
    sourcename = sourcename.replace('%', '-')
    sourcename = sourcename.replace('#', '-')
    sourcename = sourcename.replace('$', '-')
    sourcename = sourcename.replace("'", '-')
    sourcename = sourcename.replace(',', '.')
    sourcename = sourcename.replace('--', '-')
    sourcename = sourcename.replace('--', '-')
    sourcename = sourcename.replace('--', '-')
    return sourcename


def setrunning(state):
    global running
    running = state


def writesettings():
    settings['LastSave'] = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
    with open('settings.json', 'w') as outfile:
        json.dump(settings, outfile, indent=4, sort_keys=True)


def initialise():
    isettings = {}
    isettings['LastSave'] = '01/01/2000 00:00:01'
    isettings['MassSpec'] = {}
    isettings['MassSpec']['HD/H'] = 0.01
    isettings['MassSpec']['datadirectory'] = '.\\QuadStar\\data\\'
    isettings['MassSpec']['hidenMID'] = 'PyMS-MID.exp'
    isettings['MassSpec']['hidenProfile'] = 'PyMS-Profile.exp'
    isettings['MassSpec']['hidenRunfile'] = 'PyMS-Running.exp'
    isettings['MassSpec']['hidenhost'] = '127.0.0.1'
    isettings['MassSpec']['hidenport'] = 5026
    isettings['MassSpec']['multiplier'] = 1E-12
    isettings['MassSpec']['nextH'] = 'HE00000R'
    isettings['MassSpec']['nextQ'] = 1000
    isettings['MassSpec']['startimeoffset'] = 15
    isettings['MassSpec']['timeoutretries'] = 10
    isettings['Ncc'] = {}
    isettings['Ncc']['HD_H'] = 0.01
    isettings['Ncc']['ncc_filepath'] = ''
    isettings['Ncc']['q_dep_factor'] = 0.9999526
    isettings['Ncc']['q_depletion_err'] = 4E-7
    isettings['Ncc']['q_pipette_err'] = 0.07
    isettings['Ncc']['q_pipette_ncc'] = 10.23
    isettings['Ncc']['s_dep_factor'] = 0.99996107
    isettings['Ncc']['s_offset'] = 231
    isettings['Ncc']['s_pipette_ncc'] = 5.7
    isettings['cycleeditform'] = {}
    isettings['cycleeditform']['x'] = 600
    isettings['cycleeditform']['y'] = 100
    isettings['database'] = {}
    isettings['database']['databasebackuppath'] = '.\\database\\PyMs.backup.db'
    isettings['database']['databasepath'] = '.\\database\\PyMs.db'
    isettings['database']['resultsdatabasebackuppath'] = '.\\database\\HeliumResults.db.backup.db'
    isettings['database']['resultsdatabasepath'] = '.\\database\\HeliumResults.db'
    isettings['hosts'] = {}
    isettings['hosts']['laserhost'] = 'http://192.168.1.9/api'
    isettings['hosts']['pumphost'] = 'http://192.168.1.6/api'
    isettings['hosts']['valvehost'] = 'http://192.168.1.7/api'
    isettings['hosts']['xyhost'] = 'http://192.168.1.8/api'
    isettings['image'] = {}
    isettings['image']['dynolite'] = 'DinoCapture 2.0'
    isettings['image']['hiden-mid'] = 'PyMS - Python Mass Spectrometry'
    isettings['image']['hiden-mid-reheat'] = 'PyMS - Python Mass Spectrometry'
    isettings['image']['hiden-profile'] = 'PyMS - Python Mass Spectrometry'
    isettings['image']['microscope'] = 'GXCapture-T'
    isettings['image']['microscope-reheat'] = 'GXCapture-T'
    isettings['laser'] = {}
    isettings['laser']['power'] = 40.0
    isettings['logging'] = {}
    isettings['logging']['logappname'] = 'PyMS'
    isettings['logging']['logfilepath'] = '.\\logs\\'
    isettings['mainform'] = {}
    isettings['mainform']['x'] = 600
    isettings['mainform']['y'] = 100
    isettings['ncccalcform'] = {}
    isettings['ncccalcform']['x'] = 600
    isettings['ncccalcform']['y'] = 100
    isettings['newbatchform'] = {}
    isettings['newbatchform']['x'] = 600
    isettings['newbatchform']['y'] = 100
    isettings['planchetform'] = {}
    isettings['planchetform']['x'] = 600
    isettings['planchetform']['y'] = 100
    isettings['pyrometer'] = {}
    isettings['pyrometer']['current'] = 0
    isettings['pyrometer']['high'] = 1200
    isettings['pyrometer']['low'] = 700
    isettings['simplebatchform'] = {}
    isettings['simplebatchform']['x'] = 600
    isettings['simplebatchform']['y'] = 100
    isettings['vacuum'] = {}
    isettings['vacuum']['ion'] = {}
    isettings['vacuum']['ion']['current'] = 0
    isettings['vacuum']['ion']['high'] = 2.1e-09
    isettings['vacuum']['tank'] = {}
    isettings['vacuum']['tank']['current'] = 0
    isettings['vacuum']['tank']['high'] = 1e-04
    isettings['vacuum']['turbo'] = {}
    isettings['vacuum']['turbo']['current'] = 0
    isettings['vacuum']['turbo']['high'] = 9.9e-08
    isettings['xymanualform'] = {}
    isettings['xymanualform']['x'] = 600
    isettings['xymanualform']['y'] = 100
    return isettings
    # writesettings()


def readsettings():
    try:
        with open('settings.json') as json_file:
            jsettings = json.load(json_file)
            return jsettings
    except FileNotFoundError:
        print('File not found')
        return {}


def loadsettings():
    global settings
    fsettings = readsettings()
    for item in settings.keys():
        if type(settings[item]) == dict:
            for subitem in settings[item]:
                if type(settings[item][subitem]) == dict:
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
