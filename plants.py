import arcade
from arcade import load_texture

import animate
import bonuses
import time
from const import *


def lawn_x(x):
    right_x = 248 + CELL_WIDTH
    col = 1
    while right_x <= x:
        right_x += CELL_WIDTH
        col += 1
    right_x -= CELL_WIDTH/2
    return right_x, col

def lawn_y(y):
    right_y = 24 + CELL_HEIGHT
    row = 1
    while right_y <= y:
        right_y += CELL_HEIGHT
        row += 1
    right_y -= CELL_HEIGHT/2
    return right_y, row


class Plant(animate.Animate):
    def __init__(self, cost, health, window):
        super().__init__(scale = 0.15)
        self.cost = cost
        self.health = health
        self.col = 0
        self.row = 0
        self.window = window

    def update(self):
        if self.health <= 0:
            self.kill()

    def planting(self, center_x, center_y, row, col):
        self.set_position(center_x, center_y)
        self.col = col
        self.row = row
        for plant in self.window.plants:
            point_plant = arcade.get_sprites_at_point([center_x, center_y], self.window.plants)
            if point_plant:
                self.window.score += point_plant[0].cost
                point_plant[0].remove_from_sprite_lists()

                return center_x, center_y

class SunFlower(Plant):
    def __init__(self, window):
        super().__init__( 50, 80, window)
        self.append_t()
        self.spawn_time = time.time()

    def append_t(self):
        self.append_texture(arcade.load_texture("plants/sun1.png"))
        self.append_texture(arcade.load_texture("plants/sun2.png"))
        self.set_texture(0)

    def update(self):
        super().update()
        if time.time() - self.spawn_time >= 8:
            self.spawn_time = time.time()
            sun = bonuses.Sun(self.center_x, self.center_y)
            self.window.suns.append(sun)

class Nut(Plant):
    def __init__(self, window):
        super().__init__(50, 300, window)
        self.append_t()

    def append_t(self):
        self.append_texture(arcade.load_texture("plants/nut1.png"))
        self.append_texture(arcade.load_texture("plants/nut2.png"))
        self.append_texture(arcade.load_texture("plants/nut3.png"))
        self.set_texture(0)

class Pea(Plant):
    def __init__(self, window):
        super().__init__(100, 100, window)
        self.append_t()
        self.spawn_time = time.time()

    def append_t(self):
        self.append_texture(arcade.load_texture("plants/pea1.png"))
        self.append_texture(arcade.load_texture("plants/pea2.png"))
        self.append_texture(arcade.load_texture("plants/pea3.png"))
        self.set_texture(0)

    def update(self):
        super().update()
        if time.time() - self.spawn_time >= 3:
            self.spawn_time = time.time()
            bul = bonuses.Bul(self.center_x, self.center_y, self)
            self.window.buls.append(bul)


class Tree(Plant):
    def __init__(self, window):
        super().__init__( 175, 120, window)
        self.append_t()

    def append_t(self):
        self.append_texture(arcade.load_texture("plants/tree1.png"))
        self.append_texture(arcade.load_texture("plants/tree2.png"))
        self.append_texture(arcade.load_texture("plants/tree3.png"))
        self.set_texture(0)

    def update(self):
        super().update()
        hit_list = arcade.check_for_collision_with_list(self, self.window.buls)
        if len(hit_list) > 0:
            for bul in hit_list:
                bul.texture = load_texture("items/firebul.png")
                bul.attack = 30



