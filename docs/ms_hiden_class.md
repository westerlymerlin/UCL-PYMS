# None

<a id="ms_hiden_class"></a>

# ms\_hiden\_class

Class to read data from a Hiden Mass Spectrometer and calculate the best-fit value for t=0

<a id="ms_hiden_class.socket"></a>

## socket

<a id="ms_hiden_class.datetime"></a>

## datetime

<a id="ms_hiden_class.os"></a>

## os

<a id="ms_hiden_class.threading"></a>

## threading

<a id="ms_hiden_class.time"></a>

## time

<a id="ms_hiden_class.sqlite3"></a>

## sqlite3

<a id="ms_hiden_class.settings"></a>

## settings

<a id="ms_hiden_class.writesettings"></a>

## writesettings

<a id="ms_hiden_class.friendlydirname"></a>

## friendlydirname

<a id="ms_hiden_class.alarms"></a>

## alarms

<a id="ms_hiden_class.linbestfit"></a>

## linbestfit

<a id="ms_hiden_class.logger"></a>

## logger

<a id="ms_hiden_class.MsClass"></a>

## MsClass Objects

```python
class MsClass()
```

Class representing a Hiden Mass Spectrometer.

Attributes:
- __resultstabasepath: str - the path to the results database
- __midfile: str - the name of the Hiden MID file
- __profilefile: str - the name of the Hiden profile file
- __runfile: str - the name of the run file
- __host: str - the host of the Hiden Mass Spectrometer
- __port: int - the port of the Hiden Mass Spectrometer
- __multiplier: float - the multiplier used in calculations
- timeoutretries: int - the maximum number of timeout retries
- time: list - a list of time values
- m1: list - a list of m1 values
- m3: list - a list of m3 values
- m4: list - a list of m4 values
- m5: list - a list of m5 values
- m40: list - a list of m40 values
- m6: list - a list of m6 values
- bestfit: int - the best fit value
- id: str - the MS file ID in the format HEnnnnnR
- type: str - the file type
- filename: str - the file name
- identifier: str - the sample identifier
- daterun: datetime - the date and time the run was started
- batchdescription: str - the batch description
- batchid: int - the batch ID
- batchitemid: int - the batch item ID
- socketreturn: int - the return value from the socket
- running: bool - indicates whether the run is currently in progress
- timeoutcounter: int - counter for the number of timeouts

Methods:
- command_parser(command: str) -> int: Processes a command for the quad target
- resetclass(): Resets class variables to their default values
- starttimer(batchtype: str, identifier: str, batchdescription: str, batchid: int, batchitemid: int): Starts a timer
- check_quad_is_online() -> str: Self test to check if the quad is online and ready
- start_mid() -> List[str]: Starts a multiple ion detection run on the Hiden Mass Spectrometer
- start_profile() -> List[str]: Starts a 1 to 10 amu scan on the Hiden Mass Spectrometer
- getdata() -> List[List[str]]: Requests mid data from the Hiden Mass Spectrometer
- getcolumns() -> List[str]: Requests columns from the Hiden Mass Spectrometer
- getcycle(): Requests cycles from the Hiden Mass Spectrometer

<a id="ms_hiden_class.MsClass.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="ms_hiden_class.MsClass.command_parser"></a>

#### command\_parser

```python
def command_parser(command)
```

Command processor for any cycle command with 'quad' as its target

<a id="ms_hiden_class.MsClass.resetclass"></a>

#### resetclass

```python
def resetclass()
```

Reset class variables to their default

<a id="ms_hiden_class.MsClass.starttimer"></a>

#### starttimer

```python
def starttimer(batchtype, identifier, batchdescription, batchid, batchitemid)
```

Start timer - used as t=0 when calculating best-fits

<a id="ms_hiden_class.MsClass.check_quad_is_online"></a>

#### check\_quad\_is\_online

```python
def check_quad_is_online()
```

Self test to check the quad is online and ready

<a id="ms_hiden_class.MsClass.start_mid"></a>

#### start\_mid

```python
def start_mid()
```

Start a multiple ion detection run on the Hiden Mass Spectrometer

<a id="ms_hiden_class.MsClass.start_profile"></a>

#### start\_profile

```python
def start_profile()
```

Start a 1 to 10 amu scan on the Hiden Mass Spectrometer

<a id="ms_hiden_class.MsClass.getdata"></a>

#### getdata

```python
def getdata()
```

Request mid data from Hiden Mass Spectrometer

<a id="ms_hiden_class.MsClass.getcolumns"></a>

#### getcolumns

```python
def getcolumns()
```

Request columns from Hiden Mass Spectrometer

<a id="ms_hiden_class.MsClass.getcycle"></a>

#### getcycle

```python
def getcycle()
```

Request cycles from Hiden Mass Spectrometer

<a id="ms_hiden_class.MsClass.getenv"></a>

#### getenv

```python
def getenv()
```

Request environment from Hiden Mass Spectrometer

<a id="ms_hiden_class.MsClass.stop_runnning"></a>

#### stop\_runnning

```python
def stop_runnning()
```

Stop the running experiment on the Hiden Mass Spectrometer

<a id="ms_hiden_class.MsClass.next_id"></a>

#### next\_id

```python
def next_id()
```

Generate the next Helium run ID

<a id="ms_hiden_class.MsClass.check_if_stopped"></a>

#### check\_if\_stopped

```python
def check_if_stopped()
```

Check if the run is stopped, if not then raise an alarm

<a id="ms_hiden_class.MsClass.writefile"></a>

#### writefile

```python
def writefile()
```

Write Helium Data file to disk

<a id="ms_hiden_class.MsClass.filedump"></a>

#### filedump

```python
def filedump(data)
```

On error dump the hiden data to a file

<a id="ms_hiden_class.ms"></a>

#### ms

