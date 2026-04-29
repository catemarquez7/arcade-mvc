from view import VistaPrincipal


class RankingController:

    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo

        _prev = vista.on_datos_cambiados

        def _hook():
            _prev()
            if vista.vista_ranking is not None:
                self.cargar()

        vista.on_datos_cambiados = _hook

    # carga datos

    def cargar(self):
        # harcodeado al juego 2
        jugadores = self.modelo.ranking_por_juego(2)
        if self.vista.vista_ranking:
            self.vista.vista_ranking.refresh_tabla(jugadores)
