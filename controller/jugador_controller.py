from model import JugadorModel
from view import VistaPrincipal
from view.form_jugador import FormJugador


class JugadorController:

    def __init__(self, vista: VistaPrincipal, modelo: JugadorModel):
        self.vista = vista
        self.modelo = modelo

        _prev = vista.on_datos_cambiados

        def _hook():
            _prev()
            if vista.vista_jugadores is not None:
                self._conectar_vista()
        vista.on_datos_cambiados = _hook

# conexion
    def _conectar_vista(self):
        v = self.vista.vista_jugadores

        v.on_nuevo = self.nuevo
        v.on_editar = self.editar
        v.on_eliminar = self.eliminar

        self.cargar_tabla()

# carga datos
    def cargar_tabla(self):
        v = self.vista.vista_jugadores
        if v:
            v.refresh_tabla(self.modelo.listar())

# funciones
    def nuevo(self):
        FormJugador(self.vista, on_guardar=self._guardar_nuevo)

    def editar(self, jugador_id: int):
        v = self.vista.vista_jugadores

        if not jugador_id:
            v.mostrar_aviso("Seleccioná un jugador primero.")
            return

        jugador = self.modelo.obtener(jugador_id)

        if not jugador:
            v.mostrar_error("Jugador no encontrado.")
            return

        FormJugador(self.vista, jugador, self._guardar_editado)

    def eliminar(self, jugador_id: int):
        v = self.vista.vista_jugadores

        if not jugador_id:
            v.mostrar_aviso("Seleccioná un jugador primero.")
            return

        if v.confirmar_eliminar(jugador_id):
            self.modelo.eliminar(jugador_id)
            self.cargar_tabla()
            self.vista.set_status(f"JUGADOR #{jugador_id} ELIMINADO")

    def _guardar_nuevo(self, datos):
        self.modelo.crear({
            "nombre": datos["nombre"],
            "email": datos["email"],
        })

        self.cargar_tabla()
        self.vista.set_status("NUEVO JUGADOR REGISTRADO")

    def _guardar_editado(self, datos):

        self.modelo.actualizar({
            "id": datos["id"],
            "nombre": datos["nombre"],
            "email": datos["email"],
        })

        self.cargar_tabla()
