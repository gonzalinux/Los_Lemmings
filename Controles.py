import pyxel


class Controles:

    def __init__(self, tablero, juego):

        self.tablero = tablero
        self.x_selec = 0
        self.y_selec = 0
        self.juego = juego

        self.queue = list()

    def draw(self):
        pyxel.rectb(self.x_selec * 16, self.y_selec * 16 + self.tablero.top, 16, 16, 10)

        if len(self.queue) != 0:
            for tool in self.queue:
                pyxel.blt(tool[0] * 16, (tool[1] * 16) + self.tablero.top, 2, 16 * (tool[2] - 2), 16, 16, 16, 0)

    def update(self):
        if pyxel.btnr(pyxel.KEY_UP):
            self.y_selec = (self.y_selec - 1) % 14
        if pyxel.btnr(pyxel.KEY_DOWN):
            self.y_selec = (self.y_selec + 1) % 14
        if pyxel.btnr(pyxel.KEY_RIGHT):
            self.x_selec = (self.x_selec + 1) % 16
        if pyxel.btnr(pyxel.KEY_LEFT):
            self.x_selec = (self.x_selec - 1) % 16

        # dibujar herramientas
        # Aqui habiamos puesto la herramienta en el tablero, pero resulta que las
        # herramientas se activan cuando el lemming llega a ellas

        if pyxel.btnr(pyxel.KEY_D):
            if self.tablero.hayBloqueONo(self.x_selec, self.y_selec) == 0:
                elemento = self.hayHerramienta([self.x_selec, self.y_selec, 2])
                if elemento >= 0:
                    self.queue.remove(self.queue[elemento])
                    self.juego.stats["Escaleras"] -= 1
                else:
                    self.queue.append([self.x_selec, self.y_selec, 2])

                    self.juego.stats["Escaleras"] += 1

        if pyxel.btnr(pyxel.KEY_I):
            if self.tablero.hayBloqueONo(self.x_selec, self.y_selec) == 0:
                elemento = self.hayHerramienta([self.x_selec, self.y_selec, 3])
                if elemento >= 0:
                    self.queue.remove(self.queue[elemento])
                    self.juego.stats["Escaleras"] -= 1

                else:
                    self.queue.append([self.x_selec, self.y_selec, 3])

                    self.juego.stats["Escaleras"] += 1

        if pyxel.btnr(pyxel.KEY_P):
            if self.tablero.hayBloqueONo(self.x_selec, self.y_selec) == 0:
                elemento = self.hayHerramienta([self.x_selec, self.y_selec, 4])
                if elemento >= 0:
                    self.queue.remove(self.queue[elemento])
                    self.juego.stats["Paraguas"] -= 1

                else:
                    self.queue.append([self.x_selec, self.y_selec, 4])

                    self.juego.stats["Paraguas"] += 1

        if pyxel.btnr(pyxel.KEY_S):
            if self.tablero.hayBloqueONo(self.x_selec, self.y_selec) == 0 or \
                    self.tablero.hayBloqueONo(self.x_selec, self.y_selec) == 5:
                elemento = self.hayHerramienta([self.x_selec, self.y_selec, 5])
                if elemento >= 0:
                    self.queue.remove(self.queue[elemento])
                    self.juego.stats["Bloqueadores"] -= 1
                elif self.tablero.hayBloqueONo(self.x_selec, self.y_selec) == 5:
                    self.tablero.matriz[self.y_selec][self.x_selec] = 0
                    self.juego.stats["Bloqueadores"] -= 1

                else:
                    self.queue.append([self.x_selec, self.y_selec, 5])

                    self.juego.stats["Bloqueadores"] += 1

    def hayHerramienta(self, content):
        for i in range(len(self.queue)):
            tool = self.queue[i]
            if tool[0] == content[0] and tool[1] == content[1] and tool[2] == content[2]:
                return i
        return -1
