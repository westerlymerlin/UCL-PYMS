# Contents for: batchclass

* [batchclass](#batchclass)
  * [sqlite3](#batchclass.sqlite3)
  * [datetime](#batchclass.datetime)
  * [timedelta](#batchclass.timedelta)
  * [os](#batchclass.os)
  * [settings](#batchclass.settings)
  * [friendlydirname](#batchclass.friendlydirname)
  * [writesettings](#batchclass.writesettings)
  * [logger](#batchclass.logger)
  * [imager](#batchclass.imager)
  * [ncc](#batchclass.ncc)
  * [currentcycle](#batchclass.currentcycle)
  * [BatchClass](#batchclass.BatchClass)
    * [\_\_init\_\_](#batchclass.BatchClass.__init__)
    * [readdatabase](#batchclass.BatchClass.readdatabase)
    * [cancel](#batchclass.BatchClass.cancel)
    * [new](#batchclass.BatchClass.new)
    * [addstep](#batchclass.BatchClass.addstep)
    * [save](#batchclass.BatchClass.save)
    * [current](#batchclass.BatchClass.current)
    * [completecurrent](#batchclass.BatchClass.completecurrent)
    * [writebatchlog](#batchclass.BatchClass.writebatchlog)
    * [list](#batchclass.BatchClass.list)
    * [listformatted](#batchclass.BatchClass.listformatted)
    * [formatsample](#batchclass.BatchClass.formatsample)
    * [currentdescription](#batchclass.BatchClass.currentdescription)
    * [currentcycle](#batchclass.BatchClass.currentcycle)
    * [formatdescription](#batchclass.BatchClass.formatdescription)
    * [getlocationsample](#batchclass.BatchClass.getlocationsample)
    * [insertcycle](#batchclass.BatchClass.insertcycle)
    * [recalulateplanchet](#batchclass.BatchClass.recalulateplanchet)
    * [newq](#batchclass.BatchClass.newq)
    * [nextlocation](#batchclass.BatchClass.nextlocation)
    * [locxy](#batchclass.BatchClass.locxy)
    * [isitthereyet](#batchclass.BatchClass.isitthereyet)
    * [results](#batchclass.BatchClass.results)
    * [image](#batchclass.BatchClass.image)
    * [finishtime](#batchclass.BatchClass.finishtime)
  * [batch](#batchclass.batch)

<a id="batchclass"></a>

# batchclass

BatchClass - used to manage a batch of cycles (samples, blanks, qshots or other tasks)

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
    readdatabase()
        Reads the PyMS database for any open batches.

    cancel()
        Used to cancel a batch. Marks all samples as cancelled and closes the batch.

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

<a id="batchclass.BatchClass.readdatabase"></a>

#### readdatabase

```python
def readdatabase()
```

Reads the PyMS database for any open batches

<a id="batchclass.BatchClass.cancel"></a>

#### cancel

```python
def cancel()
```

Used to cancel a batch - marks all samples and cancelled and closes the batch

<a id="batchclass.BatchClass.new"></a>

#### new

```python
def new(batchtype, description)
```

Creates a new batch ***batchtype*** is 'simple' or 'planchet'

<a id="batchclass.BatchClass.addstep"></a>

#### addstep

```python
def addstep(cycle, location, identifier)
```

Adds a sample to a batch

<a id="batchclass.BatchClass.save"></a>

#### save

```python
def save()
```

Save to database

<a id="batchclass.BatchClass.current"></a>

#### current

```python
def current()
```

Returns current step or 'End' if there are no more steps

<a id="batchclass.BatchClass.completecurrent"></a>

#### completecurrent

```python
def completecurrent()
```

Mark the current task in the bach complete

<a id="batchclass.BatchClass.writebatchlog"></a>

#### writebatchlog

```python
def writebatchlog()
```

Generate the batchlog.csv file

<a id="batchclass.BatchClass.list"></a>

#### list

```python
def list()
```

Return a list of all of the outstancing tasks

<a id="batchclass.BatchClass.listformatted"></a>

#### listformatted

```python
def listformatted()
```

return a formatted list of all the outstanding tasks

<a id="batchclass.BatchClass.formatsample"></a>

#### formatsample

```python
def formatsample()
```

Generate a meaningful sample name based on the pit in the planchet and samplid, Qshot or line blank

<a id="batchclass.BatchClass.currentdescription"></a>

#### currentdescription

```python
def currentdescription()
```

Return the description attribute for the current batch

<a id="batchclass.BatchClass.currentcycle"></a>

#### currentcycle

```python
def currentcycle()
```

Return the sysle type for the current task in the batch

<a id="batchclass.BatchClass.formatdescription"></a>

#### formatdescription

```python
def formatdescription()
```

Format the description based on the batch identifier and the descri[ption field

<a id="batchclass.BatchClass.getlocationsample"></a>

#### getlocationsample

```python
def getlocationsample(location)
```

Return the location on the planchet of the current sample

<a id="batchclass.BatchClass.insertcycle"></a>

#### insertcycle

```python
def insertcycle(index, cycle)
```

Insert a new task into the batch - used when a planchet is created to add in Q-shots and line blanks at
the start, mid point and end

<a id="batchclass.BatchClass.recalulateplanchet"></a>

#### recalulateplanchet

```python
def recalulateplanchet()
```

Calculate the positions of Q-shots, line blanks and unload tasks. Used when editing a planchet

<a id="batchclass.BatchClass.newq"></a>

#### newq

```python
def newq()
```

Genrate the newxt Q-Shot number

<a id="batchclass.BatchClass.nextlocation"></a>

#### nextlocation

```python
def nextlocation()
```

Find the next location - used when moving laser to next spot.

if there is no next location then the unload 'UL' location is given

<a id="batchclass.BatchClass.locxy"></a>

#### locxy

```python
def locxy(loc)
```

for a location **loc** find the x and y values from the database

<a id="batchclass.BatchClass.isitthereyet"></a>

#### isitthereyet

```python
def isitthereyet(current_x_pos, current_y_pos)
```

Check if the laser has reached the desired location

<a id="batchclass.BatchClass.results"></a>

#### results

```python
def results()
```

return the best-fit values for all processed tasks in the batch

<a id="batchclass.BatchClass.image"></a>

#### image

```python
def image(application)
```

Calls the **imager** task from the imagefiler module to crab a screen shot of that window

<a id="batchclass.BatchClass.finishtime"></a>

#### finishtime

```python
def finishtime()
```

Calculate the theorectical finish time of the current batch

<a id="batchclass.batch"></a>

#### batch

