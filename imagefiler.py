import win32gui
import win32ui
import os
from ctypes import windll
from PIL import Image
from settings import settings, friendlydirname
from backup import backupfile


def imager(application, batchid, batchdescription, formatteddescription):
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

        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, int(w * 1), int(h * 1))

        saveDC.SelectObject(saveBitMap)

        # Change the line below depending on whether you want the whole window
        # or just the client area.
        #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
        result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
        print(result)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)
    except:
        print('imagefiler Screen Grab Failed')
        result = 0

    if result == 1:
        #PrintWindow Succeeded
        im.save(filename)
        backupfile(filename)


def enumHandler(hwnd, lParam):
    global windowstext
    if win32gui.IsWindowVisible(hwnd):
        if win32gui.IsWindowVisible(hwnd):
            windowstext = win32gui.GetWindowText(hwnd)
            if len(windowstext) > 1:
                print('"%s"' % windowstext)

if __name__ == '__main__':
    win32gui.EnumWindows(enumHandler, None)
    #imager('microscope',300,'test image','holeone_ed',100)