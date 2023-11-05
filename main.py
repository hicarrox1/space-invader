import pyxel
import random
from sprite import *

"""
jeux space invader
-touche espace pour tirer
-fleche de gauche et de droite pour bouger de gauche a droite 
"""

class Missile(AnimateElementGraphique):
    # classe des missiles

    def __init__(self, pos_x: int, pos_y: int, direction: tuple, color: str = "red") -> None:
        
        # en fonction de la couleur en parametre nous changont ces animations
        if color == "red":
            pos_image_liste = {"blow_up":[(18,50),(18,58),(18,66)],"blow_max":[(18,66)]}
        elif color == "green":
            pos_image_liste = {"blow_up":[(10,50),(10,58),(10,66)],"blow_max":[(10,66)]}

        super().__init__(pos_x, pos_y, (4,4), pos_image_liste, "blow_up", 10, direction, 0, 0)

        # lance l'animation du missile qui augmente pour finir sur le missile max
        self.one_anim("blow_up","blow_max")
        

class Vaisseau(AnimateElementGraphique):
    # classe de tous ce qui est un vaisseau

    def __init__(self, pos_x: int, pos_y: int, size: tuple, pos_image_liste: dict[list[tuple]], default_state: str, anim_speed: int, direction: tuple, transparent_color: int, life: int, image_number: int = 0) -> None:
        super().__init__(pos_x, pos_y, size, pos_image_liste, default_state, anim_speed, direction, transparent_color, image_number)

        # set les paramtre de base d'un vaisseau

        # sa vie
        self.life = life

        # si il est toujour en vie
        self.is_alive = True 

        # sa liste de missiles
        self.missiles: list['Missile'] = []

    def draw(self):

        # lorsque nous l'affichons
        super().draw()

        # nous affichons aussi ces missiles
        for missile in self.missiles:

            missile.draw()

    def update(self):

        # lorsque nous l'updaton
        super().update()

        # nous updaton aussi ces missiles
        for missile in self.missiles:

            missile.update()

    def takes_damage(self, damage):
        """fonction qui reduit la vie par rapport au degat en parametre"""

        # reduit la vie des degat causer
        self.life -= damage

        # si sa vie est inferieur en zero fais exploser le vaisseau
        if self.life <= 0 :

            self.explode()

    def explode(self):
        """joue l'animation d'explosion"""

        # nous mettons la vitesse de l'animation moins rapide et nous jouon l'animation d'explosion qui apellera la fonction destroy a la fin de l'animation
        self.anim_speed = 2
        self.one_anim("explode","explode",self.destroy)

    def destroy(self):
        """detruit le vaisseau"""
        # met sa vie a faux
        self.is_alive = False

    def spawn_missile(self, direction, color):
        """fais spawn un missile et l'ajoute dans sa liste de missile"""

        self.missiles.append(Missile(self.pos_x+int(self.size[0]/2),self.pos_y,direction,color))

class Player(Vaisseau):
    # classe du player
    
    def __init__(self, pos_x: int, pos_y: int) -> None:

        super().__init__(pos_x, pos_y, (8,8), {"idle":[(72,8)],"walk":[(72,8),(72,16)],"explode":[(56,0),(48,0),(40,0)]}, "walk", 10, (0,0), 0, 3, 0)

        # set des variable pour un cooldown entre chaque missile
        self.cooldown = 7
        self.start = 0
        # set les damage du vaiseau a 1
        self.damage = 1

    def update(self):
        super().update()

        # test les input qui vont interagir sur le player
        self.test_input()

    def test_input(self):
        """test les input qui vont interagir sur le player"""

        # si nous apuyons sur espace nous tirons
        if pyxel.btnp(pyxel.KEY_SPACE):
            
            # gere le cooldown
            if pyxel.frame_count > self.cooldown + self.start:

                self.spawn_missile((0,-2),"green") # fais spawn le missile
 
                self.start = pyxel.frame_count

        # si nous apuyons sur la fleche de droite nous changer la direction x pour aller a droite
        if pyxel.btn(pyxel.KEY_RIGHT):

            self.dx = 1

        # si nous apuyons sur la fleche de gauche nous changer la direction x pour aller a gauche
        elif pyxel.btn(pyxel.KEY_LEFT):

            self.dx = -1

        else:
            # sinon nous allons nul part
            self.dx = 0

