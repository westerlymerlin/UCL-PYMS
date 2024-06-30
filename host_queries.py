"""
Queries to the controller APIs
"""
import requests
from app_control import settings, alarms
from logmanager import logger


def lasergetalarm():
    """Get laser alarms"""
    message = {"item": 'laseralarm', "command": 1}
    headers = {"Accept": "application/json", "api-key": settings['hosts']['laserhost-api-key']}
    logger.debug('host_queries: get laser alarm')
    try:
        resp = requests.post(settings['hosts']['laserhost'], headers=headers, json=message,
                             timeout=settings['hosts']['timeoutseconds'])
        json_message = resp.json()
        alarms['laserhost'] = 0
        logger.debug('host_queries: Laser alarm responce = %s', resp.json())
        if settings['laser']['ignorestatus'] == 1:
            json_message['status'] = 133
        return json_message
    except requests.Timeout:
        logger.warning('host_queries: Laser Get Alarm Timeout Error')
        alarms['laserhost'] += 1
        return {'alarm': 'exception'}
    except requests.RequestException:
        logger.exception('host_queries: Laser Get Alarm Exception')
        alarms['laserhost'] += 1
        return {'alarm': 'exception'}

def lasergetstatus():
    """Get laser status"""
    message = {"item": 'laserstatus', "command": 1}
    headers = {"Accept": "application/json", "api-key": settings['hosts']['laserhost-api-key']}
    try:
        resp = requests.post(settings['hosts']['laserhost'], headers=headers, json=message,
                             timeout=settings['hosts']['timeoutseconds'])
        json_message = resp.json()
        alarms['laserhost'] = 0
        return json_message
    except requests.Timeout:
        logger.warning('host_queries: Laser Get Status Timeout Error')
        alarms['laserhost'] += 1
        return {'laser': 'exception'}
    except requests.RequestException:
        logger.exception('host_queries: Laser Get Status Exception')
        alarms['laserhost'] += 1
        return {'laser': 'exception'}

def valvegetstatus():
    """Get valve status"""
    message = {"item": 'getstatus', "command": True}
    headers = {"Accept": "application/json", "api-key": settings['hosts']['valvehost-api-key']}
    try:
        resp = requests.post(settings['hosts']['valvehost'], headers=headers, json=message,
                             timeout=settings['hosts']['timeoutseconds'])
        json_message = resp.json()
        alarms['valvehost'] = 0
        return json_message
    except requests.Timeout:
        logger.warning('host_queries: Valve Get Status Timeout Error')
        alarms['valvehost'] += 1
        return [{"status": "exception", "valve": 0}]
    except requests.RequestException:
        logger.exception('host_queries: Valve Get Status Exception')
        alarms['valvehost'] += 1
        return [{"status": "exception", "valve": 0}]

def pressuresread():
    """Get guage pressures"""
    message = {"item": 'getpressures', "command": True}
    headers = {"Accept": "application/json", "api-key": settings['hosts']['pumphost-api-key']}
    try:
        resp = requests.post(settings['hosts']['pumphost'], headers=headers, json=message,
                             timeout=settings['hosts']['timeoutseconds'])
        json_message = resp.json()
        settings['vacuum']['turbo']['current'] = float(json_message[0]['pressure'])
        settings['vacuum']['turbo']['units'] = json_message[0]['units']
        settings['vacuum']['tank']['current'] = float(json_message[1]['pressure'])
        settings['vacuum']['tank']['units'] = json_message[1]['units']
        settings['vacuum']['ion']['current'] = float(json_message[2]['pressure'])
        settings['vacuum']['ion']['units'] = json_message[2]['units']
        settings['vacuum']['N2']['current'] = float(json_message[3]['pressure'])
        settings['vacuum']['N2']['units'] = json_message[3]['units']
        alarms['pumphost'] = 0
        return json_message
    except requests.Timeout:
        logger.warning('host_queries: Get Pressures Pump Reader Timeout Error')
        alarms['pumphost'] += 1
        return {"pressure": 'exception', "pump": "turbo"}
    except requests.RequestException:
        logger.exception('host_queries: Get Pressures Pump Reader Exception')
        alarms['pumphost'] += 1
        return {"pressure": 'exception', "pump": "turbo"}

def xyread():
    """Get X Y Positions"""
    message = {"item": 'getxystatus', "command": True}
    headers = {"Accept": "application/json", "api-key": settings['hosts']['xyhost-api-key']}
    try:
        resp = requests.post(settings['hosts']['xyhost'], headers=headers, json=message,
                             timeout=settings['hosts']['timeoutseconds'])
        json_message = resp.json()
        alarms['xyhost'] = 0
        return json_message
    except requests.Timeout:
        logger.warning('host_queries: Get Status X-Y Controller Timeout Error')
        alarms['xyhost'] += 1
        return {"xmoving": 'exception', "xpos": 0, "ymoving": 'exception', "ypos": 0}
    except requests.RequestException:
        logger.exception('host_queries: Get Status X-Y Controller Exception')
        alarms['xyhost'] += 1
        return {"xmoving": 'exception', "xpos": 0, "ymoving": 'exception', "ypos": 0}
