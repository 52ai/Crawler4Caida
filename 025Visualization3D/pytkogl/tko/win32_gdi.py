""" wrap GDI constants and functions to Python
"""

from ctypes import c_int, c_void_p, POINTER, Structure, WinDLL
from ctypes.wintypes import BOOL, BYTE, DWORD, HDC, WORD

_gdi32 = WinDLL('gdi32')
_user32 = WinDLL('user32')


class PixelFormatDescriptor(Structure):
    _fields_ = [
        ('nSize', WORD),
        ('nVersion', WORD),
        ('dwFlags', DWORD),
        ('iPixelType', BYTE),
        ('cColorBits', BYTE),
        ('cRedBits', BYTE),
        ('cRedShift', BYTE),
        ('cGreenBits', BYTE),
        ('cGreenShift', BYTE),
        ('cBlueBits', BYTE),
        ('cBlueShift', BYTE),
        ('cAlphaBits', BYTE),
        ('cAlphaShift', BYTE),
        ('cAccumBits', BYTE),
        ('cAccumRedBits', BYTE),
        ('cAccumGreenBits', BYTE),
        ('cAccumBlueBits', BYTE),
        ('cAccumAlphaBits', BYTE),
        ('cDepthBits', BYTE),
        ('cStencilBits', BYTE),
        ('cAuxBuffers', BYTE),
        ('iLayerType', BYTE),
        ('bReserved', BYTE),
        ('dwLayerMask', DWORD),
        ('dwVisibleMask', DWORD),
        ('dwDamageMask', DWORD),
    ]


PFD_DRAW_TO_WINDOW = 4  # Variable c_int
PFD_SUPPORT_OPENGL = 32  # Variable c_int
PFD_DOUBLEBUFFER = 1  # Variable c_int
PFD_TYPE_RGBA = 0  # Variable c_int

get_dc = _user32.GetDC
get_dc.restype = HDC
get_dc.argtypes = [c_void_p]

choose_pixel_format = _gdi32.ChoosePixelFormat
choose_pixel_format.restype = c_int
choose_pixel_format.argtypes = [c_void_p, POINTER(PixelFormatDescriptor)]

set_pixel_format = _gdi32.SetPixelFormat
set_pixel_format.restype = BOOL
set_pixel_format.argtypes = [c_void_p, c_int, POINTER(PixelFormatDescriptor)]

get_pixel_format = _gdi32.GetPixelFormat
get_pixel_format.restype = c_int
get_pixel_format.argtypes = [c_void_p]

swap_buffers = _gdi32.SwapBuffers
swap_buffers.restype = BOOL
swap_buffers.argtypes = [HDC]
