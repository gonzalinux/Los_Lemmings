import pyxel
from enum import Enum


class Lemming:
    def __init__(self, x_actual, y_actual, juego):

        # dict para guardar sentidos posibles
        self.sentidos = {"derecha": 0, "izquierda": 1, "arriba": 2, "abajo": 3, "quieto": -1}
        # Donde está el Lemming al crearse
        # Vamos a guardar el movimiento horizontal y vertical
        self.sent_horiz = self.sentidos["izquierda"]
        self.sent_vert = self.sentidos["quieto"]
        # te guardas por si tiene que esperar
        self.sent_anterior = self.sentidos["izquierda"]
        self.x_actual = x_actual * 16
        self.y_actual = y_actual * 16 + 16
        self.juego = juego
        self.esta_vivo = True
        self.tablero = self.juego.tablero
        self.posescalera=[]


        # solo se muere cuando cae 3 o mas
        self.contadorcaida = 0
        # para saber si se va morir o no al final de una caida
        self.paraguas = False
        self.escalera = False
        self.bloqueando = False
        self.salvado=False

    def draw(self):
        # cambiar datos de mi imagen
        if not self.salvado:
            if self.sent_horiz == self.sentidos["derecha"]:
                pyxel.blt(self.x_actual, self.y_actual, 0, 0, 16, 16, 16, 0)
            elif self.sent_horiz == self.sentidos["izquierda"]:
                pyxel.blt(self.x_actual, self.y_actual, 0, 0, 16, -16, 16, 0)
            # Si se cae mira hacia abajo
            elif self.sent_vert == self.sentidos["abajo"]:
                pyxel.blt(self.x_actual, self.y_actual, 0, 0, 16, 16, -16, 0)

    def update(self):
        # el Lemmimg tiene que comprobar que:
        # 1. Que haya suelo y lleve cayendo un rato -> se va a morir (READY)
        # 2. Que haya suelo y no esté cayendo -> para saber que va a caerse
        # 3. Que tenga un bloque delante -> para saber si tiene que darse la vuelta
        # 4. Que haya llegado a la salida -> desaparezca
        # 5. Que esté vivo -> para moverse (READY)

        if self.esta_vivo:

            x_aux = self.x_actual
            y_aux = self.y_actual + 8
            # los extras son para comprobar que bloque va a tocar ya que la esquina
            # x y es la superior izquierda y no nos sirve a veces
            extraizquierda = -1
            extraderecha = -1

            # movimiento normal dercha izquierda
            if self.sent_horiz == self.sentidos["derecha"]:
                x_aux += 1
                extraderecha = 16

            elif self.sent_horiz == self.sentidos["izquierda"]:
                x_aux += -1
                extraizquierda = 16

            if self.sent_vert == self.sentidos["arriba"]:
                y_aux -= 1

            elif self.sent_vert == self.sentidos["abajo"]:
                if self.paraguas:
                    y_aux += 0.5
                else:
                    y_aux += 1
            # nos guardamos la casilla a la que va a pasar y la que tiene debajo
            siguiente_casilla = self.tablero.getCasillaXY(x_aux + extraderecha, y_aux)
            casilla_debajo = self.tablero.getCasillaXY(self.x_actual + extraizquierda, self.y_actual)
            casilla_debajo[1] += 1
            if self.bloqueando:
                if self.tablero.hayBloqueONo(siguiente_casilla[0], siguiente_casilla[1]) != 0:
                    self.bloqueando = False
                    if self.sent_anterior == self.sentidos["derecha"]:
                        self.sent_horiz = self.sentidos["izquierda"]
                    else:
                        self.sent_horiz = self.sentidos["derecha"]
                else:
                    return
                    # comprobamos si pasa por paraguas (ATENCION) esto puede que haya que ponerlo solo si esta cayendo

            if self.tablero.hayBloqueONo(siguiente_casilla[0], siguiente_casilla[1]) == 4:
                self.paraguas = True
                # comprobamos si toca alguna herramienta para activarla
                # (ATENCION) si nos encontramos un bloqueador el leming se debe quedar quieto hasta que desaparezca
                # falta por implementar eso
            for tool in self.juego.controles.queue:
                if tool[0] == siguiente_casilla[0] and tool[1] == siguiente_casilla[1]:
                    self.tablero.matriz[tool[1]][tool[0]] = tool[2]
                    self.juego.controles.queue.remove(tool)
                    if tool[2] == 5:
                        self.bloqueando = True
                        self.sent_anterior = self.sent_horiz
                        self.sent_horiz = "quieto"

            # si hay una escalera se sube (ATENCION) Falta hacer que pare de subir al terminar la escalera
            if self.tablero.hayBloqueONo(siguiente_casilla[0], siguiente_casilla[1]) == 2 and \
                    self.sent_horiz == self.sentidos["derecha"]:
                self.sent_vert = self.sentidos["arriba"]
                self.posescalera=siguiente_casilla
                self.escalera = True

            if self.tablero.hayBloqueONo(siguiente_casilla[0], siguiente_casilla[1]) == 3 and \
                    self.sent_horiz == self.sentidos["izquierda"]:

                self.sent_vert = self.sentidos["arriba"]
                self.escalera = True
                self.posescalera = siguiente_casilla

            if self.tablero.hayBloqueONo(casilla_debajo[0], siguiente_casilla[1]+1) == 3 and \
                    self.sent_horiz == self.sentidos["derecha"]:

                self.sent_vert = self.sentidos["abajo"]
                self.escalera = True
                self.posescalera = siguiente_casilla
            if self.tablero.hayBloqueONo(siguiente_casilla[0], siguiente_casilla[1]+1) == 2 and \
                    self.sent_horiz == self.sentidos["izquierda"]:
                self.sent_vert = self.sentidos["abajo"]
                self.posescalera=siguiente_casilla
                self.escalera = True

            # falta hacer que baje escaleras si se las encuentra debajo
            # lo siguiente es para que se salga antes, es posible que haya que cambiarlo
            if self.escalera:
                casillaux = self.tablero.getCasillaXY(x_aux + extraderecha, y_aux + 8)
                if casillaux[1] != self.tablero.getCasillaXY(self.x_actual, self.y_actual + 16)[1]:
                    self.sent_vert = self.sentidos["quieto"]
                elif abs(casillaux[0]- self.posescalera[0])==2:
                    self.escalera = False
                else:
                    self.x_actual = x_aux
                    self.y_actual = y_aux - 8
                    return

            # Si cae y hay suelo en la siguiente, muere el lemming

            if self.sent_vert == self.sentidos["abajo"] and self.sent_horiz == self.sentidos["quieto"]:
                # si hay suelo
                if self.tablero.hayBloqueONo(siguiente_casilla[0],
                                             siguiente_casilla[1]) == 1:
                    # si se va a morir (mas de dos bloques y no hay paraguas
                    if self.contadorcaida > 2 and not self.paraguas:
                        print("sa caio")
                        self.esta_vivo = False
                    # si sibrevive se restaura el sentido y deja de moverse en vertical
                    else:
                        self.paraguas = False
                        self.sent_horiz = self.sent_anterior
                        self.sent_vert = self.sentidos["quieto"]
                        self.contadorcaida = 0
                        y_aux -= 8

                # si no hay bloque se comprueba si ha cambiado de casilla para aumentar el contador
                elif siguiente_casilla[1] != self.tablero.getCasillaXY(self.x_actual, self.y_actual + 7)[1]:
                    self.contadorcaida += 1

            # si no esta cayendo y se encuentra con un bloque se da la vuelta
            elif self.tablero.hayBloqueONo(siguiente_casilla[0], siguiente_casilla[1]) == 1 \
                    or self.tablero.hayBloqueONo(siguiente_casilla[0], siguiente_casilla[1]) == 5:

                if self.sent_horiz == self.sentidos["derecha"]:
                    self.sent_horiz = self.sentidos["izquierda"]


                elif self.sent_horiz == self.sentidos["izquierda"]:
                    self.sent_horiz = self.sentidos["derecha"]





            # si se encuentra sin suelo se empieza a caer
            # tambien cae si pisa un paraguas
            elif self.tablero.hayBloqueONo(casilla_debajo[0], casilla_debajo[1]) == 0 or \
                    self.tablero.hayBloqueONo(casilla_debajo[0], casilla_debajo[1]) == 4 and not self.escalera:
                self.sent_vert = self.sentidos["abajo"]
                x_aux += 3
                self.sent_anterior = self.sent_horiz
                self.sent_horiz = self.sentidos["quieto"]
            # si ha llegado a la salida se muere (ATENCION) se deberia hacer que desaparezca y actualizar el contador de forma adecuada
            if casilla_debajo[0] == self.tablero.salida[0] and casilla_debajo[1] == self.tablero.salida[1]:
                self.salvado=True
            # se hace el cambio de verdad
            self.x_actual = x_aux
            self.y_actual = y_aux - 8

        # def haLlegado(self):
