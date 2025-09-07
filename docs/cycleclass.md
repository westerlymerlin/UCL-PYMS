# None

<a id="cycleclass"></a>

# cycleclass

Cycle Class
Author: Gary Twinn

<a id="cycleclass.sqlite3"></a>

## sqlite3

<a id="cycleclass.settings"></a>

## settings

<a id="cycleclass.logger"></a>

## logger

<a id="cycleclass.CycleClass"></a>

## CycleClass Objects

```python
class CycleClass()
```

:class: CycleClass

The CycleClass represents a cycle in a system. It stores information such as the current cycle name, description,
 status, laser power, available cycle names, samples, locations, step times, targets, and commands.
 It also provides methods to manipulate and retrieve information about the cycle.

Attributes:
- id (int): The ID of the current cycle.
- name (str): The name of the current cycle.
- description (str): The description of the current cycle.
- enabled (bool): The status of the current cycle.
- laserpower (float): The laser power of the current cycle.
- cycles (list): The list of available cycle names.
- samples (list): The available cycle names that process samples and use the laser.
- locations (list): The list of all locations on the planchet.
- steptime (list): The list of step times for the current cycle.
- steptarget (list): The list of targets for each step in the current cycle.
- stepcommand (list): The list of commands for each step in the current cycle.

Methods:
- readdatabase(): Get the list of enabled cycles from the database.
- setcycle(name: str): Set the current cycle to the given name and retrieve all the steps.
- current(): Return the current cycle name and description.
- currenttask(time: float): Return the current task at the given time.
- currentstep(): Return the current step.
- completecurrent(): Delete the current step as it has been completed.
- steplist(): Return the list of steps to be completed.
- steplistformatted(): Generate a formatted list of steps as a list of strings.
- sample(cycleitem: str): Check if an item is in the list of samples.

<a id="cycleclass.CycleClass.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="cycleclass.CycleClass.readdatabase"></a>

#### readdatabase

```python
def readdatabase()
```

Get the list of enabled cycles from the database

<a id="cycleclass.CycleClass.setcycle"></a>

#### setcycle

```python
def setcycle(name)
```

Set the current cycle to the given name and retrieve all the steps (used when the cycle starts)

<a id="cycleclass.CycleClass.current"></a>

#### current

```python
def current()
```

Return the current Cycle name and description

<a id="cycleclass.CycleClass.currenttask"></a>

#### currenttask

```python
def currenttask(time)
```

Return the current task

<a id="cycleclass.CycleClass.currentstep"></a>

#### currentstep

```python
def currentstep()
```

Return the current step

<a id="cycleclass.CycleClass.completecurrent"></a>

#### completecurrent

```python
def completecurrent()
```

Delete the current step as it has been completed

<a id="cycleclass.CycleClass.steplist"></a>

#### steplist

```python
def steplist()
```

return the list of steps to be completed

<a id="cycleclass.CycleClass.steplistformatted"></a>

#### steplistformatted

```python
def steplistformatted()
```

Generate a formatted list of steps as a list of strings

<a id="cycleclass.CycleClass.sample"></a>

#### sample

```python
def sample(cycleitem)
```

Check is an item is in the list of samples

<a id="cycleclass.currentcycle"></a>

#### currentcycle

