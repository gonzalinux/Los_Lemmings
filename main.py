import pyxel
from Tablero import Tablero
from lemmings import Lemming
from Controles import Controles
import random


class Juego:
    def __init__(self):
        pyxel.init(256, 256)
        pyxel.load("resource.pyxres")
        self.x = 0

        self.tablero = Tablero()
        self.lemmings = []
        self.nlemings = random.randint(10, 20)
        for i in range(self.nlemings):
            self.lemmings.append(Lemming(self.tablero.entrada[0], self.tablero.entrada[1], self))
        self.retrasaleming = 0
        self.controles = Controles(self.tablero, self)
        self.stats = {"Nivel": 0, "Salvados": 0, "Muertos": 0, "Vivos": 0, "Escaleras": 0, "Paraguas": 0,
                      "Bloqueadores": 0}

        pyxel.run(self.update, self.draw)
        self.terminado = False

    def update(self):
        self.x += 1
        # self.lemming.update()
        if self.x == 40 and self.retrasaleming < len(self.lemmings):
            self.stats["Vivos"] += 1
            self.retrasaleming += 1
            self.x = 0
        aux = 0
        aux2 = 0
        for i in range(self.retrasaleming):
            self.lemmings[i].update()
            if not self.lemmings[i].esta_vivo:
                aux += 1
            if self.lemmings[i].salvado:
                aux2 += 1
        self.stats["Muertos"] = aux
        self.stats["Vivos"] = self.nlemings - aux
        self.stats["Salvados"] = aux2
        if self.stats["Salvados"] + self.stats["Muertos"] > self.nlemings:
            self.terminado = True
        self.controles.update()

    def draw(self):

        pyxel.cls(0)

        pyxel.rect(0, 0, pyxel.height, 32, 9)
        x = 20
        y = 1
        for cosa in self.stats.keys():
            pyxel.text(x, y, cosa + ": " + str(self.stats.get(cosa)), 2)
            x += 70
            if x + 70 >= 256:
                x = 20
                y += 10

        self.tablero.draw()

        self.controles.draw()
        for i in range(self.retrasaleming):
            self.lemmings[i].draw()

        # if self.terminado:


Juego()
