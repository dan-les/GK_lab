#!/usr/bin/env python3
import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

val = random.random()

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.3, 0.3, 0.3, 1.0)

def shutdown():
    pass

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    random.seed(val)
    q = random.random()     
    w = random.random()
    e = random.random()
    glColor3f(q, w, e)
    
    #draw_carpet_controller(0,0,200,100,5)
    draw_carpet_controller(0,0,120,70,3)
    #draw_carpet_controller(0,0,120,70,2)
    glFlush()

#-----------------------------------------------------------------------------------
#funkcja rysujaca kwadrat o wiercholku w punkcie (x,y) i bokach a i b
def draw_rectangle(x, y, a, b):
      
    glBegin(GL_TRIANGLES)       # trojkat na dole (skladajacy sie na kwadrat)
    glVertex2f(x, y)
    glVertex2f(x, y + b)
    glVertex2f(x + a, y)
    glEnd()

    glBegin(GL_TRIANGLES)       # trojkat na gorze (skladajacy sie na kwadrat)
    glVertex2f(x, y + b)
    glVertex2f(x + a, y)
    glVertex2f(x + a, y + b)
    glEnd()
#-----------------------------------------------------------------------------------
def draw_carpet_controller(x, y, a, b, level):
    if level == 0:
        draw_rectangle(x, y, a, b)
    else:
        level = level-1  
        newA = a/3      # podzial boku a na 3 czesci
        newB = b/3      # podzial boku b na 3 czesci

        for m in range(3):
            for n in range(3):
                if m!=1 or n!=1:
                    newY = y - newB + n * newB
                    newX = x - newA + m * newA
                    draw_carpet_controller(newX, newY, newA, newB, level)
#-----------------------------------------------------------------------------------       


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
        #glfwSwapInterval(40)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main() 
