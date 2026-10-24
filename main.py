from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

scene.fog_color = color.hex("#0b1020")
scene.fog_density = (10, 60)

ground1 = 'textures/ground.png'
ground2 = 'textures/ground2.png'

ground = Entity(model = 'plane', scale = 250, texture_scale = (250, 250), texture = (ground1 or ground2), collider = 'box')
skybox_image = load_texture("textures/nightsky.png")
Sky(texture = skybox_image)

player = FirstPersonController(collision = FirstPersonController)
player.position = (0,0,-10)

tree_x = -120
tree_z = -120

class Tree(Entity):
    def __init__(self, tree_x, tree_z):
        super().__init__(position = (tree_x, 0, tree_z))
        stem = Entity(parent  = self, model = Cylinder(resolution=16), scale_y = 4, collision = Cylinder, color = color.hex("#81550e"))
        leaves = Entity(parent = self, model=Cone(resolution=16), color = color.hex("#1e5c31"), scale = (4, 6, 4), y = 2, collision = Cone)
        
class Zombie(Entity):
    def __init__(self):
        super().__init__()
        head = Entity(parent = self, model = 'cube', color = color.hex("#364625"), scale = (0.9, 1.005, 1.005), y = 2.5)
        body = Entity(parent = self, model = 'cube', color = color.hex("#25502e"), scale = (1.7, 1.2, 0.5), y = 1.5)
        foot1 = Entity(parent = self, model = 'cube', color = color.hex("#24355c"), scale_z = 0.5, scale_y = 2)
        
    def update(self):
        if distance_xz(self, player) > 2:
            self.look_at_xz(player)
            self.position += self.forward * 3 * time.dt
    
zombie = Zombie()
zombie.position = (0,0,0)    
    
while tree_x <= 120:
    tree_z = -120
    while tree_z <= 120:
        Tree(tree_x + random.randrange(-4, 5), tree_z)
        tree_z += random.randrange(12, 18)
    tree_x += random.randrange(12, 18)

def closewindow():
    on_click = exit()
    
def input(key):
    if key == 'escape':
        closewindow()

app.run()