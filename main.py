import time
import zomb
import arcade
import random
import plants
from const import *



class MainGame(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Plant vs Zombies")
        # Textures
        self.bg = arcade.load_texture("textures/background.jpg")
        self.menu = arcade.load_texture("textures/menu_vertical.png")
        self.screensaver = arcade.load_texture("textures/screensaver.jpg")
        self.logo = arcade.load_texture("textures/logo.png")
        self.end = arcade.load_texture("textures/end.png")
        self.game = "screensaver"
        # Sprites
        self.plants = arcade.SpriteList()
        self.buls = arcade.SpriteList()
        self.firebuls = arcade.SpriteList()
        self.suns = arcade.SpriteList()
        self.zombies = arcade.SpriteList()
        # Vars
        self.seed = None
        self.score = 99999
        self.r_time = 0
        # Functions
        self.setup_zombie()

    def setup_zombie(self):
        for i in range(1, 1000):
            zombie = None
            choice = random.randint(1, 3)
            if choice == 1:
                zombie = zomb.ZombieOrd()
            if choice == 2:
                zombie = zomb.ZombieBuck()
            if choice == 3:
                zombie = zomb.ZombieCone()
            zombie.center_x = WINDOW_WIDTH + i * random.randint(1400 + 10 * i, 1500 + 10 * i)
            self.zombies.append(zombie)

    def on_draw(self):
        self.clear()
        if self.game == "screensaver":
            arcade.draw_texture_rectangle(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT, self.screensaver)
        if self.game == "game":
            arcade.draw_texture_rectangle(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, WINDOW_WIDTH, WINDOW_HEIGHT, self.bg)
            self.plants.draw()
            self.buls.draw()
            self.firebuls.draw()
            self.suns.draw()
            self.zombies.draw()
            arcade.draw_texture_rectangle(WINDOW_WIDTH/12, WINDOW_HEIGHT/2, WINDOW_WIDTH/6, WINDOW_HEIGHT, self.menu)
            arcade.draw_text(f"Score:{self.score}", 50, WINDOW_HEIGHT - 100, (0, 0, 0), 16)
            if self.seed is not None:
                self.seed.draw()
        if self.game == "over":
            arcade.draw_texture_rectangle(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT, self.end)

    def update(self, delta_time: float):
        self.plants.update()
        self.plants.update_animation(delta_time)
        self.buls.update()
        self.firebuls.update()
        self.suns.update()
        self.zombies.update()
        self.zombies.update_animation(delta_time)


        for zombie in self.zombies:
            hits_bul = arcade.check_for_collision_with_list(zombie, self.buls)
            hits_firebul = arcade.check_for_collision_with_list(zombie, self.firebuls)
            stan_per_plant = arcade.check_for_collision_with_list(zombie, self.plants)
            if zombie.right <= 0:
                self.game = "over"
            for bul in hits_bul:
                zombie.health -= bul.attack
                bul.remove_from_sprite_lists()
            for firebul in hits_firebul:
                zombie.health -= firebul.attack
                firebul.remove_from_sprite_lists()
            for plant in stan_per_plant:
                zombie.change_x = 0
                if time.time() - self.r_time >= 1.5:
                    plant.health -= 20
                    print(plant.health)
                    self.r_time = time.time()
                    if plant.health <= 0 or plant.health == 0:
                        self.plants.remove(plant)
                        zombie.change_x = -1



    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE and self.game == "screensaver":
            self.game = "game"

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.game == "game":
            if 20 <= x <= 150:
                if 375 <= y <= 480 and self.score >= 50:
                    self.seed = plants.SunFlower(self)
                    self.score -= 50
                if 260 <= y <= 370 and self.score >= 100:
                    self.seed = plants.Pea(self)
                    self.score -= 100
                if 145 <= y <= 250 and self.score >= 50:
                    self.seed = plants.Nut(self)
                    self.score -= 50
                if 30 <= y <= 135 and self.score >= 175:
                    self.seed = plants.Tree(self)
                    self.score -= 175

            if self.seed is not None:
                self.seed.center_x = x
                self.seed.center_y = y
                self.seed.alpha = 150

            for sun in self.suns:
                suns_clicked = arcade.get_sprites_at_point((x, y), self.suns)
                if suns_clicked is not None:
                    sun.kill()
                    self.score += 25

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
         if self.seed is not None:
            self.seed.center_x = x
            self.seed.center_y = y

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if 248 <= x <= 950 and 24 <= y <= 524 and self.seed is not None:
            center_x, col = plants.lawn_x(x)
            center_y, row = plants.lawn_y(y)
            self.seed.planting(center_x, center_y, row, col)
            self.seed.alpha = 255
            self.plants.append(self.seed)
            self.seed = None

    

window = MainGame()
window.run()