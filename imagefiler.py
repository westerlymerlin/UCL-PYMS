"""
Image Filer
Author: Gary Twinn
"""
import os
from ctypes import windll
import win32ui
import win32gui
from PIL import Image
from app_control import settings, friendlydirname
from logmanager import logger


def imager(application, batchid, batchdescription, formatteddescription):
    """Grab a screenshot of the application and save it as a file"""
    filepath = settings['MassSpec']['datadirectory'] + \
               friendlydirname(batchid + ' ' + batchdescription)
    os.makedirs(filepath, exist_ok=True)
    filename = filepath + '\\' + friendlydirname(formatteddescription) + ' ' + application + '.png'
    try:

        hwnd = win32gui.FindWindow(None, settings['image'][application])

        # Change the line below depending on whether you want the whole window
        # or just the client area.
        #left, top, right, bot = win32gui.GetClientRect(hwnd)
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top

        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc  = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        save_bit_map = win32ui.CreateBitmap()
        save_bit_map.CreateCompatibleBitmap(mfc_dc, int(w * 1), int(h * 1))

        save_dc.SelectObject(save_bit_map)

        # Change the line below depending on whether you want the whole window
        # or just the client area.
        #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
        result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 0)
        logger.debug('Imagefiler: Screen grab %s', result)

        bmpinfo = save_bit_map.GetInfo()
        bmpstr = save_bit_map.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(save_bit_map.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)
    except:
        logger.error('imagefiler Screen Grab Failed')
        result = 0

    if result == 1:
        #PrintWindow Succeeded
        im.save(filename)

def enumHandler(hwnd, lparm):
    """List all open windows - used for debugging purposes."""
    global windowstext
    if win32gui.IsWindowVisible(hwnd):
        if win32gui.IsWindowVisible(hwnd):
            windowstext = win32gui.GetWindowText(hwnd)
            if len(windowstext) > 1:
                print('"%s"' % windowstext)

if __name__ == '__main__':
    # used for debugging only
    win32gui.EnumWindows(enumHandler, None)
    #imager('microscope',300,'test image','holeone_ed',100)