class Ennemi(Vaisseau):

    def __init__(self, pos_x: int, pos_y: int, direction: tuple, type: str = "green") -> None:
        
        # en fonction du type de l'enemi en parametre nous changont ces animations sont score et ces damages
        if type == "destoyer":
            score = 1
            damage = 1
            pos_image = {"idle":[(56,8)],"walk":[(56,8),(56,16)],"explode":[(56,0),(48,0),(40,0)]}
        elif type == "red":
            score = 3
            damage = 2
            pos_image = {"idle":[(40,8)],"walk":[(40,8),(40,16)],"explode":[(56,0),(48,0),(40,0)]}
        elif type == "green":
            score = 2
            damage = 1
            pos_image = {"idle":[(48,8)],"walk":[(48,8),(48,16)],"explode":[(56,0),(48,0),(40,0)]}

        super().__init__(pos_x, pos_y, (8,8), pos_image, "walk", 10, direction, 0, 1, 0)

        # set des variable pour un cooldown entre chaque missile qui est aleatoire
        self.cooldown = random.randint(40,200)
        self.start = pyxel.frame_count + random.randint(0,50)

        # set le score et les damage
        self.score = score
        self.damage = damage

    def apply_direction(self):

        # change la fonction qui fait bouger l'element graphique pour detecter si nous arrions sur le bord

        self.pos_x += self.dx

        # si nous arrions sur le bord 
        if not self.pos_x + self.dx < pyxel.width - self.size[0]+1:
            self.dx = -0.1
            self.pos_y += 10
            # l'enemi change de direction x et descend vers le bas
        elif not self.pos_x + self.dx >= 0:
            self.pos_y += 10
            self.dx = 0.1
            # l'enemi change de direction x et descend vers le bas
            
        if self.pos_y + self.dy >= 0 and self.pos_y + self.dy < pyxel.height - self.size[1]+1:
            self.pos_y += self.dy
        # si nous touchont pas les bordure nous descendont

        else:
            self.explode()
            # sinon l'enemi meure

    def update(self):
        super().update()

        # si le cooldown et passer nous faisons spawn un missile
        if pyxel.frame_count > self.start + self.cooldown:

            self.spawn_missile((0,1.5),"red")

            # et change le temps de quand le missile va etre tirer de maniere aleatoire
            self.start = pyxel.frame_count + random.randint(0,50)

