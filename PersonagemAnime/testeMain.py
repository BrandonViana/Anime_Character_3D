import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from LoadMesh import LoadMesh
from camera import Camera
import numpy as np  # Importar numpy para funções trigonométricas
import time

# Inicialize o Pygame
pygame.init()

# Configurações do projeto
screen_width = 1000
screen_height = 800
background_color = (1, 1, 1, 1)
drawing_color = (0, 0, 0, 1)

# Configuração da tela
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('OpenGL em Python')
mesh = LoadMesh("Anime_charcter.obj", GL_TRIANGLES)

object_position = [0.0, 0.0, -5.0]
object_rotation = [0.0, 0.0, 0.0]
object_scale = [1.0, 1.0, 1.0]

# Variáveis para movimento aleatório
amplitude = 2.0
frequency = 0.5

# Variáveis de controle do movimento
is_moving = True
manual_mode = False  # Modo manual colocado


def initialise():
    glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
    glColor(drawing_color)

    # Projeção
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 100.0)

    # Modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Aplicar rotação à cena
    glPushMatrix()

    # Transladar e rotacionar a personagem
    glTranslatef(*object_position)
    glRotatef(object_rotation[0], 1, 0, 0)  # Rotações no eixo X
    glRotatef(object_rotation[1], 0, 1, 0)  # Rotações no eixo Y
    glRotatef(object_rotation[2], 0, 0, 1)  # Rotações no eixo Z
    glScalef(*object_scale)

    # Definido a personagem utilizando malha
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glColor3f(drawing_color[0], drawing_color[1], drawing_color[2])

    for part in mesh.parts:
        glBegin(mesh.draw_mode)
        for i, vertex in enumerate(part.vertices):
            glNormal3f(*part.normals[i])
            glVertex3f(*vertex)
        glEnd()

    glPopMatrix()


def reset_camera(camera):
    camera.position = [0, 0, -5]
    camera.rotation = [0, 0]


camera = Camera()

done = False
initialise()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

# Coloquei também o  contador de FPS no terminal
fps_log_timer = 0

previous_time = time.time()

move_speed = 2.0
rotation_speed = 60.0

while not done:
    start_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                # Tecla 'c' pra resetar a camera
                reset_camera(camera)
            if event.key == pygame.K_p:
                # Alternar estado de movimento automático
                is_moving = not is_moving
            if event.key == pygame.K_TAB:
                # Alternar para o modo manual
                manual_mode = not manual_mode
            if event.key == pygame.K_PLUS or (
                    event.key == pygame.K_EQUALS and pygame.key.get_mods() & pygame.KMOD_SHIFT):
                # '+' para aumentar o tamanho do objeto
                object_scale = [s * 1.1 for s in object_scale]
            if event.key == pygame.K_MINUS:
                # '-' para diminuir o tamanho do objeto
                object_scale = [s * 0.9 for s in object_scale]

    current_time = time.time()
    delta_time = current_time - previous_time
    previous_time = current_time

    keys = pygame.key.get_pressed()

    move_increment = move_speed * delta_time

    if manual_mode:
        # Controla o movimento do objeto manualmente com W, A, S, D
        if keys[pygame.K_w]:
            object_position[1] += move_increment  # Mover para cima
        if keys[pygame.K_s]:
            object_position[1] -= move_increment  # Mover para baixo
        if keys[pygame.K_a]:
            object_position[0] -= move_increment  # Mover para a esquerda
        if keys[pygame.K_d]:
            object_position[0] += move_increment  # Mover para a direita
    elif is_moving:
        # Atualizar posição do objeto para movimento oscilatório
        object_position[0] = amplitude * np.sin(frequency * current_time)

    if keys[pygame.K_UP]:
        object_rotation[0] -= rotation_speed * delta_time
    if keys[pygame.K_DOWN]:
        object_rotation[0] += rotation_speed * delta_time
    if keys[pygame.K_LEFT]:
        object_rotation[1] -= rotation_speed * delta_time
    if keys[pygame.K_RIGHT]:
        object_rotation[1] += rotation_speed * delta_time

    camera.update(delta_time)
    glLoadIdentity()
    camera.apply()
    display()
    pygame.display.flip()


    end_time = time.time()
    frame_duration = end_time - start_time

    fps = 1.0 / frame_duration

    # Log do FPS e tempo de frame no terminal a cada 1 segundo
    fps_log_timer += delta_time
    if fps_log_timer >= 1.0:  # 1 segundo
        print(f"FPS: {fps:.2f}, Frame Duration: {frame_duration:.6f} seconds")
        fps_log_timer = 0

pygame.quit()
