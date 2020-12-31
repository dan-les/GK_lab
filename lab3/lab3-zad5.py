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

n = 20
matrix = np.zeros((n+1,n+1,3))
matrixColor = np.zeros((n+1,n+1,3))


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    axes()
    spin(time*180/pi)
    # --------- LANCUCH ---------
    # WYBOR RODZAJU TORUSA:
    # 0  <--- z linii
    # 1  <--- wypelniony (z trojkatow)
    choice = 0
    
    if choice == 0:
        drawTorusLines(0.7,0.0,0.7,0.0)   
        drawTorusLines(0.3,0.5,0.2,2.5)    
        drawTorusLines(0.1,0.9,0.5,-5.0)   
        drawTorusLines(0.9,0.1,0.1,-2.5)  
        drawTorusLines(0.9,0.8,0.1, 5)
        drawTorusLines(0.3,0.3,0.67, 7.5) 
        spin(90)
        drawTorusLines(0.9,0.3,0.67, -7.5)
        
    else:
        drawTorusFilled(0.7,0.0,0.7,0.0)   
        drawTorusFilled(0.3,0.5,0.2,2.5)    
        drawTorusFilled(0.1,0.9,0.5,-5.0)   
        drawTorusFilled(0.9,0.1,0.1,-2.5)  
        drawTorusFilled(0.9,0.8,0.1, 5)
        drawTorusFilled(0.3,0.3,0.67, 7.5) 
        spin(90)
        drawTorusFilled(0.9,0.3,0.67, -7.5)
 
    glFlush()
    
#wypelnienie tablicy wartosciami
def matrixValues():
    for i in range (0, n + 1):
        for j in range (0, n + 1):
            u = i/n
            v = j/n
            R = 2
            r = 0.5
            #wsp. 'x'
            matrix[i][j][0] =  (R + r * cos(2*pi*v))* cos(2*pi*u)
            #wsp. 'y'
            matrix[i][j][1] =  (R + r * cos(2*pi*v))* sin(2*pi*u)
            #wsp. 'z'
            matrix[i][j][2] =  r * sin(2*pi*v)
            #print(matrix)
  
def drawTorusLines(x,y,z,c):
    spin(90)
    glColor3f(x,y,z)
    for i in range (0, n):
        for j in range (0, n): 
            glBegin(GL_LINES)
            glVertex3f(matrix[i][j][0], matrix[i][j][1] + c, matrix[i][j][2])
            glVertex3f(matrix[i + 1][j][0], matrix[i + 1][j][1] + c , matrix[i + 1][j][2])
 
            glVertex3f(matrix[i][j][0], matrix[i][j][1] + c,  matrix[i][j][2])
            glVertex3f(matrix[i][j + 1][0], matrix[i][j + 1][1] + c, matrix[i][j + 1][2])
            glEnd()
            
            
def drawTorusFilled(x,y,z,c):
    spin(90)
    glColor3f(x,y,z)
    for i in range (0, n):
        for j in range (0, n): 
            glBegin(GL_TRIANGLES)     
            glVertex3f(matrix[i][j][0], matrix[i][j][1] + c, matrix[i][j][2])  
            glVertex3f(matrix[i][j + 1][0], matrix[i][j + 1][1] + c, matrix[i][j + 1][2])             
            glVertex3f(matrix[i + 1][j][0], matrix[i + 1][j][1] + c, matrix[i + 1][j][2])
            glVertex3f(matrix[i][j+1][0], matrix[i][j+1][1] + c,  matrix[i][j+1][2])
            glVertex3f(matrix[i + 1][j][0], matrix[i + 1][j][1] + c,  matrix[i + 1][j][2])
            glVertex3f(matrix[i + 1][j + 1][0], matrix[i + 1][j + 1][1] + c, matrix[i + 1][j + 1][2])
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
