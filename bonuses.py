import arcade
import plants
from const import *




class Sun(arcade.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__("items/sun.png", 0.2)
        self.center_x = center_x
        self.center_y = center_y - 10

    def update(self):
        self.angle += 1

class Firebul(arcade.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__("items/firebul.png", 0.2)
        self.attack = 30
        self.change_x = 3
        self.center_x = center_x
        self.center_y = center_y


class Bul(arcade.Sprite):
    def __init__(self, center_x, center_y, window):
        super().__init__("items/bul.png", 0.2)
        self.attack = 15
        self.change_x = 3
        self.center_x = center_x
        self.center_y = center_y
        self.window = window

    def update(self):
        self.center_x += self.change_x
        if self.center_x >= WINDOW_WIDTH:
            self.kill()
        self.firing()

    def firing(self):
        if arcade.check_for_collision(self, plants.Tree(self)):
            for firebul in self.window.firebuls:
                firebul.center_x = self.center_x
                firebul.center_y = self.center_y
                self.remove_from_sprite_lists()
                self.window.firebuls.append(firebul)