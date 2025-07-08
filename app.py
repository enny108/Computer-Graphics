import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_shape(vertices, edges):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def Cube():
    d = 1 / math.sqrt(3) # This is the default but is too large and needs to be changed
    verticies = (
        (d, -d, -d),
        (d, d, -d),
        (-d, d, -d),
        (-d, -d, -d),
        (d, -d, d),
        (d, d, d),
        (-d, -d, d),
        (-d, d, d)
        )

    edges = (
        (0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
        (6,3), (6,4), (6,7), (5,1), (5,4), (5,7)
        )
    glColor(1,1,1) # Draw the cube in white
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def Tetrahedron():
    sqrt_3 = math.sqrt(3)
    vertices = [
        ( 1,  1,  1),
        (-1, -1,  1),
        (-1,  1, -1),
        ( 1, -1, -1)
    ]
    vertices = [(x / sqrt_3, y / sqrt_3, z / sqrt_3) for x, y, z in vertices]
    edges = [
        (0,1), (0,2), (0,3),
        (1,2), (1,3), (2,3)
    ]
    glColor3f(1,1,1)
    draw_shape(vertices, edges)

def Octahedron():
    vertices = [
        ( 1, 0, 0), (-1, 0, 0),
        ( 0, 1, 0), ( 0,-1, 0),
        ( 0, 0, 1), ( 0, 0,-1)
    ]
    edges = [
        (0,2), (0,3), (0,4), (0,5),
        (1,2), (1,3), (1,4), (1,5),
        (2,4), (2,5), (3,4), (3,5)
    ]
    glColor3f(1,1,1)
    draw_shape(vertices, edges)

phi = (1 + math.sqrt(5)) / 2
inv_norm = 1 / math.sqrt(1 + phi**2)

def Dodecahedron():
    phi = (1 + math.sqrt(5)) / 2
    inv_phi = 1 / phi
    max_radius = math.sqrt(phi**2 + inv_phi**2)

    verts = []

    for x in [-1, 1]:
        for y in [-1, 1]:
            for z in [-1, 1]:
                verts.append((x, y, z))

    for y in [-phi, phi]:
        for z in [-inv_phi, inv_phi]:
            verts.append((0, y, z))

    for x in [-inv_phi, inv_phi]:
        for z in [-phi, phi]:
            verts.append((x, 0, z))

    for x in [-phi, phi]:
        for y in [-inv_phi, inv_phi]:
            verts.append((x, y, 0))

    vertices = [(x / max_radius, y / max_radius, z / max_radius) for x, y, z in verts]

    edges = []
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            if math.dist(vertices[i], vertices[j]) < 1.3 * (2 / max_radius / math.sqrt(3)):
                edges.append((i, j))

    glColor3f(1,1,1)
    draw_shape(vertices, edges)

def Icosahedron():
    phi = (1 + math.sqrt(5)) / 2
    # Normalize all vertices to lie within unit sphere
    norm = math.sqrt(1 + phi**2)
    phi /= norm
    one = 1 / norm

    vertices = [
        (0,  one,  phi), (0,  one, -phi), (0, -one,  phi), (0, -one, -phi),
        ( one,  phi, 0), ( one, -phi, 0), (-one,  phi, 0), (-one, -phi, 0),
        ( phi, 0,  one), (-phi, 0,  one), ( phi, 0, -one), (-phi, 0, -one),
    ]

    edges = []
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            if math.dist(vertices[i], vertices[j]) < 1.1 * (2 * one):
                edges.append((i, j))

    glColor3f(1, 1, 1)
    draw_shape(vertices, edges)



def Axes():
    glBegin(GL_LINES)
    glColor3f(1,0,0)
    glVertex3fv((0,0,0))
    glVertex3fv((1.5,0,0))
    glColor3f(0,1,0)
    glVertex3fv((0,0,0))
    glVertex3fv((0,1.5,0))
    glColor3f(0,0,1)
    glVertex3fv((0,0,0))
    glVertex3fv((0,0,1.5))
    glEnd()

def Circle():
    glPushMatrix()
    glLoadIdentity()
    glOrtho(-2, 2, -2, 2, -2, 2)
    glColor3f(1,0,1)
    glBegin(GL_LINE_LOOP)
    for i in range(36):
        angle = 2.0 * math.pi * i / 36
        x = math.cos(angle)
        y = math.sin(angle)
        glVertex3f(x, y, 0)
    glEnd()
    glPopMatrix()

def main():
    pygame.init()
    display = (800,800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption('Homework #1')
    glOrtho(-2, 2, -2, 2, -2, 2)
    glMatrixMode(GL_MODELVIEW)

    shape_map = {
        1: Tetrahedron,
        2: Cube,
        3: Octahedron,
        4: Dodecahedron,
        5: Icosahedron
    }
    current_shape = 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if K_1 <= event.key <= K_5:
                    current_shape = event.key - K_0

        glRotatef(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Axes()
        shape_map[current_shape]()
        Circle()
        pygame.display.flip()
        pygame.time.wait(10)

main()