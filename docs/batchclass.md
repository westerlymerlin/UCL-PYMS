# None

<a id="batchclass"></a>

# batchclass

Batch management for PyMS.

This module provides a lightweight persistence layer and in-memory model for
building and executing a queue of measurement steps (a “batch”). A batch may be
a simple list of sample runs or a planchet layout; steps are stored in / loaded
from the project’s SQLite database and processed in order.

Key features:
- Create a new batch and append steps (cycle, location, identifier)
- Load any unfinished steps from the database on startup
- Persist batch metadata and steps (insert/update)
- Mark the current step complete, cancel remaining steps, and advance the queue
- Generate per-batch results output (CSV + NCC file generation)

Notes:
- Database paths and runtime settings are taken from the shared application
  settings.
- The module exposes a singleton-like `batch` instance for use by the UI and
  control code.

<a id="batchclass.sqlite3"></a>

## sqlite3

<a id="batchclass.datetime"></a>

## datetime

<a id="batchclass.timedelta"></a>

## timedelta

<a id="batchclass.os"></a>

## os

<a id="batchclass.settings"></a>

## settings

<a id="batchclass.friendlydirname"></a>

## friendlydirname

<a id="batchclass.writesettings"></a>

## writesettings

<a id="batchclass.logger"></a>

## logger

<a id="batchclass.imager"></a>

## imager

<a id="batchclass.ncc"></a>

## ncc

<a id="batchclass.currentcycle"></a>

## currentcycle

<a id="batchclass.BatchClass"></a>

## BatchClass Objects

```python
class BatchClass()
```

The `BatchClass` represents a batch of samples or planchets. It allows for the creation, modification, and
completion of batch steps. The class interacts with a SQLite database to store
and retrieve batch information.

Attributes:
    id (int): ID number of the batch. -1 indicates that the batch has not been saved yet, otherwise it is taken from
    the database.
    date (datetime): The date and time when the batch was created.
    description (str): The description or name of the batch.
    type (str): The type of batch. Can be either 'Simple Batch' or 'Planchet'.
    runnumber (list[int]): A list of ID numbers of each item in the batch, including the samples.
    cycle (list[str]): A list of the type of cycle required for each item.
    location (list[str]): A list of the hole location if needed for each item.
    identifier (list[str]): A list of the description of the sample or qnumber for each item.
    status (list[int]): A list of the status of each item. 0 indicates 'to do', 1 indicates 'complete', and 2
    indicates 'cancelled'.
    changed (int): A flag indicating whether the batch has been modified since the last save.

Methods:
    read_database()
        Reads the PyMS database for any open batches.

    cancel_batch()
        Used to cancel_batch a batch. Marks all samples as cancelled and closes the batch.

    new(batchtype: str, description: str)
        Creates a new batch with the specified batch type and description.

    addstep(cycle: str, location: str, identifier: str)
        Adds a sample to the batch.

    save()
        Saves the batch details to the database.

    current()
        Returns the details of the current batch step or 'End' if there are no more steps.

    completecurrent()
        Marks the current batch step as complete.

    writebatchlog()
        Generates the batchlog.csv file for the batch.

<a id="batchclass.BatchClass.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="batchclass.BatchClass.read_database"></a>

#### read\_database

```python
def read_database()
```

Reads the database to fetch batch step and batch details with specific status and updates
relevant attributes accordingly. The method retrieves information on batch steps with a
status of 0 and their corresponding batch details. Additionally, it updates internal
statuses, identifiers, and other related attributes based on the retrieved data.

<a id="batchclass.BatchClass.cancel_batch"></a>

#### cancel\_batch

```python
def cancel_batch()
```

Cancels all batch steps with a status of 0 (unprocessed) and updates their status to 2 (cancelled).

This method connects to the database, retrieves all batch steps with a status
of 0, and updates their status to 2. It resets several internal attributes of
the object to default values after successfully processing the batch steps.

