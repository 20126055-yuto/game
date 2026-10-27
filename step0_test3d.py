from ursina import *

app = Ursina()

cube = Entity(model='cube', color=color.red)

def update():
    cube.rotation_y += 1

app.run()