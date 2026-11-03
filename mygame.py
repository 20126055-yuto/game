from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math

app = Ursina()

# --------------------------------------------------
# 【重要】白い背景を完全に黒で埋める設定
# --------------------------------------------------
window.title = "CORRIDOR BREAKER 3D"
window.borderless = False
window.fullscreen = False
window.color = color.black     # 背景を完全な黒に
Sky(color=color.black)          # 空の空間も完全な黒に

# --------------------------------------------------
# ステージ設定（天井を追加＆壁を分厚くして白漏れを完全防止）
# --------------------------------------------------
CORRIDOR_WIDTH = 8
CORRIDOR_HEIGHT = 6
CORRIDOR_LENGTH = 110

# 1. 床（暗い黒鉄色）
floor = Entity(
    model='cube', unlit=True,
    color=color.rgb(20, 20, 22),
    scale=(CORRIDOR_WIDTH + 4, 1, CORRIDOR_LENGTH + 10),
    position=(0, -0.5, CORRIDOR_LENGTH / 2),
    collider='box'
)

# 2. 天井（追加：上が白く見えるのを防ぐ）
ceiling = Entity(
    model='cube', unlit=True,
    color=color.rgb(15, 15, 18),
    scale=(CORRIDOR_WIDTH + 4, 1, CORRIDOR_LENGTH + 10),
    position=(0, CORRIDOR_HEIGHT + 0.5, CORRIDOR_LENGTH / 2),
    collider='box'
)

# 3. 左右の壁（暗いグレー）
left_wall = Entity(
    model='cube', unlit=True,
    color=color.rgb(30, 30, 35),
    scale=(2, CORRIDOR_HEIGHT + 2, CORRIDOR_LENGTH + 10),
    position=(-CORRIDOR_WIDTH / 2 - 1, CORRIDOR_HEIGHT / 2, CORRIDOR_LENGTH / 2),
    collider='box'
)
right_wall = Entity(
    model='cube', unlit=True,
    color=color.rgb(30, 30, 35),
    scale=(2, CORRIDOR_HEIGHT + 2, CORRIDOR_LENGTH + 10),
    position=(CORRIDOR_WIDTH / 2 + 1, CORRIDOR_HEIGHT / 2, CORRIDOR_LENGTH / 2),
    collider='box'
)

# 4. スタート背後の壁
back_wall = Entity(
    model='cube', unlit=True,
    color=color.rgb(20, 20, 25),
    scale=(CORRIDOR_WIDTH + 4, CORRIDOR_HEIGHT + 2, 2),
    position=(0, CORRIDOR_HEIGHT / 2, -1),
    collider='box'
)

# ネオンライン（床のガイド線）
Entity(model='cube', unlit=True, color=color.cyan, scale=(0.08, 0.05, CORRIDOR_LENGTH), position=(-CORRIDOR_WIDTH/2 + 0.5, 0.01, CORRIDOR_LENGTH/2))
Entity(model='cube', unlit=True, color=color.cyan, scale=(0.08, 0.05, CORRIDOR_LENGTH), position=(CORRIDOR_WIDTH/2 - 0.5, 0.01, CORRIDOR_LENGTH/2))

# --------------------------------------------------
# ゴール & 迫る赤いデスウォール
# --------------------------------------------------
goal_gate = Entity(
    model='cube', unlit=True,
    color=color.rgba(0, 255, 120, 160),
    scale=(CORRIDOR_WIDTH, CORRIDOR_HEIGHT, 1),
    position=(0, CORRIDOR_HEIGHT / 2, CORRIDOR_LENGTH - 3)
)
Text(text='[ ESCAPE POD ]', position=(0, 0.15), origin=(0, 0), scale=2.5, color=color.green, parent=goal_gate)

WALL_SPEED = 1.45
death_wall = Entity(
    model='cube', unlit=True,
    color=color.rgba(255, 20, 20, 200),
    scale=(CORRIDOR_WIDTH, CORRIDOR_HEIGHT, 1),
    position=(0, CORRIDOR_HEIGHT / 2, -10)
)

# --------------------------------------------------
# プレイヤー & UI
# --------------------------------------------------
player = FirstPersonController(position=(0, 1, 2), speed=10, jump_height=1.4)
crosshair = Entity(parent=camera.ui, model='circle', scale=0.005, color=color.white)

timer = 0.0
best_time = 999.9

time_text = Text(text='TIME: 0.00s', position=(-0.85, 0.45), scale=2, color=color.white)
best_text = Text(text='BEST: --.--s', position=(0.60, 0.45), scale=1.5, color=color.light_gray)

MAX_AMMO = 6
ammo = MAX_AMMO
is_reloading = False
ammo_text = Text(text=f'AMMO: {ammo} / {MAX_AMMO}', position=(-0.85, -0.42), scale=2, color=color.yellow)

message_text = Text(text='', origin=(0, 0), scale=3.5, y=0.12)
sub_text = Text(text='', origin=(0, 0), scale=1.5, y=-0.05, color=color.light_gray)

