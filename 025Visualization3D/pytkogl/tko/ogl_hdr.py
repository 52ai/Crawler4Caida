""" define constants and wrap OpenGL functions to Python
"""

from ctypes import c_bool, c_char_p, c_double, c_float, c_int, c_uint, c_ulong, c_void_p, POINTER

import sys

if sys.platform.startswith('win32'):

    from ctypes import WinDLL

    _libGL = WinDLL('opengl32')

elif sys.platform.startswith('linux'):

    from ctypes import cdll

    # Shared library path hardcode for Xubuntu 15.10

    _libGL = cdll.LoadLibrary('/usr/lib/x86_64-linux-gnu/mesa/libGL.so.1')

else:
    raise NotImplementedError

# Data types for Linux Platform

XID = c_ulong
GLXDrawable = XID

# Data types for OpenGL

GLbitfield = c_uint
GLubyte = c_char_p
GLclampf = c_float
GLclampd = c_double
GLdouble = c_double
GLenum = c_uint
GLfloat = c_float
GLint = c_int

GL_BLEND = 0x0BE2
GL_COLOR_BUFFER_BIT = 0x00004000
GL_DEPTH_BUFFER_BIT = 0x00000100
GL_DEPTH_TEST = 0x0B71
GL_MODELVIEW = 0x1700
GL_ONE_MINUS_SRC_ALPHA = 0x0303
GL_PROJECTION = 0x1701
GL_QUADS = 0x0007
GL_RENDERER = 0x1F01
GL_SRC_ALPHA = 0x0302
GL_VENDOR = 0x1F00
GL_VERSION = 0x1F02
GL_TRUE = 1

# Constants for Linux Platform

# Hardcode number of array elements of int type
# used in this example

PGLint = GLint * 11

GLX_RGBA = 4
GLX_RED_SIZE = 8
GLX_GREEN_SIZE = 9
GLX_BLUE_SIZE = 10
GLX_DEPTH_SIZE = 12
GLX_DOUBLEBUFFER = 5


# OpenGL Function Definitions

glBegin = _libGL.glBegin
glBegin.restype = None
glBegin.argtypes = [GLenum]

glClear = _libGL.glClear
glClear.restype = None
glClear.argtypes = [GLbitfield]

glBlendFunc = _libGL.glBlendFunc
glBlendFunc.restype = None
glBlendFunc.argtypes = [GLenum, GLenum]

glClearColor = _libGL.glClearColor
glClearColor.restype = None
glClearColor.argtypes = [GLclampf, GLclampf, GLclampf, GLclampf]

glClearDepth = _libGL.glClearDepth
glClearDepth.restype = None
glClearDepth.argtypes = [GLclampd]

glColor3f = _libGL.glColor3f
glColor3f.restype = None
glColor3f.argtypes = [GLfloat, GLfloat, GLfloat]

glEnable = _libGL.glEnable
glEnable.restype = None
glEnable.argtypes = [GLenum]

glEnd = _libGL.glEnd
glEnd.restype = None
glEnd.argtypes = None

glFlush = _libGL.glFlush
glFlush.restype = None
glFlush.argtypes = None

glGetString = _libGL.glGetString
glGetString.restype = GLubyte
glGetString.argtypes = [GLenum]

glLoadIdentity = _libGL.glLoadIdentity
glLoadIdentity.restype = None
glLoadIdentity.argtypes = None

glMatrixMode = _libGL.glMatrixMode
glMatrixMode.restype = None
glMatrixMode.argtypes = None

glOrtho = _libGL.glOrtho
glOrtho.restype = None
glOrtho.argtypes = [GLdouble, GLdouble, GLdouble, GLdouble, GLdouble, GLdouble]

glRotatef = _libGL.glRotatef
glRotatef.restype = None
glRotatef.argtypes = [GLfloat, GLfloat, GLfloat, GLfloat]

glVertex3f = _libGL.glVertex3f
glVertex3f.restype = None
glVertex3f.argtypes = [GLfloat, GLfloat, GLfloat]

glViewport = _libGL.glViewport
glViewport.restype = None
glViewport.argtypes = [GLint, GLint, GLint, GLint]

if sys.platform.startswith('win32'):

    wglCreateContext = _libGL.wglCreateContext
    wglCreateContext.restype = c_void_p
    wglCreateContext.argtypes = [c_void_p]

    wglMakeCurrent = _libGL.wglMakeCurrent
    wglMakeCurrent.restype = c_bool
    wglMakeCurrent.argtypes = [c_void_p, c_void_p]

elif sys.platform.startswith('linux'):

    glXChooseVisual = _libGL.glXChooseVisual
    glXChooseVisual.argtypes = [c_void_p, c_int, POINTER(c_int)]
    glXChooseVisual.restype = c_void_p

    glXCreateContext = _libGL.glXCreateContext
    glXCreateContext.argtypes = [c_void_p, c_void_p, c_void_p, c_bool]
    glXCreateContext.restype = c_void_p

    glXMakeCurrent = _libGL.glXMakeCurrent
    glXMakeCurrent.argtypes = [c_void_p, GLXDrawable, c_void_p]
    glXMakeCurrent.restype = c_bool

    glXSwapBuffers = _libGL.glXSwapBuffers
    glXSwapBuffers.argtypes = [c_void_p, GLXDrawable]
    glXSwapBuffers.resttype = None
