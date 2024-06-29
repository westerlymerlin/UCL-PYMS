"""
Commands to the controller APIs
"""
import requests
from logmanager import logger
from app_control import settings, alarms


def lasercommand(state):
    """Set laser state (on or off)"""
    message = {"item": 'laser', "command": state}
    headers = {"Accept": "application/json", "api-key": settings['hosts']['laserhost-api-key']}
    try:
        resp = requests.post(settings['hosts']['laserhost'], headers=headers, json=message,
                             timeout=settings['hosts']['timeoutseconds'])
        logger.info('host_commands: Setting Laser to %s', state)
        json_message = resp.json()
        alarms['laserhost'] = 0
        return json_message
    except requests.Timeout:
        alarms['laserhost'] += 5
        logger.warning('host_commands: Laser Command Timeout Error')
        return {'laser': 'timeout'}
    except requests.RequestException:
        alarms['laserhost'] += 5
        logger.exception('host_commands: Laser Command Timeout Error')
        return {'laser': 'exception'}


def lasersetpower(power):
    """Set the laser power"""
    message = {"item": 'setlaserpower', "command": power}
    headers = {"Accept": "application/json", "api-key": settings['hosts']['laserhost-api-key']}
    try:
        resp = requests.post(settings['hosts']['laserhost'], headers=headers, json=message,
                             timeout=settings['hosts']['timeoutseconds'])
        logger.info('host_commands: Setting laser power to %s', settings['laser']['power'])
        json_message = resp.json()
        alarms['laserhost'] = 0
        settings['laser']['power'] = power
        return json_message
    except requests.Timeout:
        logger.warning('host_commands: Laser Set Power Timeout Error')
        alarms['laserhost'] += 5
        return {'laser': 'timeout'}
    except requests.RequestException:
        logger.exception('host_commands: Laser Set Power Exception')
        alarms['laserhost'] += 5
        return {'laser': 'exception'}


def valvechange(valve, command):
    """Change a valve state"""
    if command == 1:
        command = 'open'
    elif command == 0:
        command = 'close'
    message = {"item": valve, "command": command}
    headers = {"Accept": "application/json", "api-key": settings['hosts']['valvehost-api-key']}
    try:
        resp = requests.post(settings['hosts']['valvehost'], headers=headers, json=message,
                             timeout=settings['hosts']['timeoutseconds'])
        json_message = resp.json()
        logger.info('host_commands: %s changed to %s', valve, command)
        alarms['valvehost'] = 0
        return json_message
    except requests.Timeout:
        logger.warning('host_commands: Valve Change Timeout Error valve %s', valve)
        alarms['valvehost'] += 5
        return [{'status': 'timout', 'valve': valve}]
    except requests.RequestException:
        logger.exception('host_commands: Valve Change Exception:')
        alarms['valvehost'] += 5
        return [{'status': 'exception', 'valve': valve}]


def xymoveto(axis, location):
    """Move the X-Y stage ***axis*** to a position ***loc***"""
    message = {'item': '%smoveto' % axis, "command": location}
    headers = {"Accept": "application/json", "api-key": settings['hosts']['xyhost-api-key']}
    try:
        resp = requests.post(settings['hosts']['xyhost'], headers=headers, json=message,
                             timeout=settings['hosts']['timeoutseconds'])
        json_message = resp.json()
        alarms['xyhost'] = 0
        return json_message
    except requests.Timeout:
        logger.warning('host_commands: X-Y Moveto Timeout Error')
        alarms['xyhost'] += 5
        return {'xmoving': 'timeout', 'xpos': 0, 'ymoving': 'timout', '"ypos': 0}
    except requests.RequestException:
        logger.exception('host_commands: X-Y Moveto Exception')
        alarms['xyhost'] += 5
        return {'xmoving': 'exception', 'xpos': 0, 'ymoving': 'exception', '"ypos': 0}


def xymove(axis, steps):
    """Move the **axis** along **steps**"""
    message = {'item': '%smove' % axis, "command": steps}
    headers = {"Accept": "application/json", "api-key": settings['hosts']['xyhost-api-key']}
    try:
        resp = requests.post(settings['hosts']['xyhost'], headers=headers, json=message,
                             timeout=settings['hosts']['timeoutseconds'])
        json_message = resp.json()
        alarms['xyhost'] = 0
        return json_message
    except requests.Timeout:
        logger.warning('host_commands: X-Y Move Timeout Error')
        alarms['xyhost'] += 5
        return {'xmoving': 'timeout', 'xpos': 0, 'ymoving': 'timout', '"ypos': 0}
    except requests.RequestException:
        logger.exception('host_commands: X-Y Move Exception')
        alarms['xyhost'] += 5
        return {'xmoving': 'exception', 'xpos': 0, 'ymoving': 'exception', '"ypos': 0}


def rpi_reboot(host):
    """reboot the raspberry pi"""
    message = {"item": 'restart', "command": 'pi'}
    apikey = host + '-api-key'
    headers = {"Accept": "application/json", "api-key": settings['hosts'][apikey]}
    try:
        resp = requests.post(settings['hosts'][host], headers=headers,
                             json=message, timeout=settings['hosts']['timeoutseconds'])
        logger.info('Rebooting the %s Raspberry Pi', host)
        return resp.json()
    except requests.RequestException:
        logger.exception('host_commands: restart %s', host)
        return {host: 'exception'}
