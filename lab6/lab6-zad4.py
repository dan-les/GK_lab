#!/usr/bin/env python3
import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

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
light_diffuse = [0.9, 0.9, 1.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10, 1.0]
light_position_bottom = [0.0, 0.0, -20.0, 1.0]
att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

x_key_pressed = 1
texture_btn_Z = 1
img_counter = 0

image1 = Image.open("m1Txtr.tga")
image2 = Image.open("LusiaTxtr.tga") # moja kotka ;-) 
image3 = Image.open("jaroTxtr.tga")
image4 = Image.open("d7Txtr.tga")


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

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)
    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position_bottom)
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT1)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

def setTexture():
    global texture_btn_Z
    global img_counter

    if texture_btn_Z:
        texture_btn_Z = 0
        img_counter += 1
    if (img_counter == 4):
        img_counter = 0
        
    if img_counter == 0:
        img = image1
    if img_counter == 1:
        img = image2
    if img_counter == 2:
        img = image3
    if img_counter == 3:
        img = image4

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, img.size[0], img.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, img.tobytes("raw", "RGB", 0, -1)
    )
    
    
def shutdown():
    pass


def render(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    # wywolanie funkcji zmieniajacej wyswietlana teksture
    # ZMIANA TEKSTURY - klawisz 'z'
    setTexture()

    # podstawa ostroslupa
    glBegin(GL_POLYGON)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(5, -5, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-5, -5, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-5, 5, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(5, 5, 0)
    glEnd()

    ############################ (mozna to pominac)
    # podstawa ostroslupa (wewnatrz) - bez tekstury - zeby bylo lepiej widac wizualizacje ze scianami bocznymi ;-)
    glBegin(GL_POLYGON)
    glVertex3d(5, 5, 0)
    glVertex3d(-5, 5, 0)
    glVertex3d(-5, -5, 0)
    glVertex3d(5, -5, 0)
    glEnd()
    ############################

    glBegin(GL_TRIANGLES)
    glTexCoord2f(0, 1.0)
    glVertex3f(-5.0, 5.0, 0.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, -5.0, 0.0)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0,  -5.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()

    # klawisz 'x' wlacza i wylacza ukrywanie sciany bocznej
    if x_key_pressed:
        glBegin(GL_TRIANGLES)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(5.0,  -5.0, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(5.0, 5.0, 0.0)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0.0, 0.0, 5.0)
        glEnd()

    glBegin(GL_TRIANGLES)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(5.0,  5.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-5.0, 5.0, 0.0)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()

    glFlush()


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


def keyboard_key_callback(window, key, scancode, action, mods):
    global x_key_pressed
    global texture_btn_Z
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_X and action == GLFW_PRESS:
        if x_key_pressed == 0:
            x_key_pressed = 1
        else:
            x_key_pressed = 0
    if key == GLFW_KEY_Z and action == GLFW_PRESS:
        if texture_btn_Z == 0:
            texture_btn_Z = 1
        else:
            texture_btn_Z = 0



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
