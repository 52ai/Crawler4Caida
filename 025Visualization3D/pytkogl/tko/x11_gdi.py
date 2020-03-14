from ctypes import c_char_p, c_void_p, cdll

# Shared library path hardcode for Xubuntu 15.10

_x11lib = cdll.LoadLibrary('/usr/lib/x86_64-linux-gnu/libX11.so')

X11_None = 0

x_open_display = _x11lib.XOpenDisplay
x_open_display.argtypes = [c_char_p]
x_open_display.restype = c_void_p
