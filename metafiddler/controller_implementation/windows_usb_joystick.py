
# Windows USB Joysick consumer

# Adapted from:
# https://gist.github.com/rdb/8883307
#   Released by rdb under the Unlicense (unlicense.org)

# I've stripped much of rdb's rich goodness in favor
# of code readability: python is a hodgepodge when it comes
# To hardware-specific calls.

# The strong point of this implementation was:
#  * Didn't require window focus (pygame)
#  Being able to grab input no matter whether the app was active
# or not was key to this whole thing working

import metafiddler.event 

from math import floor, ceil
import time
import ctypes
#import _winreg as winreg
import winreg
from ctypes.wintypes import WORD, UINT, DWORD
from ctypes.wintypes import WCHAR as TCHAR

# Its possible the JS is not added and if so lets just get on with things
joystick_provisioned = 0

# Fetch function pointers
joyGetNumDevs = ctypes.windll.winmm.joyGetNumDevs
joyGetPos = ctypes.windll.winmm.joyGetPos
joyGetPosEx = ctypes.windll.winmm.joyGetPosEx
joyGetDevCaps = ctypes.windll.winmm.joyGetDevCapsW

# Define constants
MAXPNAMELEN = 32
MAX_JOYSTICKOEMVXDNAME = 260

JOY_RETURNX = 0x1
JOY_RETURNY = 0x2
JOY_RETURNZ = 0x4
JOY_RETURNR = 0x8
JOY_RETURNU = 0x10
JOY_RETURNV = 0x20
JOY_RETURNPOV = 0x40
JOY_RETURNBUTTONS = 0x80
JOY_RETURNRAWDATA = 0x100
JOY_RETURNPOVCTS = 0x200
JOY_RETURNCENTERED = 0x400
JOY_USEDEADZONE = 0x800
JOY_RETURNALL = JOY_RETURNX | JOY_RETURNY | JOY_RETURNZ | JOY_RETURNR | JOY_RETURNU | JOY_RETURNV | JOY_RETURNPOV | JOY_RETURNBUTTONS

# This is the mapping for my XBox 360 controller.
button_names = ['a', 'b', 'x', 'y', 'tl', 'tr', 'back', 'start', 'thumbl', 'thumbr']


# Define some structures from WinMM that we will use in function calls.
class JOYCAPS(ctypes.Structure):
    _fields_ = [
        ('wMid', WORD),
        ('wPid', WORD),
        ('szPname', TCHAR * MAXPNAMELEN),
        ('wXmin', UINT),
        ('wXmax', UINT),
        ('wYmin', UINT),
        ('wYmax', UINT),
        ('wZmin', UINT),
        ('wZmax', UINT),
        ('wNumButtons', UINT),
        ('wPeriodMin', UINT),
        ('wPeriodMax', UINT),
        ('wRmin', UINT),
        ('wRmax', UINT),
        ('wUmin', UINT),
        ('wUmax', UINT),
        ('wVmin', UINT),
        ('wVmax', UINT),
        ('wCaps', UINT),
        ('wMaxAxes', UINT),
        ('wNumAxes', UINT),
        ('wMaxButtons', UINT),
        ('szRegKey', TCHAR * MAXPNAMELEN),
        ('szOEMVxD', TCHAR * MAX_JOYSTICKOEMVXDNAME),
    ]

class JOYINFO(ctypes.Structure):
    _fields_ = [
        ('wXpos', UINT),
        ('wYpos', UINT),
        ('wZpos', UINT),
        ('wButtons', UINT),
    ]

class JOYINFOEX(ctypes.Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('dwFlags', DWORD),
        ('dwXpos', DWORD),
        ('dwYpos', DWORD),
        ('dwZpos', DWORD),
        ('dwRpos', DWORD),
        ('dwUpos', DWORD),
        ('dwVpos', DWORD),
        ('dwButtons', DWORD),
        ('dwButtonNumber', DWORD),
        ('dwPOV', DWORD),
        ('dwReserved1', DWORD),
        ('dwReserved2', DWORD),
    ]


