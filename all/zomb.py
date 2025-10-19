import random
import arcade
import animate
from const import *


class Zombie(animate.Animate):
    def __init__(self, image, health):
        super().__init__(image, 0.7)
        self.health = health
        self.change_x = -1
        self.center_y, self.row = self.spawn_y()


    def update(self):
        self.center_x += self.change_x
        if self.health <= 0:
            self.kill()

    def spawn_y(self):
        rand_y = random.randint(24, 524)
        right_y = 24 + CELL_HEIGHT
        row = 1
        while right_y <= rand_y:
            right_y += CELL_HEIGHT
            row += 1
        right_y -= CELL_HEIGHT / 2
        return right_y, row

class ZombieOrd(Zombie):
    def __init__(self):
        super().__init__("zombies/OrdinaryZombie/Zombie_0.png",100)
        self.append_t()

    def append_t(self):
        for i in range(21):
            self.append_texture(arcade.load_texture(f"zombies/OrdinaryZombie/Zombie_{i}.png"))
        self.set_texture(0)

class ZombieCone(Zombie):
    def __init__(self):
        super().__init__("zombies/ConeheadZombie/ConeheadZombie_0.png", 150)
        self.append_t()

    def append_t(self):
        for i in range(20):
            self.append_texture(arcade.load_texture(f"zombies/ConeheadZombie/ConeheadZombie_{i}.png"))
        self.set_texture(0)

class ZombieBuck(Zombie):
    def __init__(self):
        super().__init__("zombies/BucketheadZombie/BucketheadZombie_0.png", 200)
        self.append_t()

    def append_t(self):
        for i in range(14):
            self.append_texture(arcade.load_texture(f"zombies/BucketheadZombie/BucketheadZombie_{i}.png"))
        self.set_texture(0)