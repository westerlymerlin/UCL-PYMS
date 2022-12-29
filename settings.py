import json

version = '2.0.6'
running = True
settings = {}


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
    with open('settings.json', 'w') as outfile:
        json.dump(settings, outfile, indent=4, sort_keys=True)


def initialise():
    global settings
    settings['logging'] = {}
    settings['logging']['logfilepath'] = '.\\logs\\'
    settings['logging']['logappname'] = 'PyMS'
    settings['hosts'] = {}
    settings['hosts']['valvehost'] = 'http://192.168.1.7/api'
    settings['hosts']['xyhost'] = 'http://192.168.1.8/api'
    settings['hosts']['pumphost'] = 'http://192.168.1.6/api'
    settings['database'] = {}
    settings['database']['databasepath'] = '.\\database\\PyMs.db'
    settings['database']['databasebackuppath'] = '.\\database\\PyMs.backup.db'
    settings['database']['resultsdatabasepath'] = '.\\database\\HeliumResults.db'
    settings['database']['resultsdatabasebackuppath'] = '.\\database\\HeliumResults.db.backup.db'
    settings['mainform'] = {}
    settings['mainform']['x'] = 600
    settings['mainform']['y'] = 100
    settings['newbatchform'] = {}
    settings['newbatchform']['x'] = 600
    settings['newbatchform']['y'] = 100
    settings['simplebatchform'] = {}
    settings['simplebatchform']['x'] = 600
    settings['simplebatchform']['y'] = 100
    settings['planchetform'] = {}
    settings['planchetform']['x'] = 600
    settings['planchetform']['y'] = 100
    settings['xymanualform'] = {}
    settings['xymanualform']['x'] = 600
    settings['xymanualform']['y'] = 100
    settings['cycleeditform'] = {}
    settings['cycleeditform']['x'] = 600
    settings['cycleeditform']['y'] = 100
    settings['ncccalcform']['x'] = 600
    settings['ncccalcform']['y'] = 100
    settings['laser'] = {}
    settings['laser']['power'] = 40.0
    settings['laser']['port'] = 'com5'
    settings['laser']['baud'] = 9600
    settings['pyrometer'] = {}
    settings['pyrometer']['current'] = 0
    settings['pyrometer']['low'] = 700
    settings['pyrometer']['high'] = 1200
    settings['vacuum'] = {}
    settings['vacuum']['tank'] = {}
    settings['vacuum']['tank']['current'] = 0
    settings['vacuum']['tank']['high'] = 1e-04
    settings['vacuum']['turbo'] = {}
    settings['vacuum']['turbo']['current'] = 0
    settings['vacuum']['turbo']['high'] = 9.9e-08
    settings['vacuum']['ion'] = {}
    settings['vacuum']['ion']['current'] = 0
    settings['vacuum']['ion']['high'] = 2.1e-09
    settings['image'] = {}
    settings['image']['dynolite'] = 'DinoCapture 2.0'
    settings['image']['microscope'] = 'GXCapture-T'
    settings['image']['microscope-reheat'] = 'GXCapture-T'
    settings['image']['"hiden-mid'] = 'PyMS - Python Mass Spectrometry',
    settings['image']['"hiden-mid-reheat'] = 'PyMS - Python Mass Spectrometry',
    settings['image']['"hiden-profile'] = 'PyMS - Python Mass Spectrometry',
    settings['MassSpec'] = {}
    settings['MassSpec']['nextQ'] = 5000
    settings['MassSpec']['nextH'] = 20000
    settings['MassSpec']['datadirectory'] = '.\\QuadStar\\data\\'
    settings['MassSpec']['hidenhost'] = '192.168.2.100'
    settings['MassSpec']['hidenport'] = 5026
    settings['MassSpec']['timeoutretries'] = 10
    settings['MassSpec']['hidenMID'] = '"C:\\Users\\UCL Helium Line\\Documents\\Hiden ' \
                                       'Analytical\\MASsoft10\\PyMS-MID.exp '
    settings['MassSpec']['hidenProfile'] = '"C:\\Users\\UCL Helium Line\\Documents\\Hiden ' \
                                           'Analytical\\MASsoft10\\PyMS-Profile.exp '
    settings['MassSpec']['hidenRunfile'] = '"C:\\Users\\UCL Helium Line\\Documents\\Hiden ' \
                                           'Analytical\\MASsoft10\\PyMS-Running.exp '
    settings['MassSpec']['multiplier'] = 1E-12
    settings['MassSpec']['HD/H'] = 0.01
    settings['Ncc'] = {}
    settings['Ncc']['HD_H'] = 0.01
    settings['Ncc']['q_dep_factor'] = 0.9999526
    settings['Ncc']['q_depletion_err'] = 0.0000004
    settings['Ncc']['s_dep_factor'] = 0.99996107
    settings['Ncc']['q_pipette_ncc'] = 10.23
    settings['Ncc']['q_pipette_err'] = 0.07
    settings['Ncc']['s_pipette_ncc'] = 5.7
    settings['Ncc']['s_offset'] = 231
    settings['Ncc']['nccfilepath'] = ''

    writesettings()


def readsettings():
    global settings
    try:
        with open('settings.json') as json_file:
            settings = json.load(json_file)
    except FileNotFoundError:
        initialise()


readsettings()
