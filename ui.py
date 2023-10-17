import pyxel
from sprite import *
from text import Text

info = {"a":pyxel.KEY_A,"z":pyxel.KEY_Z,"e":pyxel.KEY_E,"r":pyxel.KEY_R,"t":pyxel.KEY_T,"y":pyxel.KEY_Y,"u":pyxel.KEY_U,"i":pyxel.KEY_I,
        "o":pyxel.KEY_O,"p":pyxel.KEY_P,"q":pyxel.KEY_Q,"s":pyxel.KEY_S,"d":pyxel.KEY_D,"f":pyxel.KEY_F,"g":pyxel.KEY_G,
        "h":pyxel.KEY_H,"j":pyxel.KEY_J,"k":pyxel.KEY_K,"l":pyxel.KEY_L,"m":pyxel.KEY_M,"w":pyxel.KEY_W,"x":pyxel.KEY_X,"c":pyxel.KEY_C,
        "v":pyxel.KEY_V,"b":pyxel.KEY_B,"n":pyxel.KEY_N,"_":pyxel.KEY_UNDERSCORE,"1":pyxel.KEY_1,"2":pyxel.KEY_2,"3":pyxel.KEY_3,
        "4":pyxel.KEY_4,"5":pyxel.KEY_5,"6":pyxel.KEY_6,"7":pyxel.KEY_7,"8":pyxel.KEY_8,"9":pyxel.KEY_9,"0":pyxel.KEY_0,
        "delete":pyxel.KEY_DELETE,"backspace":pyxel.KEY_BACKSPACE,"enter":13}

info_only_number = {"1":pyxel.KEY_1,"2":pyxel.KEY_2,"3":pyxel.KEY_3,
        "4":pyxel.KEY_4,"5":pyxel.KEY_5,"6":pyxel.KEY_6,"7":pyxel.KEY_7,"8":pyxel.KEY_8,"9":pyxel.KEY_9,"0":pyxel.KEY_0}

class Button(Rect):

    def __init__(self, pos_x: int, pos_y: int, size: tuple, col: int, call_back, one_click: bool, full: bool = True, call_back_right_click = None) -> None:
        super().__init__(pos_x, pos_y, size, col, full)

        self.call_back = call_back

        self.one_click = one_click

        self.block = False

        self.call_back_right_click = call_back_right_click

    def use(self, fonction):

        if not self.block:

            fonction(self)

    def update(self):

        self.test_click(pyxel.MOUSE_BUTTON_LEFT, self.call_back)

        self.test_click(pyxel.MOUSE_BUTTON_RIGHT, self.call_back_right_click)

    def test_click(self, button: int, fonction):

        if self.one_click:
            verif = pyxel.btnp(button)
        else:
            verif = pyxel.btn(button)

        if verif:

            if self.test_collision_point((pyxel.mouse_x, pyxel.mouse_y)):

                self.use(fonction)


class TextButton(Button):

    def __init__(self, pos_x: int, pos_y: int, size: tuple, col: int, call_back, text: str, text_color: int, text_size: int,layout: list = [False,False,False,False], padding: list = [0,0], center: tuple = (True,True), fill: bool = True) -> None:
        super().__init__(pos_x, pos_y, size, col, call_back, fill)

        half_x = int(self.size[0]/2)
        half_y = int(self.size[1]/2)

        x = self.pos_x + half_x + padding[0]
        y = self.pos_y + half_y + padding[1]

        if layout[0]:
            x -= half_x
        if layout[1]:
            x += half_x
        if layout[2]:
            y -= half_y
        if layout[3]:
            y += half_y

        self.text = Text(x, y,(text_size,text_size),text_color,text,text_size)

        if center[0]:

            x = self.text.pos_x + int(self.text.size[0]/2)

        if center[1]:
            y = self.text.pos_y + int(self.text.size[1]/2)

            self.text.set_position(x,y)

    def draw(self):
        
        super().draw()

        if self.visibility:
            self.text.draw()

