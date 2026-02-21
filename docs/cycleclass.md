# None

<a id="cycleclass"></a>

# cycleclass

Module for managing and manipulating cycle information in a system.

This module defines the `CycleClass`, which represents a cycle and provides functionality for
retrieving and setting cycle information, as well as managing the steps within a cycle. The cycle
information is loaded from a database, and the class includes methods to query and process cycle data.

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
- read_database(): Get the list of enabled cycles from the database.
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

Reads data from the configured database and updates the instance with retrieved records.

The method performs the following operations:
1. Connects to the database using the specified configuration.
2. Retrieves a list of enabled cycles from the 'cycles' table and updates the internal cycles list.
3. Identifies cycles marked as samples and adds them to the internal samples list.
4. Retrieves all entries from the 'locations' table and updates the internal locations list.
5. Closes the database connection after all operations are complete.

<a id="cycleclass.CycleClass.setcycle"></a>

#### setcycle

```python
def setcycle(name)
```

Sets the current cycle to the specified name if it exists in the list of available cycles.
If the name is not found, logs a warning. Retrieves cycle data from the database and populates
the object's attributes with its details and associated steps. The method skips further
execution if the name is 'End'.

<a id="cycleclass.CycleClass.current"></a>

#### current

```python
def current()
```

Returns information about the current object.

This method compiles selected details of the object, such as its
name and description, into a list. It is useful for obtaining a
quick summary of the primary attributes of the object.

<a id="cycleclass.CycleClass.currenttask"></a>

#### currenttask

```python
def currenttask(time)
```

Determines and returns the current task based on the given time.

The method evaluates whether the provided time matches the scheduled
time of the next step in the process and returns the respective
task details. If no task matches the time, it provides default
values indicating either no task or the end of the tasks.

<a id="cycleclass.CycleClass.currentstep"></a>

#### currentstep

```python
def currentstep()
```

Returns the current step details if available, otherwise returns the default
step representation. The method checks if there are steps recorded and, if so,
returns the first step's information. If no steps are present, it defaults to
returning an end step.

<a id="cycleclass.CycleClass.completecurrent"></a>

#### completecurrent

```python
def completecurrent()
```

Complete the current step in the process.

This method removes the oldest step details from the relevant attributes
to mark the current step as completed. It logs the completion details
including the step time, target, and command of the current step
before removing them from their respective attributes.

<a id="cycleclass.CycleClass.steplist"></a>

#### steplist

```python
def steplist()
```

Generates a list of step details combining step time, target, and command information.

<a id="cycleclass.CycleClass.steplistformatted"></a>

#### steplistformatted

```python
def steplistformatted()
```

Generates a formatted list of steps based on step time, target, and command.

This method combines the attributes `steptime`, `steptarget`, and `stepcommand` into
a formatted list of strings. Each string contains the values from these attributes
at the corresponding index, separated by commas. If no steps exist, a default step
(`1, End, End`) is returned.

<a id="cycleclass.CycleClass.sample"></a>

#### sample

```python
def sample(cycleitem)
```

Checks if a given item exists in the sample list.

This method iterates through the 'samples' attribute and compares each
item with the provided 'cycleitem'. If the 'cycleitem' matches any item
in the list, the method returns True; otherwise, it returns False.

<a id="cycleclass.currentcycle"></a>

#### currentcycle

