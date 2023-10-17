import pyxel
from sprite import *
from random import randint

lettres = {"a":[[0, 1, 1, 0], [1, 0, 0, 1], [1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1]],
"b":[[1, 1, 1, 0], [1, 0, 0, 1], [1, 1, 1, 0], [1, 0, 0, 1], [1, 1, 1, 0]],
"c":[[0, 1, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 1]],
"d":[[1, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 0]],
"e":[[0, 1, 1], [1, 0, 0], [1, 1, 0], [1, 0, 0], [0, 1, 1]],
"f":[[0, 1, 1], [1, 0, 0], [1, 1, 0], [1, 0, 0], [1, 0, 0]],
"g":[[0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 1, 1], [1, 0, 0, 1], [0, 1, 1, 1]],
"h":[[1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1]],
"i":[[1], [0], [1], [1], [1]],
"j":[[0, 0, 1], [0, 0, 1], [0, 0, 1], [1, 0, 1], [0, 1, 1]],
"k":[[1, 0, 0, 1], [1, 0, 1, 0], [1, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1]],
"l":[[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 1]],
"o":[[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]],
"p":[[1, 1, 1, 0], [1, 0, 0, 1], [1, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
"q":[[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1]],
"r":[[1, 1, 0], [1, 0, 1], [1, 1, 1], [1, 1, 0], [1, 0, 1]],
"s":[[0, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 0]],
"t":[[1, 1, 1], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
"u":[[1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
"x":[[1, 0, 1], [1, 0, 1], [0, 1, 0], [1, 0, 1], [1, 0, 1]],
"y":[[1, 0, 1], [1, 0, 1], [1, 0, 1], [0, 1, 0], [0, 1, 0]],
"z":[[1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]],
"m":[[1, 0, 0, 0, 1], [1, 1, 0, 1, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1]],
"n":[[1, 0, 0, 0, 1], [1, 1, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 1, 1], [1, 0, 0, 0, 1]],
"v":[[1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [0, 1, 0, 1, 0], [0, 1, 0, 1, 0], [0, 0, 1, 0, 0]],
"w":[[1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 1, 0, 1, 1], [1, 0, 0, 0, 1]],
".":[[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
"_":[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
"-":[[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
"+":[[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [1, 1, 1, 1, 1], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0]],
"0":[[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
"1":[[1, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
"2":[[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
"3":[[1, 1, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [1, 1, 1]],
"4":[[1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1]],
"5":[[1, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
"6":[[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
"7":[[1, 1, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [0, 0, 1]],
"8":[[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
"9":[[1, 1, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1]],}

class Letter():

    def __init__(self, image: list, pos_x: int, pos_y: int, pyxel_size: tuple, col: int) -> None:

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.pyxel_size = pyxel_size

        self.col = col
        
        self.image = image

        self.visibility = True

        self.size = (len(self.image[0]) * self.pyxel_size[0] , len(self.image) * self.pyxel_size[1])
    
    def draw(self):

        if self.visibility:

            x = self.pos_x
            y = self.pos_y

            for row in self.image:

                for case in row:

                    if case == 1:

                        pyxel.rect(x,y,self.pyxel_size[0],self.pyxel_size[1],self.col)

                    x += self.pyxel_size[0]

                x = self.pos_x
                y += self.pyxel_size[1]

class Text():

    def __init__(self, pos_x: int, pos_y: int, pyxel_size: tuple, col: int, text: str, espacement: int = 5) -> None:
        
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.pyxel_size = pyxel_size

        self.col = col

        self.text = text

        self.espacement = espacement

        self.lettres = []

        self.set_text(self.text)

    def set_position(self, x: int, y: int):

        decalage_x = self.pos_x - x
        decalage_y = self.pos_y - y

        self.pos_x = x
        self.pos_y = y

        for l in self.lettres:
            l.pos_x += decalage_x
            l.pos_y += decalage_y
        
    def draw(self):

        for l in self.lettres:

            l.draw()

    def set_text(self, text: str):

        self.lettres = []

        x = self.pos_x
        y = self.pos_y

        size = [0,5*self.pyxel_size[1]]

        for lettre in text:

            test = lettre

            if lettre == " ":
                test = "-"

            if lettre == "\n":

                add = (5 * self.pyxel_size[1]) + self.espacement

                y += add
                size[1] += add

                x = self.pos_x

            if test in lettres:

                self.lettres.append(Letter(lettres[test],x,y,self.pyxel_size,self.col))

                add = self.lettres[-1].size[0] + self.espacement

                x += add
                size[0] += add

        self.size = size

    def set_lettre_visibility(self, lettre_index: int, visibility: bool):

        if lettre_index <= len(self.lettres) - 1  or lettre_index >= -len(self.lettres) - 1:

            self.lettres[lettre_index].visibility = visibility
    
    def get_lettre_size(self, lettre_index: int):

        return self.lettres[lettre_index].size