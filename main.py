import pyxel
import random
from sprite import *

class Missile(AnimateElementGraphique):

    def __init__(self, pos_x: int, pos_y: int, direction: tuple, color: str = "red") -> None:
        
        if color == "red":
            pos_image_liste = {"blow_up":[(18,50),(18,58),(18,66)],"blow_max":[(18,66)]}
        elif color == "green":
            pos_image_liste = {"blow_up":[(10,50),(10,58),(10,66)],"blow_max":[(10,66)]}

        super().__init__(pos_x, pos_y, (4,4), pos_image_liste, "blow_up", 10, direction, 0, 0)

        self.one_anim("blow_up","blow_max")
        

class Vaisseau(AnimateElementGraphique):

    def __init__(self, pos_x: int, pos_y: int, size: tuple, pos_image_liste: dict[list[tuple]], default_state: str, anim_speed: int, direction: tuple, transparent_color: int, life: int, image_number: int = 0) -> None:
        super().__init__(pos_x, pos_y, size, pos_image_liste, default_state, anim_speed, direction, transparent_color, image_number)

        self.life = life

        self.is_alive = True 

        self.missiles: list['Missile'] = []

    def draw(self):
        
        super().draw()

        for missile in self.missiles:

            missile.draw()

    def update(self):

        super().update()

        for missile in self.missiles:

            missile.update()

    def takes_damage(self, damage):

        self.life -= damage

        if self.life <= 0 :

            self.explode()

    def explode(self):

        self.col = 8
        self.anim_speed = 2
        self.one_anim("explode","explode",self.destroy)

    def destroy(self):
        self.is_alive = False

    def spawn_missile(self, direction, color):

        self.missiles.append(Missile(self.pos_x+int(self.size[0]/2),self.pos_y,direction,color))

class Player(Vaisseau):
    
    def __init__(self, pos_x: int, pos_y: int) -> None:

        super().__init__(pos_x, pos_y, (8,8), {"idle":[(72,8)],"walk":[(72,8),(72,16)],"explode":[(56,0),(48,0),(40,0)]}, "walk", 10, (0,0), 0, 3, 0)

        self.cooldown = 7
        self.start = 0
        self.damage = 1

    def update(self):
        super().update()

        self.test_input()

    def test_input(self):

        if pyxel.btnp(pyxel.KEY_SPACE):

            if pyxel.frame_count > self.cooldown + self.start:

                self.spawn_missile((0,-2),"green")
 
                self.start = pyxel.frame_count

        if pyxel.btn(pyxel.KEY_RIGHT):

            self.dx = 1

        elif pyxel.btn(pyxel.KEY_LEFT):

            self.dx = -1

        else:
            self.dx = 0

class Ennemi(Vaisseau):

    def __init__(self, pos_x: int, pos_y: int, direction: tuple, type: str = "green") -> None:

        if type == "destoyer":
            score = 1
            pos_image = {"idle":[(56,8)],"walk":[(56,8),(56,16)],"explode":[(56,0),(48,0),(40,0)]}
        elif type == "red":
            score = 3
            pos_image = {"idle":[(40,8)],"walk":[(40,8),(40,16)],"explode":[(56,0),(48,0),(40,0)]}
        elif type == "green":
            score = 2
            pos_image = {"idle":[(48,8)],"walk":[(48,8),(48,16)],"explode":[(56,0),(48,0),(40,0)]}

        super().__init__(pos_x, pos_y, (8,8), pos_image, "walk", 10, direction, 0, 1, 0)

        self.cooldown = random.randint(40,200)
        self.start = pyxel.frame_count + random.randint(0,50)

        self.score = score

    def apply_direction(self):

        self.pos_x += self.dx

        if not self.pos_x + self.dx < pyxel.width - self.size[0]+1:
            self.dx = -0.1
            self.pos_y += 10
        elif not self.pos_x + self.dx >= 0:
            self.dx = 0.1
            
        if self.pos_y + self.dy >= 0 and self.pos_y + self.dy < pyxel.height - self.size[1]+1:
            self.pos_y += self.dy

        else:
            self.explode()

    def update(self):
        super().update()

        if pyxel.frame_count > self.start + self.cooldown:

            self.spawn_missile((0,1.5),"red")

            self.start = pyxel.frame_count + random.randint(0,50)

class App():

    def __init__(self) -> None:

        pyxel.init(150,150)
        
        self.score = 0
        self.vaisseau = Player(50, pyxel.height - 25)
        self.enemis :list[Ennemi] = []

        pyxel.load("2.pyxres")
        pyxel.run(self.update,self.draw)

    def update(self):

        if self.vaisseau.is_alive:

            self.update_game_scene()
        else:
            self.update_game_over_scene()

    def draw(self):

        if self.vaisseau.is_alive:

            self.draw_game_scene()
        else:
            self.draw_game_over_scene()
    
    def draw_game_over_scene(self):

        pyxel.cls(8)

    def draw_game_scene(self):

        pyxel.cls(0)

        self.vaisseau.draw()

        for enemi in self.enemis:

            enemi.draw()

        self.draw_life()

        pyxel.text(50, pyxel.height-10,f"score: {self.score}", 7)

    def update_game_over_scene(self):

        pyxel.mouse(True)

    def update_game_scene(self):

        self.test_destroy_space_ship()

        pyxel.mouse(False)

        self.element_update()

        self.test_wave()
        
        self.test_missile_enemi()
        self.test_missile_vaisseau()

    def draw_life(self):

        for i in range(self.vaisseau.life):

            pyxel.blt(2+i*10, pyxel.height-10, 0, 32, 65, 8, 7, 0)

    def element_update(self):

        for enemi in self.enemis:

            enemi.update()

        self.vaisseau.update()

    def test_wave(self):

        if pyxel.frame_count % 550 == 0:

            self.spawn_wave()

    def spawn_wave(self):

        for i in range(5):
                self.spawn_enemi((i*30+random.randint(2,8),5),(0.1, random.randint(20,40) *10 ** -3 ))

    def spawn_enemi(self, pos: tuple, direction: tuple):

        self.enemis.append(Ennemi(pos[0],pos[1],direction))

    def test_missile_enemi(self):

        for enemi in self.enemis:

                for missile in enemi.missiles:

                    if self.vaisseau.test_collision_elg(missile):

                        self.vaisseau.takes_damage(1)
                        enemi.missiles.remove(missile)

                    if missile.touche_border():
                        enemi.missiles.remove(missile)

    def test_missile_vaisseau(self):

        for enemi in self.enemis:

                for missile in self.vaisseau.missiles:

                    if enemi.test_collision_elg(missile):

                        enemi.takes_damage(self.vaisseau.damage)             
                        self.vaisseau.missiles.remove(missile)

                    if missile.touche_border():
                        self.vaisseau.missiles.remove(missile)

    def test_destroy_space_ship(self):

        for space_ship in self.enemis:

            if space_ship.is_alive == False:

                self.enemis.remove(space_ship)

                self.score += space_ship.score
App()