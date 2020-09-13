"""Windows USB Joysick consumer

Adapted from:
https://gist.github.com/rdb/8883307
  Released by rdb under the Unlicense (unlicense.org)

The strong point of this implementation was:
 * Didn't require window focus (pygame)
 Being able to grab input no matter whether the app was active
or not was key to this whole thing working

"""

import ctypes
import logging
from tabulate import tabulate
import sys
import winreg
from ctypes.wintypes import WORD, UINT, DWORD
from ctypes.wintypes import WCHAR as TCHAR
from metafiddler.input_events import InputEvent

# Its possible the JS is not added and if so lets just get on with things
joystick_provisioned = False

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
JOY_RETURNALL = (
    JOY_RETURNX
    | JOY_RETURNY
    | JOY_RETURNZ
    | JOY_RETURNR
    | JOY_RETURNU
    | JOY_RETURNV
    | JOY_RETURNPOV
    | JOY_RETURNBUTTONS
)

# Name mappings to make content marginally less arbitrary
# xbox mappings
# button_names = ['a', 'b', 'x', 'y', 'tl', 'tr', 'back', 'start', 'thumbl', 'thumbr']
# This is the mapping for the NES/SNES USBs I have, different from the XBOX mapping this came ith by a fair mile.:
button_names = [
    "x",
    "a",
    "b",
    "y",
    "left",
    "right",
    "NONE-A",
    "NONE-B",
    "select",
    "start",
]


class JOYCAPS(ctypes.Structure):
    """Define some structures from WinMM that we will use in function calls."""

    _fields_ = [
        ("wMid", WORD),
        ("wPid", WORD),
        ("szPname", TCHAR * MAXPNAMELEN),
        ("wXmin", UINT),
        ("wXmax", UINT),
        ("wYmin", UINT),
        ("wYmax", UINT),
        ("wZmin", UINT),
        ("wZmax", UINT),
        ("wNumButtons", UINT),
        ("wPeriodMin", UINT),
        ("wPeriodMax", UINT),
        ("wRmin", UINT),
        ("wRmax", UINT),
        ("wUmin", UINT),
        ("wUmax", UINT),
        ("wVmin", UINT),
        ("wVmax", UINT),
        ("wCaps", UINT),
        ("wMaxAxes", UINT),
        ("wNumAxes", UINT),
        ("wMaxButtons", UINT),
        ("szRegKey", TCHAR * MAXPNAMELEN),
        ("szOEMVxD", TCHAR * MAX_JOYSTICKOEMVXDNAME),
    ]


class JOYINFO(ctypes.Structure):
    _fields_ = [
        ("wXpos", UINT),
        ("wYpos", UINT),
        ("wZpos", UINT),
        ("wButtons", UINT),
    ]


class JOYINFOEX(ctypes.Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("dwFlags", DWORD),
        ("dwXpos", DWORD),
        ("dwYpos", DWORD),
        ("dwZpos", DWORD),
        ("dwRpos", DWORD),
        ("dwUpos", DWORD),
        ("dwVpos", DWORD),
        ("dwButtons", DWORD),
        ("dwButtonNumber", DWORD),
        ("dwPOV", DWORD),
        ("dwReserved1", DWORD),
        ("dwReserved2", DWORD),
    ]


