"""
Hardware Query Interface Module
Author: Gary Twinn

This module provides query functions for retrieving status and data from various hardware
components in the mass spectrometry system. It handles communication with multiple host
controllers to obtain real-time information about system state and measurements.

Key Functions:
- lasergetalarm: Retrieves alarm status from the laser system
- lasergetstatus: Gets current status information from the laser controller
- valvegetstatus: Queries valve states and configuration from the valve controller
- pressuresread: Reads pressure measurements from various system components
- xyread: Obtains current X-Y stage position and movement status

The module handles network communication with hardware hosts, manages timeouts and
exceptions, and provides consistent data structures for system status information.
All functions return structured data that can be used by the main application for
monitoring and control purposes.

This module works in conjunction with host_commands.py to provide complete hardware
interface functionality for the mass spectrometry automation system.
"""
import requests
from app_control import settings, alarms
from logmanager import logger


def lasergetalarm():
    """
    Fetches the current alarm status from the laser host API.

    This function sends a POST request to the laser host with a predefined message.
    The response is parsed as JSON to determine the laser alarm status.
    If an exception occurs during the request, a default dictionary indicating
    an alarm exception is returned.

    Returns:
        dict: Parsed JSON response containing the alarm status or an alarm
        exception on failure.

    Raises:
        requests.Timeout: If the request to the laser host API times out.
        requests.RequestException: If there is an exception while making the
        request to the laser host API.
    """
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
    """
    Get the status of the laser from the laser host.

    This function sends a request to a specified laser host to retrieve the laser's status.
    It handles timeout and request-related exceptions, providing robust error handling and
    logging mechanisms. The method interacts with external APIs and updates the alarms
    dictionary to monitor the state of the laser host's connection reliability.

    Returns:
        dict: A JSON response containing the laser status. If an exception occurs, it
        returns a dictionary with the key 'laser' set to 'exception'.

    Raises:
        Timeout: If the request to the laser host exceeds the configured timeout.
        RequestException: For issues such as connection errors or invalid responses.
    """
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
    """
    Send a request to the valve host to retrieve the status of all valves.

    This function communicates with the valve host API to fetch the status of
    valves. It sends a request with the appropriate headers and command, processes
    the response, and returns the status of each valve. If there is a timeout or
    another exception during the request, the function logs the error, increments
    the alarm count for the valve host, and returns a fallback status.

    Returns:
        list[int] | int: A list of integers indicating the status of each valve,
        where 1 means the valve is open and 0 means it is closed. If an error
        occurs, the function returns 1 instead.

    Raises:
        requests.Timeout: If the request to the valve host times out.
        requests.RequestException: If there is an exception during the request.

    Notes:
        - This function relies on a global `settings` variable that provides
          configuration details for the valve host, including its API key,
          URL, and timeout settings.
        - It also interacts with global `logger` and `alarms` objects for
          logging and alarm tracking purposes.
    """
    message = {"item": 'getstatus', "command": True}
    headers = {"Accept": "application/json", "api-key": settings['hosts']['valvehost-api-key']}
    statusmessage = [0] * 16
    try:
        resp = requests.post(settings['hosts']['valvehost'], headers=headers, json=message,
                             timeout=settings['hosts']['timeoutseconds'])
        json_message = resp.json()
        alarms['valvehost'] = 0
        for item in json_message:
            if item['status'] == 'open':
                statusmessage[item['valve']] = 1
            else:
                statusmessage[item['valve']] = 0
        return statusmessage
    except requests.Timeout:
        logger.warning('host_queries: Valve Get Status Timeout Error')
        alarms['valvehost'] += 1
        return 1
    except requests.RequestException:
        logger.exception('host_queries: Valve Get Status Exception')
        alarms['valvehost'] += 1
        return 1

def pressuresread():
    """
    Fetches and updates vacuum pressure readings from the pump host.

    This function sends a POST request to a pump host to retrieve the current
    pressure readings for various vacuum components (turbo, tank, ion, and N2).
    It updates global settings with the retrieved data. It also handles specific
    timeout and general request exceptions by logging the errors and updating
    alarm counters.

    Raises:
        requests.Timeout: If the request to the pump host times out.
        requests.RequestException: For any other request-related exceptions.

    Returns:
        dict: The JSON message containing vacuum pressure readings if successful.
        In case of an exception, returns a dictionary with exception details.
    """
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
    """
    Sends a request to retrieve the status of the X-Y controller and handles
    response or exceptions.

    Tries to POST a message to the specified X-Y host using the API key
    authentication and returns the JSON response if successful. In case
    of timeout or any request-related exceptions, it logs warnings or
    exceptions, increments the alarm state for the X-Y host, and returns
    a default response indicating an exceptional state.

    Returns:
        dict: A dictionary containing the status of the X-Y controller, which
              includes keys like "xmoving", "xpos", "ymoving", and "ypos".

    Raises:
        requests.Timeout: If the POST request to the X-Y host times out.
        requests.RequestException: For other request-related exceptions.
    """
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