<a id="batchclass.BatchClass.new"></a>

#### new

```python
def new(batch_type, description)
```

Creates a new batch with the specified type and description.

This method initializes a new batch process by setting its type and description
attributes, and assigns the current date and time to the batch. If the batch
has already been created (identified by an id greater than 0), it cancels the
current batch before proceeding.

Parameters:
    batch_type: The type of the batch to be created.
    description: A description for the batch.

<a id="batchclass.BatchClass.addstep"></a>

#### addstep

```python
def addstep(cycle, location, identifier)
```

Adds a new step to track in the process by appending details to respective attributes.

<a id="batchclass.BatchClass.save"></a>

#### save

```python
def save()
```

Saves the current state of the batch object and its associated steps to the database. If the batch is new, it inserts
a new batch record; otherwise, it updates the existing batch record. It also ensures that related batch steps are
inserted or updated appropriately. If the batch type is 'planchet', additional recalculations are performed.

<a id="batchclass.BatchClass.current"></a>

#### current

```python
def current()
```

Returns the details of the current batch being processed or a message indicating no batches remain.

Summary:
This method checks whether any batches are available for processing. If batches exist,
it returns a list containing the current cycle, location, and identifier of the batch.
If no batches are left, it returns a list with a message signaling the end of processing
along with default placeholder values.

<a id="batchclass.BatchClass.completecurrent"></a>

#### completecurrent

```python
def completecurrent()
```

Updates the current batch step status to 1 (completed) in the database and moves on to the next task if
any remaining task exists. If all tasks are completed, it resets the relevant attributes
to their default values.

<a id="batchclass.BatchClass.writebatchlog"></a>

#### writebatchlog

```python
def writebatchlog()
```

Writes a detailed log for the batch process, including batch metadata and results. The method handles directory
creation, data retrieval from the database, CSV file generation, and integrates results into the specified
output directory.

<a id="batchclass.BatchClass.list"></a>

#### list

```python
def list()
```

Produces a consolidated list of details from multiple attributes.

This method iterates through the values of `runnumber`, combining corresponding
values from `cycle`, `location`, and `identifier` attributes to create a list of
lists. Each inner list contains the following elements in order: `runnumber`,
`cycle`, `location`, and `identifier`.

<a id="batchclass.BatchClass.listformatted"></a>

#### listformatted

```python
def listformatted()
```

Generates a formatted list of data points based on run numbers, cycles, and other attributes.

Summary:
The method iterates over the 'runnumber' list of the class, creating a formatted string for each
data point. It combines the run number, cycle, and other attributes conditionally based on specific
criteria. If no data points are processed, a default value is returned.

<a id="batchclass.BatchClass.formatsample"></a>

#### formatsample

```python
def formatsample()
```

Formatsample processes and formats a sample identifier based on its attributes and status.

This method determines the appropriate formatting for a sample by checking its cycle
status and related identifiers. Various conditions, such as whether the identifier is empty,
or specific cycle values match preset categories (e.g., 'Q-Standard', 'Index'), are used
to construct the formatted string.

<a id="batchclass.BatchClass.currentdescription"></a>

#### currentdescription

```python
def currentdescription()
```

Returns the description of the current batch or a default message if no batch
is loaded.

This method checks the value of the 'id' attribute to determine whether a
batch is loaded. If no batch is loaded (indicated by an 'id' value of -1),
it returns a default message stating that no batch is loaded. Otherwise,
it returns the description of the current batch.

<a id="batchclass.BatchClass.currentcycle"></a>

#### currentcycle

```python
def currentcycle()
```

Returns the current cycle of the loaded batch.

This method retrieves the current cycle from the loaded batch. If no batch
is loaded (indicated by `id` being -1), it returns a default message
stating that no batch is loaded.

<a id="batchclass.BatchClass.formatdescription"></a>

#### formatdescription

```python
def formatdescription()
```

Formats and returns a batch description string based on the batch ID and description.

