import pyxel
import math
from copy import deepcopy

class ElementGraphique():

    def __init__(self, pos_x: int, pos_y: int, size: tuple, image_pos: tuple, direction: tuple, transparant_col: int, image: int = 0) -> None:
        
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.dx = direction[0]
        self.dy = direction[1]

        self.size = size

        self.image_pos = image_pos
        self.image = image
        self.transparant_col = transparant_col

    def draw(self):

        pyxel.blt(self.pos_x,self.pos_y,self.image,self.image_pos[0],self.image_pos[1],self.size[0],self.size[1],self.transparant_col)

    def apply_direction(self):

        self.pos_x += self.dx
        self.pos_y += self.dy

    def update(self):

        self.apply_direction()

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

class AnimateElementGraphique(ElementGraphique):

    def __init__(self, pos_x: int, pos_y: int, size: tuple, pos_image_liste: dict[list[tuple]],default_state:str,anim_speed:int, direction: tuple, transparent_color: int, image_number: int = 0) -> None:
        super().__init__(pos_x, pos_y, size, pos_image_liste[default_state][0],direction, transparent_color, image_number)

        self.frame = 0
        self.animations= pos_image_liste
        self.state = default_state
        self.anim_speed = anim_speed
        self.one_anim_bool = False
        self.state_one_anim = self.state
        self.end_state = self.state
        self.end_function = None
    
    def update_anim(self):

        if self.one_anim_bool:
            self.state = self.state_one_anim

        if self.frame >= len(self.animations[self.state]):
            self.frame = 0

            if self.one_anim_bool:
                self.state = self.end_state
                self.one_anim_bool = False

                if self.end_function != None:
                    self.end_function()

        self.image_pos = self.animations[self.state][self.frame]

        if pyxel.frame_count %self.anim_speed == 0:
            
            self.frame += 1

    def one_anim(self,state:str,end_state:str, end_function = None):
        self.frame = 0
        self.state_one_anim = state
        self.one_anim_bool = True
        self.end_state = end_state
        self.end_function = end_function
    
    def draw(self):
        self.update_anim()
        super().draw()