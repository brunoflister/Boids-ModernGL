from model import *
import glm
import numpy as np
import random

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        #skybox
        self.skybox = SkyBox(app)

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object
        
        #grass
        n,s = 20,2
        for x in range(-n,n,s):
            for z in range(-n,n,s):
                add(Cube(app, pos = (x, -s, z)))
        #ruins
        l = 0
        for i in range(8):
            add(Cube(app, tex_id = 2, pos = (0, l ,0)))
            l = l+2
        l = 0
        for i in range(5):
            add(Cube(app, tex_id = 2, pos = (14, l ,0)))
            l = l+2
        l = 0
        for i in range(3):
            add(Cube(app, tex_id = 2, pos = (16, l ,-6)))
            l = l+2
        l = 0
        for i in range(3):
            add(Cube(app, tex_id = 2, pos = (14, l ,-10)))
            l = l+2
        add(Cube(app, tex_id = 2, pos = (12, 0 ,-7)))
        add(Cube(app, tex_id = 2, pos = (13, 0 ,-4)))

        #boids
        self.boids_list = []
        for x in range(200):
            self.boids_list.append(Boid(app, tex_id = 1, pos = (random.randint(5,10),
                                                                random.randint(3,6),
                                                                random.randint(-5, 0))))
        for boid in self.boids_list:
            add(boid)

    def update(self):
        l = 0.01
        for boid in self.boids_list:
            boid.rot.x = np.sin(self.app.time)*(0.7-l)
            boid.rot.y = self.app.time * (1.5 - l)
            l = l + 0.005
            boid.move()