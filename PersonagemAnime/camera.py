# camera.py

class Camera:
    def __init__(self):
        self.position = [0, 0, -5]
        self.rotation = [0, 0]

    def update(self, delta_time):
        import pygame
        keys = pygame.key.get_pressed()

        # Movimentos da camera
        move_speed = 2.5 * delta_time  # Quantos blocos a personagem se move
        if keys[pygame.K_w]:
            self.position[2] += move_speed
        if keys[pygame.K_s]:
            self.position[2] -= move_speed
        if keys[pygame.K_a]:
            self.position[0] -= move_speed
        if keys[pygame.K_d]:
            self.position[0] += move_speed
        if keys[pygame.K_q]:
            self.position[1] += move_speed
        if keys[pygame.K_e]:
            self.position[1] -= move_speed

        # Movimentos de rotação
        mouse_move = pygame.mouse.get_rel()
        sensitivity = 0.05  # Sensibilidade do mouse
        self.rotation[0] += mouse_move[0] * sensitivity
        self.rotation[1] += mouse_move[1] * sensitivity

    def apply(self):
        from OpenGL.GL import glRotatef, glTranslatef
        glRotatef(self.rotation[1], 1, 0, 0)
        glRotatef(self.rotation[0], 0, 1, 0)
        glTranslatef(self.position[0], self.position[1], self.position[2])
