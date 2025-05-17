# Contents for: main_form

* [main\_form](#main_form)
  * [webbrowser](#main_form.webbrowser)
  * [messagebox](#main_form.messagebox)
  * [QMainWindow](#main_form.QMainWindow)
  * [QTableWidgetItem](#main_form.QTableWidgetItem)
  * [QFont](#main_form.QFont)
  * [Qt](#main_form.Qt)
  * [QTimer](#main_form.QTimer)
  * [QThreadPool](#main_form.QThreadPool)
  * [settings](#main_form.settings)
  * [writesettings](#main_form.writesettings)
  * [setrunning](#main_form.setrunning)
  * [alarms](#main_form.alarms)
  * [VERSION](#main_form.VERSION)
  * [valvegetstatus](#main_form.valvegetstatus)
  * [lasergetstatus](#main_form.lasergetstatus)
  * [lasergetalarm](#main_form.lasergetalarm)
  * [pressuresread](#main_form.pressuresread)
  * [xyread](#main_form.xyread)
  * [lasercommand](#main_form.lasercommand)
  * [lasersetpower](#main_form.lasersetpower)
  * [valvechange](#main_form.valvechange)
  * [xymoveto](#main_form.xymoveto)
  * [xymove](#main_form.xymove)
  * [rpi\_reboot](#main_form.rpi_reboot)
  * [batch](#main_form.batch)
  * [currentcycle](#main_form.currentcycle)
  * [ms](#main_form.ms)
  * [alert](#main_form.alert)
  * [logger](#main_form.logger)
  * [Ui\_MainWindow](#main_form.Ui_MainWindow)
  * [UiBatch](#main_form.UiBatch)
  * [UiAbout](#main_form.UiAbout)
  * [UiLogViewer](#main_form.UiLogViewer)
  * [UiSettingsViewer](#main_form.UiSettingsViewer)
  * [ManualXyForm](#main_form.ManualXyForm)
  * [LaserFormUI](#main_form.LaserFormUI)
  * [NccCalcUI](#main_form.NccCalcUI)
  * [GUAGE\_GOOD](#main_form.GUAGE_GOOD)
  * [GUAGE\_BAD](#main_form.GUAGE_BAD)
  * [UiMain](#main_form.UiMain)
    * [\_\_init\_\_](#main_form.UiMain.__init__)
    * [global\_timer](#main_form.UiMain.global_timer)
    * [read\_ms](#main_form.UiMain.read_ms)
    * [check\_alarms](#main_form.UiMain.check_alarms)
    * [update\_ui\_display\_items](#main_form.UiMain.update_ui_display_items)
    * [emergency\_stop](#main_form.UiMain.emergency_stop)
    * [run\_click](#main_form.UiMain.run_click)
    * [runstate](#main_form.UiMain.runstate)
    * [closeEvent](#main_form.UiMain.closeEvent)
    * [event\_timer](#main_form.UiMain.event_timer)
    * [event\_parser](#main_form.UiMain.event_parser)
    * [menu\_show\_new\_batch](#main_form.UiMain.menu_show_new_batch)
    * [menu\_show\_about](#main_form.UiMain.menu_show_about)
    * [menu\_show\_log\_viewer](#main_form.UiMain.menu_show_log_viewer)
    * [menu\_show\_settings\_viewer](#main_form.UiMain.menu_show_settings_viewer)
    * [menu\_show\_xymanual](#main_form.UiMain.menu_show_xymanual)
    * [menu\_show\_lasermanual](#main_form.UiMain.menu_show_lasermanual)
    * [menu\_show\_ncc](#main_form.UiMain.menu_show_ncc)
    * [update\_ui\_batch\_list](#main_form.UiMain.update_ui_batch_list)
    * [update\_ui\_commandlist](#main_form.UiMain.update_ui_commandlist)
    * [update\_ui\_pressures](#main_form.UiMain.update_ui_pressures)
    * [update\_ui\_xy\_positions](#main_form.UiMain.update_ui_xy_positions)
    * [update\_ui\_results\_table](#main_form.UiMain.update_ui_results_table)
    * [move\_next](#main_form.UiMain.move_next)
    * [manual\_message](#main_form.UiMain.manual_message)
  * [move\_x](#main_form.move_x)
  * [move\_y](#main_form.move_y)
  * [restart\_pi](#main_form.restart_pi)
  * [menu\_open\_web\_page](#main_form.menu_open_web_page)

<a id="main_form"></a>

# main\_form

Main Helium line form - graphical outut of the Heliumline state and timers for running samples
Author: Gary Twinn

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

<a id="main_form.rpi_reboot"></a>

## rpi\_reboot

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

<a id="main_form.GUAGE_GOOD"></a>

#### GUAGE\_GOOD

<a id="main_form.GUAGE_BAD"></a>

#### GUAGE\_BAD

<a id="main_form.UiMain"></a>

## UiMain Objects

```python
class UiMain(QMainWindow, Ui_MainWindow)
```

Qt Class for main window

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

Timer routine for updating displays, runs every second

<a id="main_form.UiMain.read_ms"></a>

#### read\_ms

```python
def read_ms()
```

Update the Hiden Mass Spectrometer widget with its status

<a id="main_form.UiMain.check_alarms"></a>

#### check\_alarms

```python
def check_alarms()
```

Test for alarms

<a id="main_form.UiMain.update_ui_display_items"></a>

#### update\_ui\_display\_items

```python
def update_ui_display_items()
```

Update the valve and laser widgets on the display

<a id="main_form.UiMain.emergency_stop"></a>

#### emergency\_stop

```python
def emergency_stop()
```

Emergency stop event triggered

<a id="main_form.UiMain.run_click"></a>

#### run\_click

```python
def run_click()
```

Run button event handler

<a id="main_form.UiMain.runstate"></a>

#### runstate

```python
def runstate()
```

Events dependent on run state

<a id="main_form.UiMain.closeEvent"></a>

#### closeEvent

```python
def closeEvent(event)
```

Application close handler

<a id="main_form.UiMain.event_timer"></a>

#### event\_timer

```python
def event_timer()
```

Event timer used when a batch is running

<a id="main_form.UiMain.event_parser"></a>

#### event\_parser

```python
def event_parser()
```

Reads tasks from the current cycle list and initiates them if the time is correct

<a id="main_form.UiMain.menu_show_new_batch"></a>

#### menu\_show\_new\_batch

```python
def menu_show_new_batch()
```

Menu handler new batch

<a id="main_form.UiMain.menu_show_about"></a>

#### menu\_show\_about

```python
def menu_show_about()
```

Menu handler show about form

<a id="main_form.UiMain.menu_show_log_viewer"></a>

#### menu\_show\_log\_viewer

```python
def menu_show_log_viewer()
```

Menu handler show log viewer

<a id="main_form.UiMain.menu_show_settings_viewer"></a>

#### menu\_show\_settings\_viewer

```python
def menu_show_settings_viewer()
```

Menu handler show settings viewer

<a id="main_form.UiMain.menu_show_xymanual"></a>

#### menu\_show\_xymanual

```python
def menu_show_xymanual()
```

Menu Handler show xy manual form

<a id="main_form.UiMain.menu_show_lasermanual"></a>

#### menu\_show\_lasermanual

```python
def menu_show_lasermanual()
```

Menu Handler show lasermanual form

<a id="main_form.UiMain.menu_show_ncc"></a>

#### menu\_show\_ncc

```python
def menu_show_ncc()
```

Menu Handler show NCC Form

<a id="main_form.UiMain.update_ui_batch_list"></a>

#### update\_ui\_batch\_list

```python
def update_ui_batch_list()
```

Update the btach list

<a id="main_form.UiMain.update_ui_commandlist"></a>

#### update\_ui\_commandlist

```python
def update_ui_commandlist()
```

Update the list of tasks remsining in the cycle

<a id="main_form.UiMain.update_ui_pressures"></a>

#### update\_ui\_pressures

```python
def update_ui_pressures()
```

Update the guage pressures on the top of the Main Form

<a id="main_form.UiMain.update_ui_xy_positions"></a>

#### update\_ui\_xy\_positions

```python
def update_ui_xy_positions()
```

Update the X anmd Y positions on the top of the Main Form

<a id="main_form.UiMain.update_ui_results_table"></a>

#### update\_ui\_results\_table

```python
def update_ui_results_table()
```

Upfate the results table showing completed batches and the best fit t=0 values

<a id="main_form.UiMain.move_next"></a>

#### move\_next

```python
def move_next()
```

Move to the next planchet location

<a id="main_form.UiMain.manual_message"></a>

#### manual\_message

```python
def manual_message(message)
```

Pop up message box

<a id="main_form.move_x"></a>

#### move\_x

```python
def move_x()
```

Move the x axis to the next planchet location

<a id="main_form.move_y"></a>

#### move\_y

```python
def move_y()
```

Move the Y axis to the next planchet location

<a id="main_form.restart_pi"></a>

#### restart\_pi

```python
def restart_pi(host)
```

Reboot a raspberry pi

<a id="main_form.menu_open_web_page"></a>

#### menu\_open\_web\_page

```python
def menu_open_web_page(page)
```

Menu handler - open host web page

