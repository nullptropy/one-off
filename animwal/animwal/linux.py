# coding: utf-8

import ctypes
import atexit # to close display opened by get_handle

X11 = ctypes.CDLL("libX11.so")

class Display(ctypes.Structure):
    pass

X11.XOpenDisplay.restype = ctypes.POINTER(Display)

class Display(ctypes.Structure):
    pass

def get_handle():
    x11d = X11.XOpenDisplay(None)
    atexit.register(X11.XCloseDisplay, x11d)
    return X11.XRootWindow(x11d, X11.XDefaultScreen(x11d))