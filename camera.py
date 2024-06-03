import glm
import pygame as pg


FOV = 50 # deg
NEAR = 0.1
FAR = 100
SPEED = 0.01
SENSITIVITY = 0.05

class Camera:
    def __init__(self, app, position = (0,0, 4), yaw = -90, pitch = 0):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0,1,0)
        self.right = glm.vec3(1,0,0)
        self.foward = glm.vec3(0,0,-1)
        self.yaw = yaw
        self.pitch = pitch
        #viewmatrix
        self.m_view = self.get_view_matrix()
        # projection matrix
        self.m_proj = self.get_projection_matrix()
    
    def rotate(self):
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = max(-89, min(98, self.pitch))

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.foward.x = glm.cos(yaw) * glm.cos(pitch)
        self.foward.y = glm.sin(pitch)
        self.foward.z = glm.sin(yaw) * glm.cos(pitch)

        self.foward = glm.normalize(self.foward)
        self.right = glm.normalize(glm.cross(self.foward, glm.vec3(0,1,0)))
        self.up = glm.normalize(glm.cross(self.right, self.foward)) 
    
    def update(self):
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.position += self.foward * velocity
        if keys[pg.K_s]:
            self.position -= self.foward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_q]:
            self.position += self.up * velocity
        if keys[pg.K_e]:
            self.position -= self.up * velocity

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.foward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)