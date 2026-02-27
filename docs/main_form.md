# None

<a id="main_form"></a>

# main\_form

Module for the main window interface of the PyMS application.

This module defines the structure and functionality for the main GUI window of
the Python Mass Spectrometry (PyMS) application. It includes event handlers,
UI updates, and interactions with mass spectrometry hardware and associated
software components.

<a id="main_form.webbrowser"></a>

## webbrowser

<a id="main_form.messagebox"></a>

## messagebox

<a id="main_form.QMainWindow"></a>

## QMainWindow

<a id="main_form.QTableWidgetItem"></a>

## QTableWidgetItem

<a id="main_form.QFont"></a>

## QFont

<a id="main_form.Qt"></a>

## Qt

<a id="main_form.QTimer"></a>

## QTimer

<a id="main_form.QThreadPool"></a>

## QThreadPool

<a id="main_form.settings"></a>

## settings

<a id="main_form.writesettings"></a>

## writesettings

<a id="main_form.setrunning"></a>

## setrunning

<a id="main_form.alarms"></a>

## alarms

<a id="main_form.VERSION"></a>

## VERSION

<a id="main_form.valvegetstatus"></a>

## valvegetstatus

<a id="main_form.lasergetstatus"></a>

## lasergetstatus

<a id="main_form.lasergetalarm"></a>

## lasergetalarm

<a id="main_form.pressuresread"></a>

## pressuresread

<a id="main_form.xyread"></a>

## xyread

<a id="main_form.lasercommand"></a>

## lasercommand

<a id="main_form.lasersetpower"></a>

## lasersetpower

<a id="main_form.valvechange"></a>

## valvechange

<a id="main_form.xymoveto"></a>

## xymoveto

<a id="main_form.xymove"></a>

## xymove

<a id="main_form.batch"></a>

## batch

<a id="main_form.currentcycle"></a>

## currentcycle

<a id="main_form.ms"></a>

## ms

<a id="main_form.alert"></a>

## alert

<a id="main_form.logger"></a>

## logger

<a id="main_form.download_file_raw_via_api"></a>

## download\_file\_raw\_via\_api

<a id="main_form.Ui_MainWindow"></a>

## Ui\_MainWindow

<a id="main_form.UiBatch"></a>

## UiBatch

<a id="main_form.UiAbout"></a>

## UiAbout

<a id="main_form.UiLogViewer"></a>

## UiLogViewer

<a id="main_form.UiSettingsViewer"></a>

## UiSettingsViewer

<a id="main_form.ManualXyForm"></a>

## ManualXyForm

<a id="main_form.LaserFormUI"></a>

## LaserFormUI

<a id="main_form.NccCalcUI"></a>

## NccCalcUI

<a id="main_form.GAUGE_GOOD"></a>

#### GAUGE\_GOOD

<a id="main_form.GAUGE_BAD"></a>

#### GAUGE\_BAD

<a id="main_form.UiMain"></a>

## UiMain Objects

```python
class UiMain(QMainWindow, Ui_MainWindow)
```

UiMain class provides the main interface and control logic for the PyMS application.

This class is responsible for handling UI interactions, connection to various hardware
components, and updating the system status. It acts as a centralised hub for managing
batch processes, valves, and real-time data updates from components such as the vacuum
gauges and mass spectrometer.

<a id="main_form.UiMain.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="main_form.UiMain.global_timer"></a>

#### global\_timer

```python
def global_timer()
```

Updates the global timer and manages periodic tasks and UI updates.

This function increments the timer by a predefined step, updates the displayed
elapsed time, and triggers several background threads to perform periodic
updates and checks. Depending on the current timer state, it schedules
specific tasks such as updating UI components or repainting the interface.

<a id="main_form.UiMain.read_ms"></a>

#### read\_ms

```python
def read_ms()
```

Reads the status of the Hiden Quadrupole Mass Spectrometer and updates the UI elements
accordingly based on its online or offline status.

<a id="main_form.UiMain.check_alarms"></a>

#### check\_alarms

```python
def check_alarms()
```

Checks various alarm conditions and updates system status accordingly.

This method evaluates multiple alarm indicators to ensure the proper operation
of the system. If any issues are detected, it updates the system's status, resets
relevant operational counters, pauses the system, and generates appropriate alerts.
The method interacts with a variety of subsystems, including laser controllers, vacuum
pumps, Hiden instruments, and other hardware components. Alerts and logging are
generated for detected failures or deviations from normal operating conditions.

