#!/usr/bin/env python3
import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.9, 0.9, 0.9, 1.0)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    #trojkat po lewo
    glBegin(GL_TRIANGLES)

    glColor3ub(255,0,255)   # kolor rozowy w prawym wierzch. trojkata (liczby calkowite)
    glVertex2f(50.0, 0.0)

    glColor3f(0.7,0.0, 0.0) # kolor czerwonawy w gornym wierzch. trojkata (liczby zmiennoprzec.)
    glVertex2f(0.0, 50.0)

    glColor3ub(255,165,0)   # kolor pomaranczowy w lewym wierzchoku trojkata (liczby calkowite)
    glVertex2f(-50.0, 0.0)
    glEnd()

    glFlush()

#---------------------------------------------------------------------------------------------------
#funkcja rysujaca kwadrat o srodku w punkcie (x,y) o bokach dlugosci a oraz b
def draw_rectangle(x,y,a,b): 
    glBegin(GL_TRIANGLES)       # trojkat na dole (skladajacy sie na kwadrat)
    glVertex2f(x+a/2, y-b/2)
    glVertex2f(x-a/2, y+b/2)
    glVertex2f(x-a/2, y-b/2)
    glEnd()

    glBegin(GL_TRIANGLES)       # trojkat na gorze (skladajacy sie na kwadrat)
    glVertex2f(x+a/2, y-b/2)
    glVertex2f(x-a/2, y+b/2)
    glVertex2f(x+a/2, y+b/2)
    glEnd()
#---------------------------------------------------------------------------------------------------


def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspectRatio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main() 
