import json

version = '1.2.4'
running = True
settings = {}


def friendlydirname(sourcename):
    sourcename = sourcename.replace('/', '-')
    sourcename = sourcename.replace('\\', '-')
    sourcename = sourcename.replace(':', '-')
    sourcename = sourcename.replace('*', '-')
    sourcename = sourcename.replace('?', '-')
    sourcename = sourcename.replace('<', '-')
    sourcename = sourcename.replace('>', '-')
    sourcename = sourcename.replace('"', '-')
    sourcename = sourcename.replace('&', '-')
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
    settings['laser'] = {}
    settings['laser']['power'] = 25
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
    settings['image']['dyno'] = 'Dynolite'
    settings['image']['microscope'] = 'HDAVGrabber'
    settings['image']['quadstar'] = '[M1] PyMS QUADSTAR 32-bit Measurement - [Process]'
    settings['image']['microscope-reheat'] = 'HDAVGrabber'
    settings['image']['quadstar-reheat'] = '[M1] PyMS QUADSTAR 32-bit Measurement - [Process]'
    settings['MassSpec'] = {}
    settings['MassSpec']['nextQ'] = 4462
    settings['MassSpec']['nextH'] = 17103
    settings['MassSpec']['datadirectory'] = '.\\QuadStar\\data\\'
    settings['MassSpec']['readfile'] = 'C:\\QS422\\DAT\\pymscyc.mdc'
    settings['MassSpec']['multiplier'] = 1E-12
    settings['MassSpec']['HD/H'] = 0.01
    writesettings()


def readsettings():
    global settings
    try:
        with open('settings.json') as json_file:
            settings = json.load(json_file)
    except FileNotFoundError:
        initialise()


readsettings()
