import numpy as np
import glm
import moderngl as mgl
import pygame as pg

BOID_SPEED = 0.008

class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos = (0,0,0), rot = (0,0,0), scale = (1,1,1)):
        self.app = app
        self.pos = glm.vec3([p for p in pos])
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.foward = glm.vec3(0,0,-1)
        self.right = glm.vec3(1,0,0)
        self.up = glm.vec3(0,1,0)
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.vao_name = vao_name
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self):...

    def get_model_matrix(self):
        m_model = glm.mat4()
        #translate
        m_model = glm.translate(m_model, self.pos)
        #rotate
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1,0,0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0,1,0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0,0,1))
        #scale
        m_model = glm.scale(m_model, self.scale)
        return m_model
    
    def render(self):
        self.update()
        self.vao.render()

class Cube(BaseModel):
    def __init__(self, app, vao_name = 'cube', tex_id = 0, pos = (0,0,0), rot = (0,0,0), scale = (1,1,1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()
    
    def update(self):
        self.texture.use(location = 0)
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def update_shadow(self):
        self.shadow_program['m_model'].write(self.m_model)

    def render_shadow(self):
        self.update_shadow()
        self.shadow_vao.render()

    def on_init(self):
        self.program['m_view_light'].write(self.app.light.m_view_light)
        #resolution
        self.program['u_resolution'].write(glm.vec2(self.app.WIN_SIZE))
        #depth_texture
        self.depth_texture = self.app.mesh.texture.textures['depth_texture']
        self.program['shadowMap'] = 1
        self.depth_texture.use(location = 1)
        #shadow
        self.shadow_vao = self.app.mesh.vao.vaos['shadow_' + self.vao_name]
        self.shadow_program = self.shadow_vao.program
        self.shadow_program['m_proj'].write(self.camera.m_proj)
        self.shadow_program['m_view_light'].write(self.app.light.m_view_light)
        self.shadow_program['m_model'].write(self.m_model)
        #texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        #mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        #light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)

class Boid(BaseModel):
    def __init__(self, app, vao_name = 'boid', tex_id = 0, pos = (0,0,0), rot = (0,0,0), scale = (1,1,1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()
    
    def move(self):
        velocity = BOID_SPEED * self.app.delta_time
        self.pos += self.foward * velocity
    
    def update_shadow(self):
        self.shadow_program['m_model'].write(self.m_model)
    
    def render_shadow(self):
        self.update_shadow()
        self.shadow_vao.render()

    def update_boid_vectors(self):
        self.foward.z = glm.cos(self.rot.y) * glm.cos(self.rot.x)
        self.foward.y = -glm.sin(self.rot.x)
        self.foward.x = glm.sin(self.rot.y) * glm.cos(self.rot.x)

        self.foward = -glm.normalize(self.foward)
        self.right = glm.normalize(glm.cross(self.foward, glm.vec3(0,1,0)))
        self.up = glm.normalize(glm.cross(self.right, self.foward)) 

    def update(self):
        self.texture.use(location = 0)
        super().update()
        self.update_boid_vectors()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        self.m_model = self.get_model_matrix()

    def on_init(self):
        self.program['m_view_light'].write(self.app.light.m_view_light)
        #depth_texture
        self.depth_texture = self.app.mesh.texture.textures['depth_texture']
        self.program['shadowMap'] = 1
        self.depth_texture.use(location = 1)
        #shadow
        self.shadow_vao = self.app.mesh.vao.vaos['shadow_' + self.vao_name]
        self.shadow_program = self.shadow_vao.program
        self.shadow_program['m_proj'].write(self.camera.m_proj)
        self.shadow_program['m_view_light'].write(self.app.light.m_view_light)
        self.shadow_program['m_model'].write(self.m_model)
        #texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        #mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        #light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)


class SkyBox(BaseModel):
    def __init__(self, app, vao_name = 'skybox', tex_id = 'skybox', pos = (0,0,0), rot = (0,0,0), scale = (1,1,1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()
    
    def update(self):
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))

    def on_init(self):
        #texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)
        #mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))
