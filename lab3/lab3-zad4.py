#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from math import *
import random

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass

def spin (angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

n = 15
matrix = np.zeros((n+1,n+1,3))
matrixColor = np.zeros((n+1,n+1,3))


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    axes()
    spin(time*180/pi)
    drawEggTriangleStrip()
    glFlush()

#wypelnienie tablicy wartosciami
def matrixValues():
    for i in range (0, n + 1):
        for j in range (0, n + 1):
            u = i/n
            v = j/n
            #wsp. 'x'
            matrix[i][j][0] = (-90 * pow(u, 5) + 225 * pow(u, 4) - 270 * pow(u, 3) + 180 * pow(u, 2) - 45 * u) * cos(pi * v)
            #wsp. 'y'
            matrix[i][j][1] =  160 * pow(u, 4) - 320 * pow(u, 3) + 160 * pow(u, 2)
            #wsp. 'z'
            matrix[i][j][2] = (-90 * pow(u, 5) + 225 * pow(u, 4) - 270 * pow(u, 3) + 180 * pow(u, 2) - 45 * u) * sin(pi * v)

#wypelnienie tablicy z kolorami wartosciami            
def matrixColorValues():
    for i in range (0, n + 1):
        for j in range (0, n + 1):
            u = i/n
            v = j/n
            matrixColor[i][j][0] =  random.random()
            matrixColor[i][j][1] =  random.random()
            matrixColor[i][j][2] =  random.random()
            
    
    #ustawnienie takiego samego koloru przy laczeniu
    for i in range (0, int(n / 2) - 1):
        matrixColor[n - i][n][0] = matrixColor[i][0][0]
        matrixColor[n - i][n][1] = matrixColor[i][0][1]
        matrixColor[n - i][n][2] = matrixColor[i][0][2]
            
def drawEggTriangleStrip():
    for i in range (0, n):
        for j in range (0, n):
            glBegin(GL_TRIANGLE_STRIP)
            glColor3f(matrixColor[i][j][0], matrixColor[i][j][1], matrixColor[i][j][2])
            glVertex3f(matrix[i][j][0], matrix[i][j][1] - 5, matrix[i][j][2])  
            
            glColor3f(matrixColor[i + 1][j][0], matrixColor[i + 1][j][1], matrixColor[i + 1][j][2])
            glVertex3f(matrix[i + 1][j][0], matrix[i + 1][j][1] - 5, matrix[i + 1][j][2])
     
            glColor3f(matrixColor[i][j + 1][0], matrixColor[i][j + 1][1], matrixColor[i][j + 1][2])
            glVertex3f(matrix[i][j + 1][0], matrix[i][j + 1][1] - 5, matrix[i][j + 1][2])  
            
            glColor3f(matrixColor[i + 1][j+1][0], matrixColor[i + 1][j+1][1], matrixColor[i + 1][j+1][2])
            glVertex3f(matrix[i + 1][j+1][0], matrix[i + 1][j+1][1] - 5, matrix[i + 1][j+1][2])
            glEnd();
 
          
def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)


    random.seed(1)
    matrixColorValues()
    matrixValues()    
    
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