<a id="main_form.UiMain.update_ui_display_items"></a>

#### update\_ui\_display\_items

```python
def update_ui_display_items()
```

Updates the UI display elements based on the current status of various system components.

This method dynamically adjusts the visibility of UI elements representing valves and the laser
based on their statuses retrieved from external status functions. It ensures the UI remains
synchronised with the underlying system status by logging changes and updating the visibility
of corresponding UI components.

<a id="main_form.UiMain.emergency_stop"></a>

#### emergency\_stop

```python
def emergency_stop()
```

Triggers an emergency stop for the system, halting all ongoing operations, resetting
counters, and ensuring that safety protocols are followed. This method is designed to
handle critical situations requiring immediate intervention.

<a id="main_form.UiMain.run_click"></a>

#### run\_click

```python
def run_click()
```

Handles the click event for the run button in the user interface.

This method checks the state of the 'Run' toggle button and updates various
instance attributes accordingly. If the button is pressed, it triggers a 'Run'
operation, logging the event and initialising associated variables. If the
button is not pressed, it triggers a 'Pause' operation, logging the event and
adjusting attributes to reflect the paused state. The method also updates the
finish time label in the user interface based on the operation mode.

<a id="main_form.UiMain.runstate"></a>

#### runstate

```python
def runstate()
```

Handles toggling between automated and manual control modes.

This method adjusts the state of the control panel based on the current
run mode. It disables or enables certain UI components, updates the status
label, and controls the laser state accordingly. In case of any errors
during execution, it logs the error event.

<a id="main_form.UiMain.closeEvent"></a>

#### closeEvent

```python
def closeEvent(event)
```

Handles the close event of the main UI form.

This method is triggered when the main form receives a close event.
It logs the event, saves the current position of the form to the settings,
writes the updated settings to persistent storage, flags the application state
as no longer running, and cleans up the form instance.

<a id="main_form.UiMain.event_timer"></a>

#### event\_timer

```python
def event_timer()
```

Handles timed events and updates the user interface based on the current batch's state.

This method is called periodically to check for updates and handle events such as changes
to the current batch or executing event parsing logic. It performs the necessary updates to
reload interface components when the current batch has changed and logs errors in case of
unexpected issues.

<a id="main_form.UiMain.event_parser"></a>

#### event\_parser

```python
def event_parser()
```

Handles the parsing and execution of events in a predefined sequence.

This method is responsible for managing the execution of commands in the current cycle
based on specific timing and conditions. It performs various tasks depending on the type
of command, such as controlling valves, lasers, an XY table, taking images, sending manual
messages, or handling the end of a cycle. It ensures synchronisation of the sequence,
monitors laser alarms, and updates the list and state of the program accordingly.

<a id="main_form.UiMain.menu_show_new_batch"></a>

#### menu\_show\_new\_batch

```python
def menu_show_new_batch()
```

Displays a new batch dialog.

This method initialises and shows a modal dialogue for creating or working
with a new batch. It ensures the dialogue is set up properly and executes
necessary checks before display.

<a id="main_form.UiMain.menu_show_about"></a>

#### menu\_show\_about

```python
def menu_show_about()
```

Displays the "About" dialogue for the application.

This method is responsible for initialising and displaying the "About"
dialog when triggered. It creates an instance of the UiAbout class
and uses it to show the dialogue to the user.

<a id="main_form.UiMain.menu_show_log_viewer"></a>

#### menu\_show\_log\_viewer

```python
def menu_show_log_viewer()
```

Displays and initialises the log viewer dialogue.

This method creates an instance of the log viewer dialogue, loads the log
data, and makes the dialogue visible to the user.

<a id="main_form.UiMain.menu_show_settings_viewer"></a>

#### menu\_show\_settings\_viewer

```python
def menu_show_settings_viewer()
```

Displays the settings viewer dialogue.

This method initialises and displays the settings viewer dialogue to allow
users to view and manage application settings and secrets.

<a id="main_form.UiMain.menu_show_xymanual"></a>

#### menu\_show\_xymanual

```python
def menu_show_xymanual()
```

Displays the XY Manual dialogue to the user.

This method initialises and displays a modal dialogue, allowing the
user to interact with the XY Manual form.

