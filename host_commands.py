"""
Commands to the controller APIs
"""
import requests
from logmanager import logger
from settings import settings, alarms


def lasercommand(state):
    """Set laser state (on or off)"""
    message = {"item": 'laser', "command": state}
    try:
        resp = requests.post(settings['hosts']['laserhost'], json=message, timeout=1)
        logger.debug('host_commands: Setting Laser to %s', state)
        alarms['laserhost'] = 0
        return resp.json()
    except requests.RequestException:
        alarms['laserhost'] += 5
        logger.warning('host_commands: Laser Command Timeout Error')
        return {'laser': 'timeout'}


def lasersetpower(power):
    """Set the laser power"""
    message = {"item": 'setlaserpower', "command": power}
    try:
        resp = requests.post(settings['hosts']['laserhost'], json=message, timeout=1)
        logger.debug('host_commands: Setting laser power to %s', settings['laser']['power'])
        alarms['laserhost'] = 0
        settings['laser']['power'] = power
        return resp.json()
    except requests.RequestException:
        logger.warning('host_commands: Laser Set Power Timeout Error')
        alarms['laserhost'] += 5
        return {'laser': 'timeout'}


def valvechange(valve, command):
    """Change a valve state"""
    if command == 1:
        command = 'open'
    elif command == 0:
        command = 'close'
    message = {"item": valve, "command": command}
    try:
        resp = requests.post(settings['hosts']['valvehost'], json=message, timeout=1)
        alarms['valvehost'] = 0
        return resp.json()
    except requests.RequestException:
        logger.warning('host_commands: Valve Change Timeout Error')
        alarms['valvehost'] += 5
        return [{'status': 'timout', 'valve': 1}]


def xymoveto(axis, location):
    """Move the X-Y stage ***axis*** to a position ***loc***"""
    message = {'item': '%smoveto' % axis, "command": location}
    try:
        resp = requests.post(settings['hosts']['xyhost'], json=message, timeout=1)
        alarms['xyhost'] = 0
        return resp.json()
    except requests.RequestException:
        logger.warning('host_commands: X-Y Moveto Timeout Error')
        alarms['xyhost'] += 5
        return {'xmoving': 'timeout', 'xpos': 0, 'ymoving': 'timout', '"ypos': 0}


def xymove(axis, steps):
    """Move the **axis** along **steps**"""
    message = {'item': '%smove' % axis, "command": steps}
    try:
        resp = requests.post(settings['hosts']['xyhost'], json=message, timeout=1)
        alarms['xyhost'] = 0
        return resp.json()
    except requests.RequestException:
        logger.warning('host_commands: X-Y Move Timeout Error')
        alarms['xyhost'] += 5
        return {'xmoving': 'timeout', 'xpos': 0, 'ymoving': 'timout', '"ypos': 0}


def pyrolasercommand(state):
    """enable / disable the rangefinder laser on the pyrometer"""
    message = {"item": 'laser', "command": state}
    try:
        resp = requests.post(settings['hosts']['pumphost'], json=message, timeout=1)
        alarms['pumphost'] = 0
        return resp.json()
    except requests.RequestException:
        logger.warning('host_commands: Pump Command Timeout Error')
        alarms['pumphost'] += 5
        return {'laser': 'timeout'}

def rpi_reboot(host):
    """reboot the raspberry pi"""
    message = {"item": 'restart', "command": 'pi'}
    try:
        resp = requests.post(settings['hosts'][host], json=message, timeout=1)
        logger.info('Rebooting the %s Raspberry Pi', host)
        return resp.json()
    except requests.RequestException:
        logger.warning('host_commands: restart %s', host)
        return {host: 'timeout'}