game_state = 'PLAYING'

# --------------------------------------------------
# エフェクト生成
# --------------------------------------------------
def create_explosion_particles(pos):
    for _ in range(12):
        p = Entity(
            model='cube', unlit=True, color=color.orange, scale=0.15,
            position=pos, collider=None
        )
        velocity = Vec3(random.uniform(-4, 4), random.uniform(-2, 5), random.uniform(-4, 4))
        p.animate_position(p.position + velocity, duration=0.4, curve=curve.out_expo)
        p.animate_scale((0, 0, 0), duration=0.4)
        destroy(p, delay=0.4)

def create_bullet_impact(pos):
    impact = Entity(
        model='sphere', unlit=True, color=color.cyan, scale=0.08,
        position=pos, collider=None
    )
    impact.animate_scale((0, 0, 0), duration=0.3, delay=1.5)
    destroy(impact, delay=1.8)

# --------------------------------------------------
# 物理障害物（ハードル＆柱）
# --------------------------------------------------
obstacles = []

def create_obstacles():
    global obstacles
    for obs in obstacles: destroy(obs)
    obstacles.clear()

    # ハードル：黄色
    for z in [18, 38, 58, 78, 92]:
        hurdle = Entity(
            model='cube', unlit=True, color=color.yellow,
            scale=(CORRIDOR_WIDTH - 1, 0.9, 0.6),
            position=(0, 0.45, z),
            collider='box'
        )
        obstacles.append(hurdle)

    # 柱：パープル
    pillar_data = [
        (-2.2, 28), ( 2.2, 48), (-2.2, 68), ( 2.2, 88)
    ]
    for x, z in pillar_data:
        pillar = Entity(
            model='cube', unlit=True, color=color.magenta,
            scale=(3.5, CORRIDOR_HEIGHT, 1.2),
            position=(x, CORRIDOR_HEIGHT / 2, z),
            collider='box'
        )
        obstacles.append(pillar)

# --------------------------------------------------
# 動く的 ＆ バリア
# --------------------------------------------------
class TargetNode(Entity):
    def __init__(self, position, scale, barrier):
        super().__init__(
            model='sphere', unlit=True, color=color.orange,
            scale=scale, position=position, collider='sphere'
        )
        self.barrier = barrier
        self.move_speed = random.uniform(2.5, 4.5)
        self.direction = random.choice([-1, 1])

    def update(self):
        if game_state == 'PLAYING':
            self.x += self.direction * self.move_speed * time.dt
            if self.x > 3.0:
                self.x = 3.0
                self.direction = -1
            elif self.x < -3.0:
                self.x = -3.0
                self.direction = 1

targets = []
barriers = []

def spawn_checkpoints():
    global targets, barriers
    for t in targets: destroy(t)
    for b in barriers: destroy(b)
    targets.clear()
    barriers.clear()

    checkpoint_z = [12, 22, 32, 42, 52, 62, 72, 82, 95]
    for z in checkpoint_z:
        wall = Entity(
            model='cube', unlit=True,
            color=color.rgba(0, 160, 255, 120),
            scale=(CORRIDOR_WIDTH, CORRIDOR_HEIGHT, 0.4),
            position=(0, CORRIDOR_HEIGHT / 2, z),
            collider='box'
        )
        barriers.append(wall)

        rx = random.uniform(-2.5, 2.5)
        ry = random.uniform(1.2, 3.5)
        rz = z - random.uniform(1.5, 3.0)
        r_scale = random.uniform(0.65, 1.2)

        target = TargetNode(position=Vec3(rx, ry, rz), scale=r_scale, barrier=wall)
        targets.append(target)

create_obstacles()
spawn_checkpoints()

# --------------------------------------------------
# 銃の組み立て
# --------------------------------------------------
GUN_BASE_POS = Vec3(0.35, -0.3, 0.6)
GUN_BASE_ROT = Vec3(-2, -5, 0)

gun = Entity(parent=camera, position=GUN_BASE_POS, rotation=GUN_BASE_ROT)

Entity(parent=gun, model='cube', unlit=True, color=color.red, scale=(0.09, 0.1, 0.65), position=(0, 0.06, 0.1))
Entity(parent=gun, model='cube', unlit=True, color=color.black, scale=(0.08, 0.08, 0.55), position=(0, -0.02, 0.08))
Entity(parent=gun, model='cube', unlit=True, color=color.rgb(40, 40, 45), scale=(0.08, 0.28, 0.14), position=(0, -0.16, -0.05), rotation=(22, 0, 0))
Entity(parent=gun, model='cube', unlit=True, color=color.black, scale=(0.04, 0.04, 0.01), position=(0, 0.07, 0.43))
Entity(parent=gun, model='cube', unlit=True, color=color.yellow, scale=(0.015, 0.025, 0.02), position=(0, 0.12, 0.4))

muzzle_flash = Entity(parent=gun, model='sphere', unlit=True, color=color.yellow, scale=(0.18, 0.18, 0.22), position=(0, 0.07, 0.55), enabled=False)

