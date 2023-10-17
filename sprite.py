import pyxel
import math
from copy import deepcopy

class Sprite():

    def __init__(self, pos_x:int, pos_y:int, size:tuple,pos_image:tuple,transparent_color:int,image_number:int = 0) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = size
        self.pos_image = pos_image
        self.image_number = image_number
        self.transparent_color = transparent_color
        self.visibility = True

    def draw(self):

        if self.visibility:
            pyxel.blt(self.pos_x,self.pos_y,self.image_number,self.pos_image[0],self.pos_image[1],self.size[0],self.size[1],self.transparent_color)
    
    def touche_border(self):

        if self.pos_x < 0 or self.pos_x + self.size[0] > pyxel.width:
            return True
        if self.pos_y < 0 or self.pos_y + self.size[1] > pyxel.height:
            return True
        
        return False
    
    def test_collision_sprite(self, target:'Sprite'):

        if target.pos_x < self.pos_x+self.size[0] and target.pos_y < self.pos_y+self.size[1] and target.pos_x+target.size[0] > self.pos_x and target.pos_y+target.size[1] > self.pos_y:
            return True
        return False
    
    def test_collision_pos(self, pos:list, size:dict):

        if pos[0] < self.pos_x+self.size[0] and pos[1] < self.pos_y+self.size[1] and pos[0]+size[0] > self.pos_x and pos[1]+ size[1] > self.pos_y:
            return True
        return False
    
    def test_collision_point(self, cord:tuple):

        if cord[0] >= self.pos_x and cord[0] <= self.pos_x+self.size[0] and cord[1] >= self.pos_y and cord[1] <= self.pos_y+self.size[1] :
            return True
        return False
    
    def get_pos(self):

        return (self.pos_x, self.pos_y)
    
    def get_half_x(self):

        return self.pos_x + self.size[0]/2
    
    def get_half_y(self):

        return self.pos_y + self.size[1]/2
    
    def set_visibility(self, visibility: bool):

        self.visibility = visibility

    def get_distance(self, target: 'Sprite'):

        return abs(math.sqrt((self.pos_x-target.pos_x)**2+(self.pos_y-target.pos_y)**2))
    
    def get_size(self):

        return self.size


class AnimateSprite(Sprite):


    def __init__(self, pos_x: int, pos_y: int, size: tuple, pos_image_liste: dict[list[tuple]],default_state:str,anim_speed:int, transparent_color: int, image_number: int = 0) -> None:
        super().__init__(pos_x, pos_y, size, pos_image_liste[default_state][0], transparent_color, image_number)

        self.frame = 0
        self.animations= pos_image_liste
        self.state = default_state
        self.anim_speed = anim_speed
        self.one_anim_bool = False
        self.state_one_anim = self.state
        self.end_state = self.state
    
    def update_anim(self):

        if self.one_anim_bool:
            self.state = self.state_one_anim
        if self.frame >= len(self.animations[self.state]):
            self.frame = 0
            if self.one_anim_bool:
                self.state = self.end_state
                self.one_anim_bool = False

        self.pos_image = self.animations[self.state][self.frame]

        if pyxel.frame_count %self.anim_speed == 0:
            
            self.frame += 1

    def one_anim(self,state:str,end_state:str):
        self.frame = 0
        self.state_one_anim = state
        self.one_anim_bool = True
        self.end_state = end_state
    
    def draw(self):
        self.update_anim()
        super().draw()


class MoveSprite(Sprite):


    def __init__(self, pos_x: int, pos_y: int, size: tuple, pos_image: tuple, transparent_color: int, speed: int, proximity: int = 10, image_number: int = 0) -> None:
        super().__init__(pos_x, pos_y, size, pos_image, transparent_color, image_number)

        # movement variable
        self.direction = [0,0]
        self.speed = speed

        self.pos = (self.pos_x,self.pos_y) #pos to go

        self.proximity = proximity

        self.have_to_move = False

        #self.in_move = False

    def got_to(self, pos: tuple, proximity: int = 10):

        self.pos = pos
        self.proximity = proximity
        self.have_to_move = True

    def go_to_direction(self, pos: tuple):

        self.pos = pos
        self.get_direction()
        
    def get_direction(self):
        signe = 1
        adj = self.pos_x - self.pos[0]
        opos = self.pos_y - self.pos[1]
        if adj > 0:
            signe = -1
        if not adj == 0:
            angle = math.atan(opos/adj) 
            self.direction[0] = math.cos(angle) * signe
            self.direction[1] = math.sin(angle) * signe
        else:
            self.direction[0] = 0
            if opos < 0:
                self.direction[1] = 1
            else:
                self.direction[1] = -1

        if abs(adj) <=  self.proximity and abs(opos) <=  self.proximity:
            self.arrived()
        
    def move(self, dt: float):

        if self.have_to_move:

            self.get_direction()

        self.pos_x += self.direction[0] * self.speed * dt
        self.pos_y += self.direction[1] * self.speed * dt

    def update(self):

        self.move(0.025)

    def arrived(self):
        self.direction = [0,0]
        self.pos = (self.pos_x,self.pos_y)
        self.have_to_move = False

