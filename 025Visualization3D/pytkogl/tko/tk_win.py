""" define the minimal skeleton abstract class to create a Tkinter Window to use OpenGL

"""

from ctypes import sizeof

from tkinter import Frame

import sys

if sys.platform.startswith('win32'):

    from tko.win32_gdi import PFD_DRAW_TO_WINDOW, PFD_SUPPORT_OPENGL, PFD_DOUBLEBUFFER, PFD_TYPE_RGBA, \
                            PixelFormatDescriptor, get_dc, choose_pixel_format, set_pixel_format, \
                            get_pixel_format, swap_buffers


    from tko.ogl_hdr import wglCreateContext, wglMakeCurrent

elif sys.platform.startswith('linux'):

    from tko.x11_gdi import X11_None, x_open_display

    from tko.ogl_hdr import PGLint, GLX_RGBA, GLX_DEPTH_SIZE, GLX_DOUBLEBUFFER, GL_TRUE, \
                            GLX_BLUE_SIZE, GLX_GREEN_SIZE, GLX_RED_SIZE, \
                            glXChooseVisual, glXCreateContext, glXMakeCurrent, glXSwapBuffers


class TkOglWin(Frame):

    def __init__(self, parent, *args, **kwargs):

        Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.parent.title(kwargs.get('app_title', 'Opengl Test'))

        self.bind('<Configure>', self.on_resize)

        self.parent.after(100, self._cfg_tkogl)

    def _cfg_tkogl(self):

        if sys.platform.startswith('win32'):

            self.hdc = get_dc(self.winfo_id())

            pfd = PixelFormatDescriptor()
            pfd.nSize = sizeof(PixelFormatDescriptor)
            pfd.nVersion = 1
            pfd.dwFlags = PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_DOUBLEBUFFER
            pfd.iPixelType = PFD_TYPE_RGBA
            pfd.cColorBits = 24
            pfd.cDepthBits = 16

            pixel_format = choose_pixel_format(self.hdc, pfd)

            print("ChoosePixelFormat returned", pixel_format)

            print("SetPixelFormat returned", set_pixel_format(self.hdc, pixel_format, pfd))

            print("GetPixelFormat returned", get_pixel_format(self.hdc), "!!!\n")

            rc = wglCreateContext(self.hdc)
            wglMakeCurrent(self.hdc, rc)

        elif sys.platform.startswith('linux'):

            att = PGLint(
                GLX_RGBA, GLX_DOUBLEBUFFER,
                GLX_RED_SIZE, 4,
                GLX_GREEN_SIZE, 4,
                GLX_BLUE_SIZE, 4,
                GLX_DEPTH_SIZE, 16,
                X11_None
            )

            self.dpy = x_open_display(None)

            vi = glXChooseVisual(self.dpy, 0, att)

            glc = glXCreateContext(self.dpy, vi, None, GL_TRUE)

            glXMakeCurrent(self.dpy, self.winfo_id(), glc)

        self.set_ortho_view()

        self.parent.after(10, self._render_loop)

    def on_resize(self, event, arg=None):

        raise NotImplementedError

    def _render_loop(self):

        self.render_scene()

        if sys.platform.startswith('win32'):

            swap_buffers(self.hdc)

        elif sys.platform.startswith('linux'):

            glXSwapBuffers(self.dpy, self.winfo_id())

        self.parent.after(5, self._render_loop)

    def render_scene(self):

        raise NotImplementedError

    def set_ortho_view(self):

        raise NotImplementedError
