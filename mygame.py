from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# ステージ設定
CORRIDOR_WIDTH = 8
CORRIDOR_HEIGHT = 5
CORRIDOR_LENGTH = 100

floor = Entity(
    model='cube', color=color.dark_gray,
    scale=(CORRIDOR_WIDTH, 1, CORRIDOR_LENGTH),
    position=(0, -0.5, CORRIDOR_LENGTH / 2),
    collider='box'
)
left_wall = Entity(
    model='cube', color=color.gray,
    scale=(1, CORRIDOR_HEIGHT, CORRIDOR_LENGTH),
    position=(-CORRIDOR_WIDTH / 2, CORRIDOR_HEIGHT / 2, CORRIDOR_LENGTH / 2),
    collider='box'
)
right_wall = Entity(
    model='cube', color=color.gray,
    scale=(1, CORRIDOR_HEIGHT, CORRIDOR_LENGTH),
    position=(CORRIDOR_WIDTH / 2, CORRIDOR_HEIGHT / 2, CORRIDOR_LENGTH / 2),
    collider='box'
)
back_wall = Entity(
    model='cube', color=color.gray,
    scale=(CORRIDOR_WIDTH, CORRIDOR_HEIGHT, 1),
    position=(0, CORRIDOR_HEIGHT / 2, -0.5),
    collider='box'
)

# プレイヤー
player = FirstPersonController(position=(0, 1, 2), speed=10)
crosshair = Entity(parent=camera.ui, model='circle', scale=0.006, color=color.white)

# 【追加】右上のタイマー表示 (UI)
timer = 0.0
time_text = Text(
    text='TIME: 0.0',
    position=(-0.8, 0.45),  # 画面の右上（X: 0.65, Y: 0.45）
    scale=2,
    color=color.white
)

# 銃の組み立て
GUN_BASE_POS = Vec3(0.35, -0.3, 0.6)
GUN_BASE_ROT = Vec3(-2, -5, 0)

gun = Entity(parent=camera, position=GUN_BASE_POS, rotation=GUN_BASE_ROT)
gun_slide = Entity(parent=gun, model='cube', color=color.rgb(50, 50, 55), scale=(0.09, 0.1, 0.65), position=(0, 0.06, 0.1))
gun_frame = Entity(parent=gun, model='cube', color=color.rgb(30, 30, 32), scale=(0.08, 0.08, 0.55), position=(0, -0.02, 0.08))
gun_grip = Entity(parent=gun, model='cube', color=color.rgb(20, 20, 22), scale=(0.08, 0.28, 0.14), position=(0, -0.16, -0.05), rotation=(22, 0, 0))
gun_barrel_hole = Entity(parent=gun, model='cube', color=color.black, scale=(0.04, 0.04, 0.01), position=(0, 0.07, 0.43))
front_sight = Entity(parent=gun, model='cube', color=color.white, scale=(0.015, 0.025, 0.02), position=(0, 0.12, 0.4))
muzzle_flash = Entity(parent=gun, model='sphere', color=color.yellow, scale=(0.18, 0.18, 0.22), position=(0, 0.07, 0.55), enabled=False)

# 毎フレーム実行される処理（タイマーの更新）
def update():
    global timer
    timer += time.dt                    # 経過時間を足していく
    time_text.text = f'TIME: {timer:.1f}'  # 小数点第1位まで文字として表示

# 射撃処理
def input(key):
    if key == 'left mouse down':
        shoot()

def shoot():
    muzzle_flash.enabled = True
    invoke(setattr, muzzle_flash, 'enabled', False, delay=0.04)
    gun.animate_position(GUN_BASE_POS + Vec3(0, 0.03, -0.12), duration=0.04)
    gun.animate_rotation(GUN_BASE_ROT + Vec3(-12, 0, 0), duration=0.04)
    invoke(gun.animate_position, GUN_BASE_POS, duration=0.1, delay=0.04)
    invoke(gun.animate_rotation, GUN_BASE_ROT, duration=0.1, delay=0.04)

window.color = color.black
DirectionalLight(y=2, z=3, shadows=False)

app.run()