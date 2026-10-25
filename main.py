from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

health = 100
health_text = Text(f"Health: {health}", position = (-0.85, 0.47), color = color.black, scale = 1.5)
lost_text = Text("You Lost!", origin = (0,0), color = color.red, enabled = False, scale = 3)

scene.fog_color = color.hex("#0b1020")
scene.fog_density = (2, 60)

ground1 = 'textures/ground.png'
ground2 = 'textures/ground2.png'

ground = Entity(model = 'plane', scale = 250, texture_scale = (250, 250), texture = (ground1 or ground2), collider = 'box')
skybox_image = load_texture("textures/nightsky.png")
Sky(texture = skybox_image)

player = FirstPersonController(collider = 'box')
player.position = (0,0,-30)

tree_x = -120
tree_z = -120

class Tree(Entity):
    def __init__(self, tree_x, tree_z):
        super().__init__(position = (tree_x, 0, tree_z))
        stem = Entity(parent  = self, model = Cylinder(resolution=16), scale_y = 4, collider = 'box', color = color.hex("#81550e"))
        leaves = Entity(parent = self, model=Cone(resolution=16), color = color.hex("#1e5c31"), scale = (4, 6, 4), y = 2, collider = 'box')
        
class Zombie(Entity):
    def __init__(self):
        super().__init__()
        head = Entity(parent = self, model = 'cube', color = color.hex("#364625"), scale = (0.9, 1.005, 1.005), y = 2.5, collider = 'box')
        body = Entity(parent = self, model = 'cube', color = color.hex("#25502e"), scale = (1.7, 1.2, 0.5), y = 1.5, collider = 'box')
        foot1 = Entity(parent = self, model = 'cube', color = color.hex("#24355c"), scale_z = 0.5, scale_y = 2, collider = 'box')
        self.attack_timer = 0
        
    def update(self):
        global health
        dist = distance_xz(self, player)
        if dist > 1:
            self.look_at_xz(player)
            self.position += self.forward * 3 * time.dt
        if dist < 1.5:
            self.attack_timer += time.dt
            if self.attack_timer >= 2:
                self.attack_timer = 0
                health -= 10
                health_text.text = f"Health: {health}"
                print("-10 Health")
                if health <= 0:
                    lost_text.enabled = True
    
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