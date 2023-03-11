from settings import settings, alarms
import requests


def lasergetalarm():
    message = {"item": 'laseralarm', "command": settings['laser']['power']}
    try:
        resp = requests.post(settings['hosts']['laserhost'], json=message, timeout=1)
        alarms['laseralarm'] = resp.json()['status']
        alarms['laserhost'] = 0
        return resp.json()
    except requests.RequestException:
        print('host_queries: Laser Get Alarm Timeout Error')
        alarms['laserhost'] += 1
        return {'alarm': 'timout'}


def lasergetstatus():
    message = {"item": 'laserstatus', "command": settings['laser']['power']}
    try:
        resp = requests.post(settings['hosts']['laserhost'], json=message, timeout=1)
        alarms['laserhost'] = 0
        return resp.json()
    except requests.RequestException:
        print('host_queries: Laser Get Status Timeout Error')
        alarms['laserhost'] += 1
        return {'laser': 'timeout'}

def valvegetstatus():
    message = {"item": 'getstatus', "command": True}
    try:
        resp = requests.post(settings['hosts']['valvehost'], json=message, timeout=1)
        alarms['valvehost'] = 0
        return resp.json()
    except requests.RequestException:
        print('host_queries: Valve Get Status Timeout Error')
        alarms['valvehost'] += 1
        return {{'status': 'timout', 'valve': 1}}


def pressuresread():
    message = {"item": 'getpressures', "command": True}
    try:
        resp = requests.post(settings['hosts']['pumphost'], json=message, timeout=1)
        settings['vacuum']['turbo']['current'] = float(resp.json()[0]['pressure'])
        settings['vacuum']['tank']['current'] = float(resp.json()[1]['pressure'])
        settings['vacuum']['ion']['current'] = float(resp.json()[2]['pressure'])
        alarms['pumphost'] = 0
        return resp.json()
    except requests.RequestException:
        print('host_queries: Get Pressures Pump Reader Timeout Error')
        alarms['pumphost'] += 1
        return {{"pressure": 'timeout', "pump": "turbo"}}


def tempratureread():
    message = {"item": 'gettemperature', "command": True}
    try:
        resp = requests.post(settings['hosts']['pumphost'], json=message, timeout=1)
        settings['pyrometer']['current'] = float(resp.json()['temperature'])
        alarms['pumphost'] = 0
        return resp.json()
    except requests.RequestException:
        print('host_queries: Get Temperature Pump Reader Timeout Error')
        alarms['pumphost'] = 0
        return {"laser": 0, "maxtemp": 0, "temperature": 'timeout'}


def xyread():
    try:
        message = {"item": 'getxystatus', "command": True}
        resp = requests.post(settings['hosts']['xyhost'], json=message, timeout=1)
        alarms['xyhost'] = 0
        return resp.json()
    except requests.RequestException:
        print('host_queries: Get Status X-Y Controller Timeout Error')
        alarms['xyhost'] += 1
        return {"xmoving": 'timeout', "xpos": 0, "ymoving": 'timout', "ypos": 0}
