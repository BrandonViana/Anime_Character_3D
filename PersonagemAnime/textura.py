# textura.py

import pygame
from OpenGL.GL import *


class Textura:
    def __init__(self, file_path):
        self.texture = self.load_texture(file_path)

    def load_texture(self, file_path):
        # Carregar imagem usando Pygame
        texture_surface = pygame.image.load(file_path)
        texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
        width = texture_surface.get_width()
        height = texture_surface.get_height()

        # Gerar ID de textura e associar a textura carregada ao ID
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        # Gerar mipmaps para a textura
        glGenerateMipmap(GL_TEXTURE_2D)

        # Definir parâmetros de textura
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        return texture_id

    def use(self):
        glBindTexture(GL_TEXTURE_2D, self.texture)