class App():

    def __init__(self) -> None:

        pyxel.init(150,150)

        # set de toute les variable utile pour le jeux 
        
        #le score
        self.score = 0
        self.high_score = 0

        # les elements graphique
        self.vaisseau = Player(50, pyxel.height - 25)
        self.enemis :list[Ennemi] = []

        pyxel.load("2.pyxres")
        pyxel.run(self.update,self.draw)

    def update(self):
        
        #si nous avons pas perdu nous updatons la scene de game over sinon la scene de jeux
        if self.vaisseau.is_alive:

            self.update_game_scene()
        else:
            self.update_game_over_scene()

    def draw(self):

        #si nous avons pas perdu nous afichons la scene de game over sinon la scene de jeux
        if self.vaisseau.is_alive:

            self.draw_game_scene()
        else:
            self.draw_game_over_scene()
    
    def draw_game_over_scene(self):
        """affiche la scene de mort"""

        # met l'ecran a zero en rouge
        pyxel.cls(8)

        # affiche les texte de game over
        pyxel.text(20,20,"game over", 7)
        pyxel.text(20,60,"press space to restart", 7)

        # affiche le texte qui donne le score actuelle et le meilleur
        pyxel.text(20,100,f"last score: {self.score} high score: {self.high_score}", 7)

    def draw_game_scene(self):
        """affiche la scene de jeux"""

        # met l'ecran a zero en noir
        pyxel.cls(0)

        # affiche le vaisseau
        self.vaisseau.draw()

        # affiche les enemis
        for enemi in self.enemis:

            enemi.draw()

        # affiche le nombre de coeur
        self.draw_life()

        # affiche le score actuelle
        pyxel.text(50, pyxel.height-10,f"score: {self.score}", 7)

    def draw_life(self):
        """affiche le nombre de coeur"""

        for i in range(self.vaisseau.life): # le nombre de fois qu'il y a de coeur nous en affichons un de plus

            pyxel.blt(2+i*10, pyxel.height-10, 0, 32, 65, 8, 7, 0)

    def update_game_over_scene(self):
        """update la scene de game over"""

        # si nous avons perdu nous metton a jour le high score
        self.set_high_score()
        # et testons si nous appuyons sur la touche de restart
        self.test_restart()

    def set_high_score(self):
        """met a jour le high score"""

        if self.score >= self.high_score:

            self.high_score = self.score

    def test_restart(self):
        """teste si nous appuyons sur la touche de restart et restart en fonction"""

        if pyxel.btn(pyxel.KEY_SPACE):

            self.restart()

    def restart(self):
        "restart le jeux"

        # remet les variable par default
        self.vaisseau = Player(50, pyxel.height - 25)
        self.score = 0
        self.enemis = []

    def update_game_scene(self):
        """update la scene de jeux"""

        self.test_destroy_space_ship()

        # update tout les element
        self.element_update()

        # test si il faut faire spawn une nouvelle vague d'ennemis
        self.test_wave()
        
        # teste pour chaque missile si il touche  
        self.test_missile_enemi() # pour les missiles enemis
        self.test_missile_vaisseau() # pour les missiles du vaisseau

    def test_destroy_space_ship(self):
        """suprime les element mort"""

        for space_ship in self.enemis:

            if space_ship.is_alive == False:
                
                #si l'element et mort on le suprime de la liste des enemis et rajouton au score le score de l'enemis
                self.enemis.remove(space_ship)

                self.score += space_ship.score

    def element_update(self):
        """update tout les element"""

        # update les enemis
        for enemi in self.enemis:

            enemi.update()

        # update le vaisseau
        self.vaisseau.update()

    def test_wave(self):
        """test si il faut faire spawn une nouvelle vague d'ennemis"""

        # tous les 550 frame
        if pyxel.frame_count % 550 == 0:

            self.spawn_wave()

    def spawn_wave(self):
        """spawn une nouvelle vague d'ennemis"""

        # fait spawn 5 enemis avec chacun une direction aleatoire
        for i in range(5):
                self.spawn_enemi((i*30+random.randint(2,8),5),(0.1, random.randint(20,40) *10 ** -3 ))

    def spawn_enemi(self, pos: tuple, direction: tuple):

        # choisi aleatoirement le type de l'enemi
        rand = random.randint(1,10)

        if rand <= 5: 
            type_enemi = "destoyer" # le plus fréquemment
        elif rand <= 8:
            type_enemi = "green"
        else:
            type_enemi = "red" # le plus rare

        self.enemis.append(Ennemi(pos[0],pos[1],direction,type_enemi)) # creer un nouvel enemi et l'ajoute dans la liste des enemis

    def test_missile_enemi(self):
        """teste pour chaque missile de l'enemi si il touche le player"""

        for enemi in self.enemis: # pour chaque enemi 

                for missile in enemi.missiles: # nous testont pour tous c'est missile

                    if self.vaisseau.test_collision_elg(missile): # si il touche le player
                        
                        # dans ce cas nous apliquons les damage de l'enemi sur le player
                        self.vaisseau.takes_damage(enemi.damage)
                        # et suprimons le missile de sa liste
                        enemi.missiles.remove(missile)

                    if missile.touche_border(): # si il touche le bord
                        # nous suprimons le missile de sa liste
                        enemi.missiles.remove(missile)

    def test_missile_vaisseau(self):
        """teste pour chaque missile du player si il touche un enemi"""

        for enemi in self.enemis: # pour chaque enemis

                for missile in self.vaisseau.missiles: # pour chaque missile du vaisseau

                    if enemi.test_collision_elg(missile): # nous verifions si le missile touche l'enemi
                        
                        # dans ce cas nous apliquons les damage du player sur l'enemi
                        enemi.takes_damage(self.vaisseau.damage)
                        # et suprimons le missile de sa liste            
                        self.vaisseau.missiles.remove(missile)

                    if missile.touche_border(): # si il touche le bord
                        # nous suprimons le missile de sa liste
                        self.vaisseau.missiles.remove(missile)

App()