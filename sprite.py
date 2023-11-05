import pyxel
import math
from copy import deepcopy

"""
prefab des classe pour des element qui seront afficher dans le jeux
"""

class ElementGraphique():
    # classe de base pour tous les element qui s'afiche

    def __init__(self, pos_x: int, pos_y: int, size: tuple, image_pos: tuple, direction: tuple, transparant_col: int, image: int = 0) -> None:

        # parametre pour aficher

        # pos
        self.pos_x = pos_x
        self.pos_y = pos_y

        # direction
        self.dx = direction[0]
        self.dy = direction[1]

        # taille
        self.size = size

        # l'emplacement de l'image dans la sprite sheet
        self.image_pos = image_pos

        # le numero de l'image
        self.image = image

        # la couleur transparent
        self.transparant_col = transparant_col

    def draw(self):
        """fonction qui affiche l'element graphique"""
        
        pyxel.blt(self.pos_x,self.pos_y,self.image,self.image_pos[0],self.image_pos[1],self.size[0],self.size[1],self.transparant_col)

    def apply_direction(self):
        """fonction qui applique la direction sur la position"""

        self.pos_x += self.dx
        self.pos_y += self.dy

    def update(self):
        """fonction qui update l'element graphique"""

        # aplique la direction
        self.apply_direction()

    def test_collision_elg(self, target:'ElementGraphique'):
        """fonction qui teste si l'element graphique et en colision avec un autre element graphique donner en parametre et renvoi vrai ou faux en fonction"""

        if target.pos_x < self.pos_x+self.size[0] and target.pos_y < self.pos_y+self.size[1] and target.pos_x+target.size[0] > self.pos_x and target.pos_y+target.size[1] > self.pos_y:
            return True
        return False

    def touche_border(self):
        """fonction qui teste si l'element graphique touche """

        if self.pos_x < 0 or self.pos_x + self.size[0] > pyxel.width:
            return True
        if self.pos_y < 0 or self.pos_y + self.size[1] > pyxel.height:
            return True
        
        return False

class AnimateElementGraphique(ElementGraphique):
    # classe de base pour tous les element qui s'afiche avec des animations

    def __init__(self, pos_x: int, pos_y: int, size: tuple, pos_image_liste: dict[list[tuple]],default_state:str,anim_speed:int, direction: tuple, transparent_color: int, image_number: int = 0) -> None:
        super().__init__(pos_x, pos_y, size, pos_image_liste[default_state][0],direction, transparent_color, image_number)

        # toute les variable pour animer l'element graphique

        # la frame actuelle
        self.frame = 0
        # les animation qui sont relier chacun a un etat dans un dico
        self.animations= pos_image_liste
        # etat actuelle
        self.state = default_state
        # vitesse de l'animation
        self.anim_speed = anim_speed
        # booléen permetant de savoir si nous somme en train de faire une animation qui va s'arete a la fin de cette animation
        self.one_anim_bool = False
        # etat qui va s'activer apres la fin de l'animation qui se joue une fois
        self.end_state = self.state
        #fonction qui va s'exécuter apres la fin de l'animation qui se joue une fois
        self.end_function = None
    
    def update_anim(self):
        """fonction qui update la position de l'image en fonction de l'animation qui se joue"""

        # si nous arrivons a la fin de l'animation nous la rejouons 
        if self.frame >= len(self.animations[self.state]):
            self.frame = 0

            # et si l'animation ce jouez une seule fois nous changez l'etat vers celui voulu et exécuton la fonction si elle existe qui se joue a la fin de l'animation
            if self.one_anim_bool:
                self.state = self.end_state
                self.one_anim_bool = False

                if self.end_function != None:
                    self.end_function()

        # set la position de l'image en de l'etat et la frame actuelle
        self.image_pos = self.animations[self.state][self.frame]

        # en fonction de la vitesse d'animation change de frame pour la suivante 
        if pyxel.frame_count %self.anim_speed == 0:
            
            self.frame += 1

    def one_anim(self,state:str,end_state:str, end_function = None):
        """lance une animation qui va ce joue qu'une fois"""
        #set la frame a zero met a l'etat voulu
        self.frame = 0
        self.state = state
        # set les variable utile pour jouer l'animation une fois
        self.one_anim_bool = True
        self.end_state = end_state
        self.end_function = end_function
    
    def draw(self):
        self.update_anim()
        super().draw()