# None

<a id="imagefiler"></a>

# imagefiler

Application Window Screenshot Capture Module

This module provides functionality for capturing screenshots of specific application windows
and saving them as PNG image files. It is designed for mass spectrometry automation systems
to document the visual state of various instrument control applications during batch processing.

Key Features:
- Captures screenshots of named application windows using Windows API
- Saves images with descriptive filenames based on batch information
- Automatically creates directory structures for organized file storage
- Handles window enumeration for debugging and application discovery
- Provides robust error handling and logging for capture failures

Main Functions:
- imager(): Captures and saves a screenshot of a specified application window
- enumHandler(): Enumerates visible windows for debugging purposes

Dependencies:
- Windows-specific APIs (win32gui, win32ui, ctypes)
- PIL (Python Imaging Library) for image processing
- Custom modules: app_control, logmanager

Author: Gary Twinn

<a id="imagefiler.os"></a>

## os

<a id="imagefiler.windll"></a>

## windll

<a id="imagefiler.win32ui"></a>

## win32ui

<a id="imagefiler.win32gui"></a>

## win32gui

<a id="imagefiler.Image"></a>

## Image

<a id="imagefiler.settings"></a>

## settings

<a id="imagefiler.friendlydirname"></a>

## friendlydirname

<a id="imagefiler.logger"></a>

## logger

<a id="imagefiler.imager"></a>

#### imager

```python
def imager(application, batchid, batchdescription, formatteddescription)
```

Captures the graphical representation of a specific application window and saves it as
a PNG image file at a specified location.

Parameters:
    application (str): Name of the application to capture.
    batchid (str): Identifier for the batch associated with the image.
    batchdescription (str): Description of the batch.
    formatteddescription (str): A formatted description specific to the captured image.

Raises:
    No specific exceptions are raised explicitly, but the function logs errors when a
    screen capture fails.

Returns:
    None

<a id="imagefiler.enumHandler"></a>

#### enumHandler

```python
def enumHandler(hwnd, lparm)
```

Handles enumeration of windows and prints their titles if they are visible and have
a non-empty title.

Args:
    hwnd (int): Handle to a window.
    lparm (int): Application-defined value for callback function.

