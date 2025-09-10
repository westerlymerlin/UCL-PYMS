# None

<a id="host_commands"></a>

# host\_commands

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

<a id="host_commands.requests"></a>

## requests

<a id="host_commands.logger"></a>

## logger

<a id="host_commands.settings"></a>

## settings

<a id="host_commands.alarms"></a>

## alarms

<a id="host_commands.lasercommand"></a>

#### lasercommand

```python
def lasercommand(state)
```

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

<a id="host_commands.lasersetpower"></a>

#### lasersetpower

```python
def lasersetpower(power)
```

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

<a id="host_commands.valvechange"></a>

#### valvechange

```python
def valvechange(valve, command)
```

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

<a id="host_commands.xymoveto"></a>

#### xymoveto

```python
def xymoveto(axis, location)
```

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

<a id="host_commands.xymove"></a>

#### xymove

```python
def xymove(axis, steps)
```

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