class Joystick:
    def __init__(self):
        global info
        global caps
        global button_states
        global joystick_provisioned

        # Get the number of supported devices (usually 16).
        num_devs = joyGetNumDevs()
        if num_devs == 0:
            logging.warn("Joystick driver not loaded.")

        # Number of the joystick to open.
        joy_id = 0

        # Check if the joystick is plugged in.
        info = JOYINFO()
        p_info = ctypes.pointer(info)
        if joyGetPos(0, p_info) != 0:
            logging.info("Joystick %d not plugged in.", (joy_id + 1))

        else:
            print(
                "\n"
                + tabulate([["Joystick mapping"]], tablefmt="github")
                + "\n"
                + tabulate(
                    [
                        ["[right]", "next"],
                        ["[left]", "prev"],
                        ["[up]", "volume up"],
                        ["[down]", "volume down"],
                        ["[sel]", "stop"],
                        ["[start]", "start"],
                        ["left", "seek back"],
                        ["right", "seek forward"],
                        ["A", "Playlist A"],
                        ["B", "Playlist B"],
                        ["X", "Playlist X"],
                        ["Y", "Playlist Y"],
                    ],
                    tablefmt="grid",
                )
            )

            joystick_provisioned = True

            # Get device capabilities.
            caps = JOYCAPS()
            if joyGetDevCaps(joy_id, ctypes.pointer(caps), ctypes.sizeof(JOYCAPS)) != 0:
                logging.critical("FATAL: Failed to get device capabilities.")
                sys.exit()

            # logging.debug("Driver name: " + caps.szPname)

            # Fetch the name from registry.
            key = None
            if len(caps.szRegKey) > 0:
                try:
                    key = winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER,
                        "System\\CurrentControlSet\\Control\\MediaResources\\Joystick\\%s\\CurrentJoystickSettings"
                        % (caps.szRegKey),
                    )
                except WindowsError:
                    key = None

            if key:
                oem_name = winreg.QueryValueEx(key, "Joystick%dOEMName" % (joy_id + 1))
                if oem_name:
                    key2 = winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER,
                        "System\\CurrentControlSet\\Control\\MediaProperties\\PrivateProperties\\Joystick\\OEM\\%s"
                        % (oem_name[0]),
                    )
                    if key2:
                        oem_name = winreg.QueryValueEx(key2, "OEMName")
                        logging.debug("OEM name: " + oem_name[0])
                    key2.Close()

            # Set the initial button states.
            button_states = {}
            for b in range(caps.wNumButtons):
                name = button_names[b]
                if (1 << b) & info.wButtons:
                    button_states[name] = True
                else:
                    button_states[name] = False

            # Initialise the JOYINFOEX structure.
            info = JOYINFOEX()
            info.dwSize = ctypes.sizeof(JOYINFOEX)
            info.dwFlags = (
                JOY_RETURNBUTTONS
                | JOY_RETURNCENTERED
                | JOY_RETURNPOV
                | JOY_RETURNU
                | JOY_RETURNV
                | JOY_RETURNX
                | JOY_RETURNY
                | JOY_RETURNZ
            )
            p_info = ctypes.pointer(info)

    # Fetch new joystick data until it returns non-0 (that is, it has been unplugged)
    def poll(self):
        """See if there is any input on this device"""
        global p_info
        global info
        global caps
        global button_states
        global joystick_provisioned

        # No joystick provisioned, lets bounce.
        if not joystick_provisioned:
            return

        if joyGetPosEx(0, p_info) == 0:
            # Remap the values to float
            x = (info.dwXpos - 32767) / 32768.0
            y = (info.dwYpos - 32767) / 32768.0

            # Figure out which buttons are pressed.
            for b in range(caps.wNumButtons):
                pressed =  (1 << b) & info.dwButtons != 0
                name = button_names[b]

                if pressed and not button_states[name] == pressed:
                    logging.debug("button '" + name + "'pressed'")

                button_states[name] = pressed

            # X/Y JOYSTICK EVENTS
            # -----------------------------------------------------------------------------
            # Value here is kind of not always == 1
            if x > 0.5:
                # X/Y to the left
                return InputEvent.NEXT
            elif x < -0.5:
                # X/Y to the right
                return InputEvent.PREVIOUS
            elif y > 0.5:
                # X/Y down
                return InputEvent.VOLUME_DOWN
            elif y < -0.5:
                # X/Y up
                return InputEvent.VOLUME_UP

            # Metabuttons
            # -----------------------------------------------------------------------------

            # PLAYER BUTTONS
            # -----------------------------------------------------------------------------
            buttonmap = {
                "a": InputEvent.PLAYLIST_A,
                "b": InputEvent.PLAYLIST_B,
                "x": InputEvent.PLAYLIST_X,
                "y": InputEvent.PLAYLIST_Y,
                "left": InputEvent.SEEK_BACK,
                "right":  InputEvent.SEEK_FORWARD,
                "start": InputEvent.PLAY,
                "select": InputEvent.STOP

            }
            for button in buttonmap.keys():
                if button_states.get(button):
                    return buttonmap[button]


        return InputEvent.NONE
