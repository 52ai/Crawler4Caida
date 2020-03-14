"""entry point for Tkinter Window with OpenGL]
"""

from tkinter import Tk, YES, BOTH

from tko.tk_win import TkOglWin

from tko.ogl_hdr import GL_BLEND, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, \
                        GL_MODELVIEW, GL_ONE_MINUS_SRC_ALPHA, GL_PROJECTION, GL_QUADS, GL_RENDERER, \
                        GL_SRC_ALPHA, GL_VENDOR, GL_VERSION, \
                        glBegin, glClear, glBlendFunc, glClearColor, \
                        glClearDepth, glColor3f, glEnable, glEnd, glGetString, glFlush, \
                        glLoadIdentity, glMatrixMode, glOrtho, glRotatef, glVertex3f, glViewport


class AppOgl(TkOglWin):

    rot = 0

    def on_resize(self, event, arg=None):

        if event:
            w = event.width
            h = event.height
        else:
            if arg:
                w = arg['w']
                h = arg['h']
            else:
                raise Exception

        dx = w/h
        glViewport(0, 0, w, h)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(
            -2 * dx,
            2 * dx,
            -2,
            2,
            -2,
            2
        )

    def set_ortho_view(self):

        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0, 0, 0, 0)
        glClearDepth(1)
        glMatrixMode(GL_PROJECTION)

        self.on_resize(None, arg={
            'w': self.winfo_width(),
            'h': self.winfo_height()
        })

        print('%s - %s - %s' % (
            glGetString(GL_VENDOR),
            glGetString(GL_VERSION),
            glGetString(GL_RENDERER)
        ))

    def render_scene(self):

        self.rot += .5

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotatef(self.rot, 1, 1, 0.5)

        # Draw a simple cube.
        glBegin(GL_QUADS)

        glColor3f(0, 1, 0)
        glVertex3f(1, 1, -1)
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, 1, 1)
        glVertex3f(1, 1, 1)

        glColor3f(1, 0.5, 0)
        glVertex3f(1, -1, 1)
        glVertex3f(-1, -1, 1)
        glVertex3f(-1, -1, -1)
        glVertex3f(1, -1, -1)

        glColor3f(1, 0, 0)
        glVertex3f(1, 1, 1)
        glVertex3f(-1, 1, 1)
        glVertex3f(-1, -1, 1)
        glVertex3f(1, -1, 1)

        glColor3f(1, 1, 0)
        glVertex3f(1, -1, -1)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, 1, -1)
        glVertex3f(1, 1, -1)

        glColor3f(0, 0, 1)
        glVertex3f(-1, 1, 1)
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, -1, 1)

        glColor3f(1, 0, 1)
        glVertex3f(1, 1, -1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, -1, -1)

        glEnd()

        glFlush()


if __name__ == '__main__':

    root = Tk()

    app = AppOgl(root, width=320, height=200)

    app.pack(fill=BOTH, expand=YES)

    app.mainloop()
