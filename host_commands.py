
"""
Host Commands Module - Hardware Control Interface

This module provides command functions for controlling various hardware components
in the PyMS (Python Mass Spectrometry) system. It includes functions for:

- Laser control and power management
- Valve operations and state changes
- XY positioning system movement and positioning
- Communication with hardware controllers

These functions serve as the interface layer between the PyMS application
and the underlying hardware systems, handling the low-level command protocols
and hardware-specific communication.

Author: Gary Twinn
"""
import requests
from logmanager import logger
from app_control import settings, alarms, SECRETS


def lasercommand(state):
    """
    Sends a command to the laser system to either activate or deactivate it by communicating
    with the laserhost API. Handles potential errors during the communication.

    Parameters:
    state (str): The desired state of the laser ('on' or 'off').

    Returns:
    dict: The response message from the laserhost API. In case of timeout or request
          exceptions, the returned dictionary indicates the error type:
          {'laser': 'timeout'} for timeout errors and {'laser': 'exception'} for general
          request exceptions.

    Raises:
    requests.Timeout: If the request to the laserhost API takes too long to complete.
    requests.RequestException: For general request-related errors.
    """
    message = {"item": 'laser', "command": state}
    headers = {"Accept": "application/json", "api-key": SECRETS['laserhost-api-key']}
    try:
        resp = requests.post(settings['hosts']['laserhost'], headers=headers, json=message,
                             timeout=settings['hosts']['timeoutseconds'], verify='cacerts')
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
    """
    Sets the power level of the laser device by sending a command to the laser host.

    This function sends a POST request to the laser host, instructing it to set the laser
    power to the specified level. It uses the laserhost API key for authentication and
    handles network errors such as timeouts or exceptions. On success, it updates the
    stored laser power setting and resets alarms related to the laser host. Errors
    result in corresponding updates to the laserhost alarm counter and return appropriate
    error messages.

    Args:
        power (int): The desired laser power level to set.

    Returns:
        dict: A JSON response from the laser host API. If the request was successful, it
        contains the response data from the server. On error, it contains a message
        indicating a timeout or exception.
    """
    message = {"item": 'setlaserpower', "command": power}
    headers = {"Accept": "application/json", "api-key": SECRETS['laserhost-api-key']}
    try:
        resp = requests.post(settings['hosts']['laserhost'], headers=headers, json=message,
                             timeout=settings['hosts']['timeoutseconds'], verify='cacerts')
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
    """
    Sends a command to change the state of a specified valve by utilizing an API request.

    Parameters:
    valve : str
        The identifier of the valve whose state is to be modified.
    command : int
        The command to execute on the valve (1 for 'open', 0 for 'close').

    Returns:
    list
        A list containing the response JSON from the API call in success scenarios.
        In case of a timeout or exception, it contains the status of the failure and the valve identifier.

    Raises:
    requests.Timeout
        If the request times out before receiving a response.
    requests.RequestException
        If there is an error in sending the request or receiving the response.
    """
    if command == 1:
        command = 'open'
    elif command == 0:
        command = 'close'
    message = {"item": valve, "command": command}
    headers = {"Accept": "application/json", "api-key": SECRETS['valvehost-api-key']}
    try:
        resp = requests.post(settings['hosts']['valvehost'], headers=headers, json=message,
                             timeout=settings['hosts']['timeoutseconds'], verify='cacerts')
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
    """
    Moves the specified axis to the given location.

    This function sends a request to move a specific axis (X or Y) to the given
    location. It communicates with the server using a POST request and handles
    timeouts or other exceptions during the communication. In case of an error,
    appropriate alarms are incremented and default error responses are returned.

    Arguments:
        axis (str): The axis to move, e.g., 'x' or 'y'.
        location (int): The position to move the specified axis to.

    Returns:
        dict: A dictionary containing the response from the server. On success,
        it includes updated position information for the axis. On error or
        timeout, it includes error indicators and default positions.

    Raises:
        requests.Timeout: If the request to the server times out.
        requests.RequestException: If the request to the server fails due to
        other reasons.
    """
    message = {'item': '%smoveto' % axis, "command": location}
    headers = {"Accept": "application/json", "api-key": SECRETS['xyhost-api-key']}
    try:
        resp = requests.post(settings['hosts']['xyhost'], headers=headers, json=message,
                             timeout=settings['hosts']['timeoutseconds'], verify='cacerts')
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
    """
    Sends a command to move an axis (X or Y) by the specified number of steps.

    The function constructs a movement command and sends it as a POST request to the configured
    XY host endpoint. It handles timeout and other request exceptions, logging appropriate
    warnings or exceptions and updating alarm counters accordingly. The response from the XY
    host is returned as a JSON object.

    Parameters:
        axis (str): The axis to move, typically 'x' or 'y'.
        steps (int): The number of steps to move the specified axis.

    Returns:
        dict: A JSON object received from the host indicating motion status and current axis
        positions or a default response in case of errors.

    Raises:
        requests.Timeout: If the request to the host endpoint times out.
        requests.RequestException: If a general request error occurs.
    """
    message = {'item': '%smove' % axis, "command": steps}
    headers = {"Accept": "application/json", "api-key": SECRETS['xyhost-api-key']}
    try:
        resp = requests.post(settings['hosts']['xyhost'], headers=headers, json=message,
                             timeout=settings['hosts']['timeoutseconds'], verify='cacerts')
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
