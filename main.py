import pyxel
import random

class ElementGraphique():

    def __init__(self, pos_x: int, pos_y: int, size: tuple, col: int, direction: int) -> None:
        
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.dx = direction[0]
        self.dy = direction[1]

        self.size = size
        self.col = col

    def draw(self):

        pyxel.rect(self.pos_x,self.pos_y,self.size[0],self.size[1],self.col)

    def update(self):

        self.pos_x += self.dx
        self.pos_y += self.dy

    def test_collision_elg(self, target:'ElementGraphique'):

        if target.pos_x < self.pos_x+self.size[0] and target.pos_y < self.pos_y+self.size[1] and target.pos_x+target.size[0] > self.pos_x and target.pos_y+target.size[1] > self.pos_y:
            return True
        return False

    def touche_border(self):

        if self.pos_x < 0 or self.pos_x + self.size[0] > pyxel.width:
            return True
        if self.pos_y < 0 or self.pos_y + self.size[1] > pyxel.height:
            return True
        
        return False

class Missile(ElementGraphique):

    def __init__(self, pos_x: int, pos_y: int, direction: int) -> None:
        super().__init__(pos_x, pos_y, (1,2), 5, direction)

class Player(ElementGraphique):

    def __init__(self, pos_x: int, pos_y: int, size: tuple, col: int, direction: int, life: int) -> None:
        super().__init__(pos_x, pos_y, size, col, direction)

        self.life = life

        self.missiles: list['Missile'] = []

    def draw(self):
        super().draw()

        for missile in self.missiles:

            missile.draw()

    def update(self):

        if self.pos_x + self.dx >= 0 and self.pos_x + self.dx < pyxel.width - self.size[0]+1:
            self.pos_x += self.dx
        if self.pos_y + self.dy >= 0 and self.pos_y + self.dy < pyxel.height - self.size[1]+1:
            self.pos_y += self.dy

        for missile in self.missiles:

            missile.update()

    def explode(self):

        self.col = 8

    def spawn_missile(self, direction):

        self.missiles.append(Missile(self.pos_x+int(self.size[0]/2),self.pos_y,direction))

class Vaisseau(Player):
    
    def __init__(self, pos_x: int, pos_y: int) -> None:
        super().__init__(pos_x, pos_y, (5,5),8, (0,0), 100)

        self.cooldown = 7
        self.start = 0

    def update(self):
        super().update()

        self.test_input()

    def test_input(self):

        if pyxel.btnp(pyxel.KEY_SPACE):

            if pyxel.frame_count > self.cooldown + self.start:

                self.spawn_missile((0,-1))
 
                self.start = pyxel.frame_count

        if pyxel.btn(pyxel.KEY_RIGHT):

            self.dx = 1

        elif pyxel.btn(pyxel.KEY_LEFT):

            self.dx = -1

        else:
            self.dx = 0

class Ennemi(Player):

    def __init__(self, pos_x: int, pos_y: int, direction: tuple, life: int) -> None:
        super().__init__(pos_x, pos_y, (3,3),4,direction, life)

        self.cooldown = random.randint(40,200) 
        self.start = 0

    def update(self):
        super().update()

        if pyxel.frame_count > self.start + self.cooldown:

            self.spawn_missile((0,0.3))

            self.start = pyxel.frame_count + random.randint(0,200)

class App():

    def __init__(self) -> None:

        pyxel.init(50,50)
        
        self.score = 0
        self.vaisseau = Vaisseau(25,40)
        self.enemis :list[Ennemi] = []

        pyxel.run(self.update,self.draw)

    def update(self):

        self.element_update()

        self.test_wave()
        
        self.test_missile_enemi()
        self.test_missile_vaisseau()

    def draw(self):

        pyxel.cls(0)

        self.vaisseau.draw()

        for enemi in self.enemis:

            enemi.draw()

    def element_update(self):

        for enemi in self.enemis:

            enemi.update()

        self.vaisseau.update()

    def test_wave(self):

        if pyxel.frame_count % 550 == 0:

            self.spawn_wave()

    def spawn_wave(self):

        for i in range(5):
                self.spawn_enemi((i*10+random.randint(2,8),5),(0, random.randint(5,20) *10 ** -3 ))

    def spawn_enemi(self, pos: tuple, direction: tuple):

        self.enemis.append(Ennemi(pos[0],pos[1],direction,20))

    def test_missile_enemi(self):

        for enemi in self.enemis:

                for missile in enemi.missiles:

                    if self.vaisseau.test_collision_elg(missile):

                        self.vaisseau.explode()
                        self.vaisseau = None
                        enemi.missiles.remove(missile)

                    if missile.touche_border():
                        enemi.missiles.remove(missile)

    def test_missile_vaisseau(self):

        for enemi in self.enemis:

                for missile in self.vaisseau.missiles:

                    if enemi.test_collision_elg(missile):

                        enemi.explode()
                        self.enemis.remove(enemi)
                        self.vaisseau.missiles.remove(missile)

                    if missile.touche_border():
                        self.vaisseau.missiles.remove(missile)

App()