def init():
    # Get the number of supported devices (usually 16).
    num_devs = joyGetNumDevs()
    if num_devs == 0:
        print("Joystick driver not loaded.")

    # Number of the joystick to open.
    joy_id = 0

    # Check if the joystick is plugged in.
    info = JOYINFO()
    p_info = ctypes.pointer(info)
    if joyGetPos(0, p_info) != 0:
        print("Joystick %d not plugged in." % (joy_id + 1))
        
    else:
        print("Joystick provisioned\n\n",
            "Mapping:\n",
            "🡆 - next\n",
            "🡄 - prev\n",
            "🡅 - volume up\n",
            "🡇 - volume down\n",
            "[sel] - stop\n",
            "[start] - start\n",
            "A - Playlist A\n",
            "B - Playlist B\n"
            )

        joystick_provisioned = 1

        # Get device capabilities.
        caps = JOYCAPS()
        if joyGetDevCaps(joy_id, ctypes.pointer(caps), ctypes.sizeof(JOYCAPS)) != 0:
            print("Failed to get device capabilities.")
            exit()

        print("Driver name:", caps.szPname)

        # Fetch the name from registry.
        key = None
        if len(caps.szRegKey) > 0:
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "System\\CurrentControlSet\\Control\\MediaResources\\Joystick\\%s\\CurrentJoystickSettings" % (caps.szRegKey))
            except WindowsError:
                key = None

        if key:
            oem_name = winreg.QueryValueEx(key, "Joystick%dOEMName" % (joy_id + 1))
            if oem_name:
                key2 = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "System\\CurrentControlSet\\Control\\MediaProperties\\PrivateProperties\\Joystick\\OEM\\%s" % (oem_name[0]))
                if key2:
                    oem_name = winreg.QueryValueEx(key2, "OEMName")
                    print( "OEM name:", oem_name[0])
                key2.Close()

        # Set the initial button states.
        button_states = {}
        for b in range(caps.wNumButtons):
            name = button_names[b]
            if (1 << b) & info.wButtons:
                button_states[name] = True
            else:
                button_states[name] = False


        buttons_text = ""

        # Initialise the JOYINFOEX structure.
        info = JOYINFOEX()
        info.dwSize = ctypes.sizeof(JOYINFOEX)
        info.dwFlags = JOY_RETURNBUTTONS | JOY_RETURNCENTERED | JOY_RETURNPOV | JOY_RETURNU | JOY_RETURNV | JOY_RETURNX | JOY_RETURNY | JOY_RETURNZ
        p_info = ctypes.pointer(info)

# Fetch new joystick data until it returns non-0 (that is, it has been unplugged)
def poll(): 
    
    # No joystick provisioned, lets bounce.
    if joystick_provisioned == 0:
        return

    if joyGetPosEx(0, p_info) == 0:
        # Remap the values to float
        x = (info.dwXpos - 32767) / 32768.0
        y = (info.dwYpos - 32767) / 32768.0

        # Figure out which buttons are pressed.
        for b in range(caps.wNumButtons):
            pressed = (0 != (1 << b) & info.dwButtons)
            name = button_names[b]
            button_states[name] = pressed

        # Format a list of currently pressed buttons.
        buttons_text = ""
        for btn in button_names:
            if button_states.get(btn):
                buttons_text += btn + ' '

        # Value here is kind of not always == 1
        if x > .5:
            # X/Y to the left
            return(mafiddler.event.NEXT)
        elif x < -.5:
            # X/Y to the right
            return(metafiddler.event.PREVIOUS)
        elif y  > .5:
            # X/Y down
            return(metafiddler.event.VOLUME_DOWN)
        elif y < -.5:
            # X/Y up
            return(metafiddler.event.VOLUME_UP)
        
        if (button_states.get("thumbl")):
            return(metafiddler.event.PLAY)
        if (button_states.get("thumbr")):
            return(metafiddler.event.STOP)
       
        if (button_states.get("x")):
            return(metafiddler.event.PLAYLIST_A)
        if (button_states.get("b")):
            return(metafiddler.event.PLAYLIST_B)

    return(metafiddler.event.NONE)
