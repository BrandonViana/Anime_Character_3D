import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from LoadMesh import LoadMesh
from camera import Camera
from textura import Textura
import numpy as np
import time

pygame.init()

# Configurações do projeto
screen_width = 1000
screen_height = 800
background_color = (0, 0, 0, 0)
drawing_color = (2, 2, 2, 2)

# Configuração da tela
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('OpenGL em Python')
mesh = LoadMesh("Anime_charcter.obj", GL_TRIANGLES)

# Textura do corpo
body_texture = Textura("textures.png")

object_position = [0.0, 0.0, -5.0]
object_rotation = [0.0, 0.0, 0.0]
object_scale = [1.0, 1.0, 1.0]

# Variáveis que movimentam o objeto sozinho
amplitude_x = 2.0
frequency_x = 0.5
amplitude_y = 1.0
frequency_y = 0.25

# Variáveis de controle do movimento
is_moving = True
manual_mode = False  # Adicionado controle manual na personagem


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
    glEnable(GL_TEXTURE_2D)

# Efeitos de luz comentado, para utilizar, descomente os códigos.

    #Habilitar iluminação
    #glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)
    #Define a posição do ponto de luz
    #light_position = [2.0, 2.0, 0.0, 1.0]
    #glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # Define outras propriedades da luz, como difusa, ambiente e especular
    #(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    #glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
    #glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Aplicar rotação na personagem
    glPushMatrix()

    # Transladar, rotacionar e escalar o objeto
    glTranslatef(*object_position)
    glRotatef(object_rotation[0], 1, 0, 0)  # Rotações no eixo X
    glRotatef(object_rotation[1], 0, 1, 0)  # Rotações no eixo Y
    glRotatef(object_rotation[2], 0, 0, 1)  # Rotações no eixo Z
    glScalef(*object_scale)  # Escalonamento do objeto

    # Código para colocar a textura no corpo
    body_texture.use()
    for part in mesh.parts:
        glBegin(mesh.draw_mode)
        for i, vertex in enumerate(part.vertices):
            glTexCoord2f(*part.tex_coords[i])
            glNormal3f(*part.normals[i])
            glVertex3f(*vertex)
        glEnd()

    glPopMatrix()


def reset_camera(camera):
    camera.position = [0, 0, -5]
    camera.rotation = [0, 0]


camera = Camera() # Puxa a Camera

done = False
initialise()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

# Colocado um contador de FPS para ver quantos fps está a personagem
fps_log_timer = 0

previous_time = time.time()

# Velocidade de movimento e rotação
move_speed = 2.0
rotation_speed = 60.0

while not done:
    start_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                # Letra "c" pra centralizar o objeto resetando a camera
                reset_camera(camera)
            if event.key == pygame.K_p:
                # Para o movimento da personagem que está automático
                is_moving = not is_moving
            if event.key == pygame.K_TAB:
                # "TAB" para alternar entre o modo manual de movimento do objeto e o modo da camera
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
        # Movimento aleatório da personagem
        object_position[0] = amplitude_x * np.sin(frequency_x * current_time)  # Movimento horizontal
        object_position[1] = amplitude_y * np.cos(frequency_y * current_time)  # Movimento vertical

    # Teclas de rotação da personagem
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

    # Duração do frame
    end_time = time.time()
    frame_duration = end_time - start_time

    fps = 1.0 / frame_duration

    # A cada 1 segundo o FPS é colocado no terminal
    fps_log_timer += delta_time
    if fps_log_timer >= 1.0:  # 1 segundo
        print(f"FPS: {fps:.2f}, Frame Duration: {frame_duration:.6f} seconds")
        fps_log_timer = 0

pygame.quit()
