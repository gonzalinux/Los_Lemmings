import random
from enum import Enum

import pyxel


class Tablero:
    def __init__(self):
        self.left = 32
        self.top = 32
        self.width = 16
        self.height = 16
        self.matriz = []
        for x in range(14):
            self.matriz.append([])
            for Y in range(16):
                self.matriz[x].append(0)

        filas = []
        while len(filas) < 7:
            num = random.randint(0, 13)
            if num not in filas:
                filas.append(num)

        self.bloques = []
        filas.sort()
        for nfila in filas:
            ancho = random.randint(5, 10)
            origen = random.randint(0, 15 - ancho)
            for x in range(ancho):

                self.matriz[nfila][origen + x] = 1
                if self.matriz[nfila - 1][origen + x] == 0 and nfila != 0:
                    self.bloques.append([origen + x, nfila])

        self.entrada = self.bloques[random.randint(0, len(self.bloques) - 1)]
        self.salida = self.entrada
        while self.entrada == self.salida:
            self.salida = self.bloques[random.randint(0, len(self.bloques) - 1)]

    def draw(self):
        # Hay que cambiar segun lo que tengas en resources
        # Primero se ponen todas las casillas como cuadricula y luego se rellenan con lo que tengan
        for y in range(len(self.matriz)):
            for x in range(len(self.matriz[y])):
                pyxel.blt(self.width * x, 32 + self.height * y, 0, 16, 0, self.width, self.height, )
                # si son bloques
                if self.matriz[y][x] == 1:
                    pyxel.blt(self.width * x, 32 + self.height * y, 0, 0, 0, self.width, self.height, )
                # si son herramientas
                elif self.matriz[y][x] != 0:
                    pyxel.blt(self.width * x, 32 + self.height * y,
                              2, 16*(self.matriz[y][x]-2), 0, self.width, self.height,0)

        pyxel.blt(self.entrada[0] * self.width, (self.entrada[1] + 1) * self.height, 1, 16, 0, self.width, self.height)
        pyxel.blt(self.salida[0] * self.width, (self.salida[1] + 1) * self.height, 1, 0, 0, self.width, self.height)

    # def update(self):
    # pala para romper bloques

    def getCasillaXY(self, x, y):

        """Dadas unas coordenadas en píxeles me da la casilla donde esta el Lemming. """

        xaux = int(x / 16)
        yaux = int((y - self.top) / 16)
        if x < 0:
            xaux = -1
        if y < 0:
            yaux = -1

        return [xaux, yaux]

    def hayBloqueONo(self, columna, fila):
        if columna >= 16 or columna < 0:
            return 1
        if fila >= 14 or fila < 0:
            return 1
        return self.matriz[fila][columna]