# --------------------------------------------------
# リセット機能
# --------------------------------------------------
def reset_game():
    global timer, game_state, ammo, is_reloading
    timer = 0.0
    game_state = 'PLAYING'
    ammo = MAX_AMMO
    is_reloading = False
    ammo_text.text = f'AMMO: {ammo} / {MAX_AMMO}'
    ammo_text.color = color.yellow

    player.position = (0, 1, 2)
    player.rotation = (0, 0, 0)
    camera.rotation = (0, 0, 0)
    player.speed = 10
    death_wall.position = (0, CORRIDOR_HEIGHT / 2, -10)
    message_text.text = ''
    sub_text.text = ''

    create_obstacles()
    spawn_checkpoints()

# --------------------------------------------------
# 更新処理
# --------------------------------------------------
bob_timer = 0.0
pulse_timer = 0.0

def update():
    global timer, game_state, bob_timer, pulse_timer, best_time

    if game_state == 'PLAYING':
        timer += time.dt
        time_text.text = f'TIME: {timer:.2f}s'
        death_wall.z += WALL_SPEED * time.dt

        pulse_timer += time.dt * 8
        pulse = 1.0 + math.sin(pulse_timer) * 0.03
        death_wall.scale_x = CORRIDOR_WIDTH * pulse

        is_moving = held_keys['w'] or held_keys['s'] or held_keys['a'] or held_keys['d']
        if is_moving and not is_reloading and player.grounded:
            bob_timer += time.dt * 12
            gun.y = GUN_BASE_POS.y + math.sin(bob_timer) * 0.015
            gun.x = GUN_BASE_POS.x + math.cos(bob_timer * 0.5) * 0.01
        elif not is_reloading:
            gun.position = GUN_BASE_POS

        if player.z >= goal_gate.z:
            game_state = 'WIN'
            player.speed = 0

            if timer < best_time:
                best_time = timer
                best_text.text = f'BEST: {best_time:.2f}s'
                best_text.color = color.yellow
                message_text.text = f'NEW RECORD!!\n{timer:.2f}s'
                message_text.color = color.yellow
            else:
                message_text.text = f'CLEAR!!\n{timer:.2f}s'
                message_text.color = color.green

            sub_text.text = 'Press [ R ] to Play Again'

        elif death_wall.z >= player.z:
            game_state = 'LOSE'
            message_text.text = 'CAUGHT BY THE WALL...\nGAME OVER'
            message_text.color = color.red
            sub_text.text = 'Press [ R ] to Retry'
            player.speed = 0

# --------------------------------------------------
# 入力 ＆ 射撃 ＆ リロード
# --------------------------------------------------
def input(key):
    global is_reloading

    if game_state == 'PLAYING':
        if key == 'left mouse down':
            if ammo > 0 and not is_reloading:
                shoot()
            elif ammo == 0 and not is_reloading:
                reload()

        if key == 'r' and not is_reloading and ammo < MAX_AMMO:
            reload()

    elif game_state in ['WIN', 'LOSE']:
        if key == 'r':
            reset_game()

def shoot():
    global ammo
    ammo -= 1
    ammo_text.text = f'AMMO: {ammo} / {MAX_AMMO}'
    if ammo == 0:
        ammo_text.color = color.red

    muzzle_flash.enabled = True
    invoke(setattr, muzzle_flash, 'enabled', False, delay=0.04)
    gun.animate_position(GUN_BASE_POS + Vec3(0, 0.03, -0.12), duration=0.04)
    gun.animate_rotation(GUN_BASE_ROT + Vec3(-12, 0, 0), duration=0.04)
    invoke(gun.animate_position, GUN_BASE_POS, duration=0.1, delay=0.04)
    invoke(gun.animate_rotation, GUN_BASE_ROT, duration=0.1, delay=0.04)

    hit_info = raycast(camera.world_position, camera.forward, distance=100, ignore=(player, gun))
    
    if hit_info.hit:
        if isinstance(hit_info.entity, TargetNode):
            create_explosion_particles(hit_info.entity.world_position)
            destroy(hit_info.entity.barrier)
            destroy(hit_info.entity)
        elif hit_info.entity not in [death_wall, goal_gate]:
            create_bullet_impact(hit_info.point)

def reload():
    global is_reloading
    is_reloading = True
    ammo_text.text = 'RELOADING...'
    ammo_text.color = color.orange

    gun.animate_position(GUN_BASE_POS + Vec3(0, -0.4, 0), duration=0.3)
    gun.animate_rotation(GUN_BASE_ROT + Vec3(20, -10, 0), duration=0.3)
    invoke(finish_reload, delay=1.0)

def finish_reload():
    global ammo, is_reloading
    ammo = MAX_AMMO
    is_reloading = False
    ammo_text.text = f'AMMO: {ammo} / {MAX_AMMO}'
    ammo_text.color = color.yellow
    gun.animate_position(GUN_BASE_POS, duration=0.2)
    gun.animate_rotation(GUN_BASE_ROT, duration=0.2)

app.run()