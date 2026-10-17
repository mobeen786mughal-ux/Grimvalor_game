from ursina import *
import random

app = Ursina()

window.title = 'Grimvalor - Full Game'
window.borderless = False

# === PLAYER STATS ===
player_hp = 100
max_hp = 100
coins = 0
score = 0

# === WORLD ===
Sky(color=color.rgb(10,10,30))
ground = Entity(model='plane', scale=(200,1,200), color=color.rgb(25,25,25), collider='box', texture='white_cube')

# Castle Platforms
platforms = []
for i in range(25):
    p = Entity(
        model='cube',
        color=color.rgb(70,50,30) if i%2==0 else color.dark_gray,
        scale=(Vec3(random.randint(4,8), 1, random.randint(4,8))),
        position=(random.randint(-40,40), random.randint(2,20), random.randint(-40,40)),
        collider='box'
    )
    platforms.append(p)

# Player
player = Entity(model='cube', color=color.azure, scale=(1,2,1), position=(0,15,0), collider='box')
sword = Entity(parent=player, model='cube', color=color.light_gray, scale=(0.2,1.2,0.3), position=(0.7,0,0.6), rotation=(0,0,90), enabled=False)

# Coins
coins_list = [Entity(model='sphere', color=color.gold, scale=0.6, position=(random.uniform(-35,35), random.uniform(3,18), random.uniform(-35,35)), collider='box') for _ in range(20)]

# Enemies
def make_enemy(pos, boss=False):
    e = Entity(model='cube', color=color.red if not boss else color.rgb(180,0,180), scale=(1,2,1) if not boss else (2.5,3.5,2.5), position=pos, collider='box')
    e.hp = 100 if not boss else 400
    e.boss = boss
    e.speed = 2.5 if not boss else 1.8
    return e

enemies = [make_enemy((15,2,10)), make_enemy((-20,5,-10)), make_enemy((25,8,-20)), make_enemy((-15,10,15))]
final_boss = make_enemy((0,2,45), boss=True)
enemies.append(final_boss)

# Physics
vy = 0
gravity = 32
jump = 14
speed = 7
can_double = True
dashing = False
attacking = False

# UI
hp_t = Text(text=f'HP: {player_hp}', pos=(-0.85,0.45), color=color.red, scale=1.5)
coin_t = Text(text='Coins: 0', pos=(-0.85,0.40), color=color.yellow, scale=1.5)
ctrl_t = Text(text='WASD Move | SPACE Double Jump | SHIFT Dash | F Attack', pos=(-0.75,-0.45), scale=0.9)

def update():
    global vy, can_double, player_hp, coins, dashing, attacking, score
    if player_hp <= 0:
        return

    # Move
    mx = held_keys['d'] - held_keys['a']
    mz = held_keys['w'] - held_keys['s']
    cur_speed = 14 if dashing else speed
    player.x += mx * cur_speed * time.dt
    player.z += mz * cur_speed * time.dt

    # Gravity
    hit = raycast(player.position+Vec3(0,0.5,0), (0,-1,0), 1.4, ignore=[player, sword]).hit
    if not hit:
        vy -= gravity * time.dt
    else:
        if vy < 0: vy = 0
        can_double = True
    player.y += vy * time.dt
    if player.y < -30: player_hp = 0

    # Camera
    camera.position = lerp(camera.position, player.position + Vec3(0,6,-12), time.dt*5)
    camera.look_at(player.position)

    # Enemies AI
    for e in enemies:
        if e.hp <= 0: continue
        d = distance(player, e)
        if d < 25 and d > 2:
            e.look_at(player)
            e.position += e.forward * e.speed * time.dt
        e.y -= 12*time.dt
        if e.y < 1: e.y = 1
        if d < 2.5 and random.random() < 0.015:
            player_hp -= 15 if not e.boss else 30
            hp_t.text = f'HP: {player_hp}'
            player.blink(color.red, 0.1)

    # Coins collect
    for c in coins_list[:]:
        if distance(player, c) < 1.6:
            coins += 1
            coin_t.text = f'Coins: {coins}'
            destroy(c)
            coins_list.remove(c)

    if final_boss.hp <= 0:
        Text(text='YOU WIN! BOSS DEFEATED!', origin=(0,0), scale=2, color=color.gold)

def input(key):
    global vy, can_double, dashing, attacking
    if key == 'space':
        if raycast(player.position+Vec3(0,0.5,0), (0,-1,0), 1.4, ignore=[player, sword]).hit:
            vy = jump
        elif can_double:
            vy = jump
            can_double = False
    if key == 'shift' and not dashing:
        dashing = True
        player.color = color.cyan
        invoke(lambda: (setattr(player, 'color', color.azure), setattr(globals(), 'dashing', False)), delay=0.35)
    if key in ('f','left mouse down') and not attacking:
        attacking = True
        sword.enabled = True
        sword.animate_rotation(Vec3(0,0,210), duration=0.12)
        for e in enemies:
            if distance(player, e) < 4 and e.hp > 0:
                e.hp -= 40
                e.blink(color.white, 0.1)
                e.position += Vec3(random.uniform(-1,1),0.5,random.uniform(-1,1))
                if e.hp <= 0:
                    e.color = color.black
                    e.collider = None
        invoke(reset_atk, delay=0.2)

def reset_atk():
    global attacking
    attacking = False
    sword.enabled = False
    sword.rotation_z = 90

app.run()
