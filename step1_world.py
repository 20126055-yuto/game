from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
import random

# Step 1 - add 1
# 地面
ground = Entity(model='plane', scale=60, texture='grass', texture_scale=(60, 60),
                color=color.blue, collider='box')

# Step 1 - add 2
# プレイヤー　(マウスで見回す、WASDで移動、Spaceでジャンプ
player = FirstPersonController()

# Step 2 - add 2
# 敵
enemies = []
for i in range(8):
    enemy = Entity(model='diamond', color=color.yellow, scale=0.5, collider='box',
                   position=(random.randint(-20, 20),0.75, random.randint(10,25)))
    enemies.append(enemy)
# Step 3 - add 3
# スコア
score = 0
score_text = Text(text='score: 0', position=(-0.85, 0.45), scale=2)

# Step 3 -add 2
#撃つ(左クリック)
def input(key):
    global score
    if key == 'left mouse down':
        if mouse.hovered_entity in enemies:
            enemy = mouse.hovered_entity
            enemies.remove(enemy)
            destroy(enemy)
            score += 1
            score_text.text = 'Score: ' + str(score)

# Step 4 -add 1
def update():
    for enemy in enemies:
        enemy.look_at_2d(player.position,'y')
        enemy.position += enemy.forward * time.dt * 3

# Step 1 -add 3
#空
Sky()
app.run()