class Rect(Sprite):

    def __init__(self, pos_x: int, pos_y: int, size: tuple, col: int, fill: bool = True) -> None:
        super().__init__(pos_x, pos_y, size, (0,0), 0, 0)

        self.col = col

        self.fill = fill

        self.name = "rect"

    def draw(self):

        if self.visibility:
            if self.fill:
                pyxel.rect(self.pos_x,self.pos_y,self.size[0],self.size[1],self.col)
            else:
                pyxel.rectb(self.pos_x,self.pos_y,self.size[0],self.size[1],self.col)

class Circle(Sprite):

    def __init__(self, pos_x: int, pos_y: int, size: int, col: int, fill: bool = True) -> None:
        super().__init__(pos_x, pos_y, size, (0,0), 0, 0)

        self.col = col

        self.fill = fill

    def draw(self):

        if self.visibility:
            if self.fill:
                pyxel.circ(self.pos_x,self.pos_y,self.size,self.col)
            else:
                pyxel.circb(self.pos_x,self.pos_y,self.size,self.col)


class Image(Sprite):

    def __init__(self, pos_x: int, pos_y: int, image: list, size: tuple, transparent_color: int = -1, rotation: int = 0) -> None:
        super().__init__(pos_x, pos_y, size, 0, transparent_color, 0)

        self.image = deepcopy(image)

        pixel_size_x = int(size[0]/len(image[0]))
        pixel_size_y = int(size[1]/len(image))
        
        self.rotation = 0

        self.pixel_size = [pixel_size_x,pixel_size_y]

        self.turn(rotation)
    
    def draw(self):

        if self.visibility:
        
            x = self.pos_x
            y = self.pos_y

            for row in self.image:

                for case in row:

                    if self.transparent_color == -1 or case != self.transparent_color:

                        pyxel.rect(x,y,self.pixel_size[0],self.pixel_size[1],case)

                    x += self.pixel_size[0]

                x = self.pos_x
                y += self.pixel_size[1]


    def complex_test_collision_sprite(self, target:'Sprite'):

        if target.pos_x < self.pos_x+self.size[0] and target.pos_y < self.pos_y+self.size[1] and target.pos_x+target.size[0] > self.pos_x and target.pos_y+target.size[1] > self.pos_y:
            return True
        return False
    
    def complex_test_collision_pos(self, pos:list, size:dict):

        if pos[0] < self.pos_x+self.size[0] and pos[1] < self.pos_y+self.size[1] and pos[0]+size[0] > self.pos_x and pos[1]+ size[1] > self.pos_y:
            return True
        return False
    
    def complex_test_collision_point(self, cord:tuple):

        if self.test_collision_point(cord):
            
            return self.test_collision_pixel((cord[0]-self.pos_x,cord[1]-self.pos_y))
    
    def test_collision_pixel(self, pos: tuple):

        row = int(pos[0]/self.pixel_size[0])
        col = int(pos[1]/self.pixel_size[1])

        print(pos,row,col,self.image[row][col],self.test_collision_point((pos[0]+self.pos_x,pos[1]+self.pos_y)))

        if self.image[row][col] != self.transparent_color:
            return True
        else:
            return False
        
    def turn(self, rotation):

        new_rotation = self.rotation + rotation 

        dif = new_rotation - self.rotation

        if dif == 90 or dif == -90:

            self.pixel_size.reverse()

        self.rotation = new_rotation

        if rotation == 180 or rotation == -180:
            
            self.reverse()

            self.image.reverse()

        if rotation == -90 or rotation == 270:

            self.image.reverse()

            self.turn_90()

        if rotation == 90 or rotation == -270:

            self.reverse()

            self.turn_90()

    def reverse(self):

        for ligne in self.image:

            ligne.reverse()

    def turn_90(self):

        image = []
        index = 0

        for row in self.image:

            for case in row:
                
                if len(image) < index + 1:
                    image.append([case])
                else:
                    image[index].append(case)

                index += 1
            
            index = 0
        
        self.image = image
    
    def set_rotation(self, rotation):

        new_rotation = rotation

        dif = new_rotation - self.rotation

        print(dif)

        self.turn(dif)