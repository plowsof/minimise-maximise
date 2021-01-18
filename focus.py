"""
Developed with 32-bit python on Windows 7. Might work in other environments,
but some of these APIs might not exist before Vista.

Much credit to Eric Blade for this:
https://mail.python.org/pipermail/python-win32/2009-July/009381.html
and David Heffernan:
http://stackoverflow.com/a/15898768/9585
"""
import win32con

import sys
import ctypes
import ctypes.wintypes

import time
from win32 import win32gui
import pywintypes
from win32api import GetSystemMetrics, ChangeDisplaySettings
import platform

user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32
kernel32 = ctypes.windll.kernel32

# force aware so can get accurate measurements of taskbar height
if platform.release() == '10':
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
elif platform.release() == '7':
    ctypes.windll.user32.SetProcessDPIAware()
else:
    sys.exit(1)


WinEventProcType = ctypes.WINFUNCTYPE(
    None,
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.HWND,
    ctypes.wintypes.LONG,
    ctypes.wintypes.LONG,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.DWORD
)


# The types of events we want to listen for, and the names we'll use for
# them in the log output. Pick from
# http://msdn.microsoft.com/en-us/library/windows/desktop/dd318066(v=vs.85).aspx
eventTypes = {
    win32con.EVENT_OBJECT_FOCUS: "Focus"
}

# limited information would be sufficient, but our platform doesn't have it.
processFlag = getattr(win32con, 'PROCESS_QUERY_LIMITED_INFORMATION',
                      win32con.PROCESS_QUERY_INFORMATION)

threadFlag = getattr(win32con, 'THREAD_QUERY_LIMITED_INFORMATION',
                     win32con.THREAD_QUERY_INFORMATION)
sofId = ""
resizedDesktop = 0
# store last event time for displaying time between events

def callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread,
             dwmsEventTime):
    global lastTime
    global sofId
    #minimise a minimised window = bad?
    global sofMini
    global sofFull
    global resizedDesktop
    #sof stuff
    fgWindow = win32gui.GetForegroundWindow()
    #print("SoFid = "+str(sofId)+"\n")
    #print("fgwindow"+str(fgWindow)+"\n")

    while True:
        try:
            tup = win32gui.GetWindowPlacement(sofId)
            break
        except:
            onSoFWindowHandleChange()

    minimized = True
    if tup[1] == win32con.SW_SHOWMAXIMIZED:
        #print("mini false")
        minimized = False
    elif tup[1] == win32con.SW_SHOWMINIMIZED:
        #print("mini true")
        minimized = True
    elif tup[1] == win32con.SW_SHOWNORMAL:
        #print("normal true")
        normal = True

    if fgWindow != sofId:
        #focused window != sof
        #minimise sof just incase
        #account for vid_fullscreen 0 players
        if minimized == False:
            print("minimise sof")
            win32gui.ShowWindow(sofId, win32con.SW_MINIMIZE)

        #if we resized desktop already
        #lost focus of sof
        if origResDesktop != getDesktop():
            if resizedDesktop == 0:
                if ChangeDisplaySettings(None, 0) == win32con.DISP_CHANGE_SUCCESSFUL:
                    resizedDesktop = 1
                    print("Change res to original")
                else:
                    print("Change res to original failed")

    else:
        #we have focus of sof
        print("we have sof focus")
        theres={}
        theres = getRes(sofId)
        print("ok?")
        print(theres)
        if getDesktop() != theres:
            print("resize desktop to sof res")
            resizedDesktop = 0
            print(theres)
            if not setRes(theres[0],theres[1]):
                print("failed setting sof resolution")
            #mini then max seems to fix the LALT bug... hm
            win32gui.ShowWindow(sofId, win32con.SW_MINIMIZE)
            win32gui.ShowWindow(sofId, win32con.SW_MAXIMIZE)


def setHook(WinEventProc, eventType):
    return user32.SetWinEventHook(
        eventType,
        eventType,
        0,
        WinEventProc,
        0,
        0,
        win32con.WINEVENT_OUTOFCONTEXT
    )

def sofWinEnumHandler( hwnd, ctx ):
    global sofId
    #if win32gui.IsWindowVisible( hwnd ):
    #print (hex(hwnd), win32gui.GetWindowText( hwnd ))
    if win32gui.GetWindowText( hwnd ) == "SoF":
        sofId = hwnd

def searchForSoFWindow():
    global sofId
    sofId = ""
    while sofId == "":
        print("cant find SoF,,, ill keep looking")
        win32gui.EnumWindows( sofWinEnumHandler, None )
        time.sleep(2)
    print("Found the SoF window")

def onSoFWindowHandleChange():
    global sofRes
    sofRes = getRes(sofId)


def setRes(x,y):
    devmode = pywintypes.DEVMODEType()

    devmode.PelsWidth = x
    devmode.PelsHeight = y

    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

    if ChangeDisplaySettings(devmode, 0) != win32con.DISP_CHANGE_SUCCESSFUL:
        return False
    return True

    

def getRes(hwnd):
    retRes={}
    retRes[0]="0"
    retRes[1]="0"
    while True:
        try:
            rect = win32gui.GetWindowRect(hwnd)
            break
        except:
            searchForSoFWindow()
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    retRes[0] = w
    retRes[1] = h
    return retRes
def getDesktop():
    global resDesktop
    #print("Width =", GetSystemMetrics(0))
    #print("Height =", GetSystemMetrics(1))
    resDesktop={}
    resDesktop[0]=GetSystemMetrics(0)
    resDesktop[1]=GetSystemMetrics(1)
    return resDesktop

def main():
    global sofId
    global origResDesktop
    #wait for SoF id to be gotten first
    #then continue 
    origResDesktop={}
    origResDesktop = getDesktop()
    print(origResDesktop)
    searchForSoFWindow()
    onSoFWindowHandleChange()
    print("SoF found. Adding hooks.")

    ole32.CoInitialize(0)

    WinEventProc = WinEventProcType(callback)
    user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE

    hookIDs = [setHook(WinEventProc, et) for et in eventTypes.keys()]
    if not any(hookIDs):
        print('SetWinEventHook failed')
        sys.exit(1)

    msg = ctypes.wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
        user32.TranslateMessageW(msg)
        user32.DispatchMessageW(msg)

    for hookID in hookIDs:
        user32.UnhookWinEvent(hookID)
    ole32.CoUninitialize()


if __name__ == '__main__':
    main()
