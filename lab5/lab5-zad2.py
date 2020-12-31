#!/usr/bin/env python3
import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 10.0]
theta = 0.0
pix2angle = 1.0
left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0
light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]
att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

buttons_state = [0,0,0,0,0,0,0,0,0] # przechowywanie stanow klawiszy 1-9
left_buttons_state = 0
right_buttons_state = 0

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

def shutdown():
    pass

def render(time):
    global theta
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        
    #diffuse
    changeValue(0, 0)
    changeValue(1, 0)
    changeValue(2, 0)  
    #ambient
    changeValue(3, 3)
    changeValue(4, 3)
    changeValue(5, 3)
    #specular
    changeValue(6, 6)
    changeValue(7, 6)
    changeValue(8, 6)  

    glRotatef(theta, 0.0, 1.0, 0.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    glFlush()


def changeValue(index, move):   # move oznacza przesuniecie o wielkokrotnosc liczby 3
                                # bo zmieniamy 3 tablice (w kazdej 3 elementy),
                                # a nacisniete przyciski trzymam w jednej 9-elem. tablicy (dla wygody)
                                # move == 0 ---> diffuse (klawisze 1-3 odpowiadaja kolejnym wartosciom)
                                # move == 3 ---> ambient (klawisze 4-6 odpowiadaja kolejnym wartosciom)
                                # move == 6 ---> specular (klawisze 7-9 odpowiadaja kolejnym wartosciom)
                                # zmiana wartosci: klawisze strzalek - w lewo i prawo                            
    global light_diffuse
    global light_ambient 
    global light_specular 
    global left_buttons_state
    global right_buttons_state    
    
    if buttons_state[index]:
        if move == 0:
            if left_buttons_state and int(round(100*light_diffuse[index - move])) > 0:
                light_diffuse[index - move] -=  0.1
                print("light_diffuse: ", light_diffuse)
                glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
            if right_buttons_state and int(round(100*light_diffuse[index - move])) < 100:
                light_diffuse[index - move] +=  0.1
                print("light_diffuse: ",light_diffuse)
                glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
            
        if move == 3:
            if left_buttons_state and int(round(100*light_ambient[index - move])) > 0:
                light_ambient[index - move] -=  0.1
                glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
                print("light_ambient: ",light_ambient)
            if right_buttons_state and int(round(100*light_ambient[index - move])) < 100:
                light_ambient[index - move] +=  0.1
                print("light_ambient: ",light_ambient)
                glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
                
        if move == 6:
            if left_buttons_state and int(round(100*light_specular[index - move])) > 0:
                light_specular[index - move] -=  0.1
                print("light_specular: ",light_specular) 
                glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)    
            if right_buttons_state and int(round(100*light_specular[index - move])) < 100:
                light_specular[index - move] +=  0.1
                print("light_specular: ",light_specular) 
                glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
              
        left_buttons_state = 0
        right_buttons_state = 0   

def keyboard_key_callback(window, key, scancode, action, mods):
    global buttons_state
    global left_buttons_state
    global right_buttons_state
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(1)
    if key == GLFW_KEY_2 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(2)
    if key == GLFW_KEY_3 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(3)
    if key == GLFW_KEY_4 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(4)
    if key == GLFW_KEY_5 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(5)
    if key == GLFW_KEY_6 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(6)
    if key == GLFW_KEY_7 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(7)
    if key == GLFW_KEY_8 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(8)
    if key == GLFW_KEY_9 and action == GLFW_PRESS:
        fillZerosAndChangeBtn(9)
    if key == GLFW_KEY_LEFT and action == GLFW_PRESS:
        left_buttons_state = 1
    if key == GLFW_KEY_RIGHT and action == GLFW_PRESS:
        right_buttons_state = 1
                  
 
def fillZerosAndChangeBtn(i):
    global buttons_state
    buttons_state = [0] * 9     # wypelnienie zerami
    buttons_state[i-1] = 1      # przypisanie '1' w tablicy odpowiedniemu przyciskowi


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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
