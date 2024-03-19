import ctypes
import time

import pyautogui
from pyautogui import *

SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def pressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def releaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0,
                        ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def main():
    while True:
        time.sleep(3)
        pressKey(0x02)
        time.sleep(0.5)
        releaseKey(0x02)
        time.sleep(0.5)
        pressKey(0x039)
        time.sleep(0.5)
        releaseKey(0x39)

        print("Looking for image...")

        image = pyautogui.locateOnScreen("fish.png", confidence=0.8)

        while image is None:
            image = pyautogui.locateOnScreen("fish.png", confidence=0.8)

        print("Image found!")

        while image is not None:
            image = pyautogui.locateOnScreen("fish.png", confidence=0.8)
            pic = pyautogui.screenshot(region=(910, 490, 100, 100))
            width, height = pic.size
            found = False

            for x in range(0, 100, 5):
                for y in range(0, 100, 5):
                    r, g, b = pic.getpixel((x, y))
                    b_opposite = 255 - b
                    if b_opposite >= 120:
                        click(x + width, y + height)
                        found = True
                        break
                if found:
                    break

        print("Fish caught!")

        pressKey(0x2C)
        time.sleep(0.5)
        releaseKey(0x2C)


if __name__ == '__main__':
    main()