<a id="main_form.UiMain.menu_show_lasermanual"></a>

#### menu\_show\_lasermanual

```python
def menu_show_lasermanual()
```

Displays the laser manual interface by opening a new modal dialogue.

This method is responsible for initialising and displaying a modal dialogue
for the laser manual interface. It ensures the dialogue is modal to prevent
interaction with the main interface while the dialogue is open.

<a id="main_form.UiMain.menu_show_ncc"></a>

#### menu\_show\_ncc

```python
def menu_show_ncc()
```

Displays the NCC Calculation Menu.

This method initialises an instance of the NccCalcUI class, sets it as a modal dialogue,
refreshes its content, and displays the dialogue.

<a id="main_form.UiMain.update_ui_batch_list"></a>

#### update\_ui\_batch\_list

```python
def update_ui_batch_list()
```

Updates the batch list in the user interface by clearing and repopulating the list,
and also updates other related UI elements with formatted information from the
batch and cycle data. Any errors during this process are logged.

<a id="main_form.UiMain.update_ui_commandlist"></a>

#### update\_ui\_commandlist

```python
def update_ui_commandlist()
```

Updates the UI command list with the current cycle's formatted steps.

This method clears the existing commands from the UI list and populates it with
the formatted steps of the current cycle. Logs debug messages during the process
and logs errors if an exception occurs.

<a id="main_form.UiMain.update_ui_pressures"></a>

#### update\_ui\_pressures

```python
def update_ui_pressures()
```

Updates the user interface with the latest vacuum pressures.

This method retrieves current pressure readings for various vacuum components
and updates the corresponding UI text fields. The values are formatted
appropriately for display. If the nitrogen (N2) pressure exceeds a specific
threshold, its display value is shown as "N/A".

<a id="main_form.UiMain.update_ui_xy_positions"></a>

#### update\_ui\_xy\_positions

```python
def update_ui_xy_positions()
```

Updates the UI with the current X and Y positions.

This method fetches the current X and Y positions by reading the status
using the `xyread` function. If the status of the X movement is not
'timeout', the method updates the X and Y position attributes and
reflects these values in the respective UI elements for display.

<a id="main_form.UiMain.update_ui_results_table"></a>

#### update\_ui\_results\_table

```python
def update_ui_results_table()
```

Updates the user interface results table with the latest data.

This method retrieves the batch results and updates the table displayed
in the user interface by clearing old entries and repopulating the table with
new information. Each row of the table represents a result with the
corresponding timestamp, file name, description, and result value.

<a id="main_form.UiMain.move_next"></a>

#### move\_next

```python
def move_next()
```

Moves to the next specified location by initiating motion threads.

This method is responsible for transitioning to the next location provided
by the batch system. It uses threads managed by `thread_manager` to
initiate movement along the x and y axes. Debug logs are generated for
tracking the operation status.

<a id="main_form.UiMain.manual_message"></a>

#### manual\_message

```python
def manual_message(message)
```

Provides a method to display a manual step message to the user through a popup.

    Displays a popup message to inform the user about a necessary manual step in
    the application. The main form's state is temporarily updated to handle this
    manual step, and once the user acknowledges the popup, the state is restored.

<a id="main_form.move_x"></a>

#### move\_x

```python
def move_x()
```

Moves the object to a new x-coordinate based on the next location from the batch.

This function retrieves the next location coordinates from the batch and moves

<a id="main_form.move_y"></a>

#### move\_y

```python
def move_y()
```

Moves an object along the Y-axis to a specified location.

The function determines the next location of the object and moves it
to the corresponding Y-coordinate. It utilizes data from the `batch`
object to calculate the target position.

<a id="main_form.check_for_updates"></a>

#### check\_for\_updates

```python
def check_for_updates()
```

Checks for updates to the application and provides appropriate messages.

This function checks if a new version of the application is available by
downloading update information via an API. If an update is detected, it
notifies the user to close the application and run the installer. Otherwise,
it informs the user that they are using the latest version.

<a id="main_form.menu_open_web_page"></a>

#### menu\_open\_web\_page

```python
def menu_open_web_page(page)
```

Opens a specific web page or file based on the provided page identifier.

This function dynamically generates URLs based on the given page identifier
and the host configuration stored within the `settings` dictionary. It supports
various categories such as status pages, log pages, and static files. Corresponding
URLs are opened using the default web browser.

