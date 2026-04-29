from controller import JugadorController, JuegoController, RankingController
from view import VistaPrincipal
from model import init_db, JugadorModel, JuegoModel
import sys
import os


def main():
    init_db()

    vista = VistaPrincipal()

    modelo_jugador = JugadorModel()
    modelo_juego = JuegoModel()

    JugadorController(vista=vista, modelo=modelo_jugador)
    JuegoController(vista=vista,   modelo=modelo_juego)
    RankingController(vista=vista, modelo=modelo_jugador)

    vista.mainloop()


if __name__ == "__main__":
    main()