This method attempts to construct a string representation of the batch information.
If the batch ID is set to -1, indicating no batch is loaded, a default message is returned.
In case of exceptions during formatting, an error message is provided.

<a id="batchclass.BatchClass.getlocationsample"></a>

#### getlocationsample

```python
def getlocationsample(location)
```

Retrieves a sample identifier based on the provided location.

This method attempts to fetch a corresponding identifier for
the given location from the stored location list.

<a id="batchclass.BatchClass.insertcycle"></a>

#### insertcycle

```python
def insertcycle(index, cycle)
```

Inserts a new cycle and its associated default values at the specified index.

This method modifies several attributes of the class by inserting a new entry at
the given index. The inserted entry includes a cycle value and default values for
other corresponding attributes.

<a id="batchclass.BatchClass.recalulateplanchet"></a>

#### recalulateplanchet

```python
def recalulateplanchet()
```

Recalculates the planchet for the current run.

This method modifies the current run by inserting specific cycles at different
positions in the run. If the run number length exceeds 36, additional cycles
are inserted at the middle of the run. This is done to ensure standardization
across the run phases.

<a id="batchclass.BatchClass.nextlocation"></a>

#### nextlocation

```python
def nextlocation()
```

Returns the next non-empty location from the list of locations or a fallback value.

This method iterates through the `location` list, starting from the second
element, to look for the first non-empty string. If all subsequent elements
are empty, it returns a default value of 'UL'.

<a id="batchclass.BatchClass.locxy"></a>

#### locxy

```python
def locxy(loc)
```

Retrieves the x and y coordinates of a specific location from the database.

Fetches information from the locations table in the connected SQLite database
to obtain the x and y positional values associated with the specified location name.

<a id="batchclass.BatchClass.isitthereyet"></a>

#### isitthereyet

```python
def isitthereyet(current_x_pos, current_y_pos)
```

Determines whether the current position is near the target location.

The method checks if the given x and y coordinates are within a threshold
distance from a specific target location. If the target location is not
specified or only the initial location is available, it considers the position
to have been reached by default. The method logs information when the x and y
coordinates are verified as close to the target location.

<a id="batchclass.BatchClass.results"></a>

#### results

```python
def results()
```

Fetches the results of the most recent or specified batch run from a SQLite database.

This method retrieves records associated with a batch run from the database. If a specific batch
ID (`self.id`) is greater than zero, it is used directly. Otherwise, the method identifies the
most recent batch run using the `HeliumRuns` table. The results include details such as
record ID, identifier, date of the run, and best fit for each entry within the specified or
latest batch.

<a id="batchclass.BatchClass.image"></a>

#### image

```python
def image(application)
```

Formats a sample ID and initiates the imaging process for the application.

This method creates a sample ID by combining a prefix with a unique run
number and formatted sample data, then calls the `imager` function to
carry out the imaging process. The generated `sample_id` is passed along
with the application name, unique identifier, and description of the
sample to the imaging function.

<a id="batchclass.BatchClass.finishtime"></a>

#### finishtime

```python
def finishtime()
```

Calculates the estimated finish time for a batch process.

Connects to the database and calculates the total time of unfinished batch steps
where their corresponding cycle steps have a target set to "end". Uses the current
time and the total time retrieved from the database to compute the estimated end
time.

<a id="batchclass.next_q"></a>

#### next\_q

```python
def next_q()
```

Generates the next unique identifier for a MassSpec operation.

The function retrieves the current value of the "nextQ" setting from the
"MassSpec" configuration, increments it, updates the setting, and then
returns the original value as a string.

<a id="batchclass.reset_q"></a>

#### reset\_q

```python
def reset_q()
```

Resets the 'Q' number to the next available identifier.

This method connects to the database, retrieves the last used identifier
from the 'QNumbers' view, and updates the application settings with the
next sequential number. If an error occurs during the process, it is logged.

<a id="batchclass.batch"></a>

#### batch