class ImageButton(Button):

    def __init__(self, pos_x: int, pos_y: int, size: tuple, col: int, image: list, image_size: tuple, transparent_color: int, call_back, one_click: bool,layout: list = [False,False,False,False], padding: list = [0,0], center: tuple = (True,True), fill: bool = True) -> None:
        super().__init__(pos_x, pos_y, size, col, call_back, one_click,fill)

        self.transparent_color = transparent_color

        self.image = image
    
        pixel_size_x = int(image_size[0]/len(image[0]))
        pixel_size_y = int(image_size[1]/len(image))

        self.pixel_size = (pixel_size_x,pixel_size_y)

        half_x = int(self.size[0]/2)
        half_y = int(self.size[1]/2)

        x = self.pos_x + half_x + padding[0]
        y = self.pos_y + half_y + padding[1]

        if layout[0]:
            x -= half_x
        if layout[1]:
            x += half_x
        if layout[2]:
            y -= half_y
        if layout[3]:
            y += half_y

        if center[0]:

            x -= int(image_size[0]/2)

        if center[1]:
            y -= int(image_size[1]/2)

        self.image_x = x
        self.image_y = y

    def draw(self):
        
        super().draw()

        if self.visibility:
            
            x = self.image_x
            y = self.image_y

            for row in self.image:

                for case in row:

                    if case != self.transparent_color:

                        pyxel.rect(x,y,self.pixel_size[0],self.pixel_size[1],case)

                    x += self.pixel_size[0]

                x = self.image_x
                y += self.pixel_size[1]


class Input(Rect):

    def __init__(self, pos_x: int, pos_y: int, size: tuple, col: int, text_color: int, text_size: int, fill: bool = True, call_back = None, only_number: bool = False, default_str: str = "...", limit_cara: int = 0) -> None:
        super().__init__(pos_x, pos_y, size, col, fill)

        half_y = int(self.size[1]/2)

        self.text = Text(self.pos_x + text_size, self.pos_y + half_y ,(text_size,text_size),text_color,"",text_size)

        y = self.text.pos_y - int(self.text.size[1]/2)

        self.text.set_position(self.text.pos_x,y)

        self.text.set_text(default_str)

        self.text_tap = False

        self.current_text = default_str

        self.call_back = call_back

        self.only_number = only_number

        self.default_str = default_str

        self.limit_cara = limit_cara

    def draw(self):
        
        super().draw()

        if self.visibility:
            self.text.draw()

    def update(self):

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):

            if self.test_collision_point((pyxel.mouse_x,pyxel.mouse_y)):

                self.launch_text_tap()
            else:
                if self.text_tap == True:
                    self.stop_text_tap()

        self.update_text_tap()

    def launch_text_tap(self):

        if self.text_tap == False:
            self.current_text = ""
            self.text.set_text("")
            self.text_tap = True
        else:
            self.stop_text_tap()

    def stop_text_tap(self):

        if len(self.current_text) >= 1:
                self.text_tap = False
        else:
            self.current_text = self.default_str
            self.text.set_text(self.default_str)
            self.text_tap = False

        if self.call_back != None:

            self.call_back(self.current_text)

    def update_text_tap(self):

        if self.text_tap:

            lettre = self.tap_text()

            if lettre != None:

                if lettre == "delete":

                    self.current_text = ""

                elif lettre == "backspace":

                    self.current_text = self.current_text[0:-1]

                elif lettre == "enter":
        
                    self.stop_text_tap()
                    return
                
                else:

                    if self.limit_cara == 0 or not len(self.current_text) + 1 > self.limit_cara: 
                        self.current_text += lettre

                self.text.set_text(self.current_text)

                if self.text.size[0] > self.size[0]:

                    text_size = self.text.size[0]
                    index = -1

                    while text_size > self.size[0]:
                        
                        self.text.set_lettre_visibility(index,False)

                        text_size -= self.text.get_lettre_size(index)[0] + self.text.espacement
                        index -= 1

    def tap_text(self):

        if self.only_number:
            dico = info_only_number
        else:
            dico = info

        for cle,valeur in dico.items():

                if pyxel.btnp(valeur):
                    return cle
    