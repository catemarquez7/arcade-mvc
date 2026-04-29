from model import JuegoModel
from view import VistaPrincipal
from view.form_juego import FormJuego


class JuegoController:

    def __init__(self, vista: VistaPrincipal, modelo: JuegoModel):
        self.vista = vista
        self.modelo = modelo

        _prev = vista.on_datos_cambiados

        def _hook():
            _prev()
            if vista.vista_juegos is not None:
                self._conectar_vista()
        vista.on_datos_cambiados = _hook

# conexión
    def _conectar_vista(self):
        v = self.vista.vista_juegos

        v.on_nuevo = self.nuevo
        v.on_editar = self.editar
        v.on_eliminar = self.eliminar

        self.cargar_tabla()

# datos
    def cargar_tabla(self):
        v = self.vista.vista_juegos
        if v:
            v.refresh_tabla(self.modelo.listar())

# funciones
    def nuevo(self):
        FormJuego(self.vista, on_guardar=self._guardar_nuevo)

    def editar(self, juego_id: int):
        v = self.vista.vista_juegos

        if not juego_id:
            v.mostrar_aviso("Seleccioná un juego primero.")
            return

        juego = self.modelo.obtener(juego_id)

        if not juego:
            v.mostrar_error("Juego no encontrado.")
            return

        FormJuego(self.vista, juego, self._guardar_editado)

    def eliminar(self, juego_id: int):
        v = self.vista.vista_juegos

        if not juego_id:
            v.mostrar_aviso("Seleccioná un juego primero.")
            return

        if v.confirmar_eliminar(juego_id):
            self.modelo.eliminar(juego_id)
            self.cargar_tabla()
            self.vista.set_status(f"JUEGO #{juego_id} ELIMINADO")

    def _guardar_nuevo(self, datos):
        try:
            anio = int(datos["anio"]) if datos["anio"] else 0
            monedas = int(datos["monedas"]) if datos["monedas"] else 1
        except ValueError:
            self.vista.vista_jugadores.mostrar_error("Score inválido")
            return

        self.modelo.crear({
            "nombre": datos["nombre"],
            "genero": datos["genero"],
            "anio": anio,
            "monedas": monedas,
            "activo": datos["activo"]
        })

        self.cargar_tabla()
        self.vista.set_status("NUEVO JUEGO REGISTRADO")

    def _guardar_editado(self, datos):
        try:
            anio = int(datos["anio"]) if datos["anio"] else 0
            monedas = int(datos["monedas"]) if datos["monedas"] else 1
        except ValueError:
            self.vista.vista_jugadores.mostrar_error("Score inválido")
            return

        self.modelo.actualizar({
            "id": datos["id"],
            "nombre": datos["nombre"],
            "genero": datos["genero"],
            "anio": int(datos["anio"]) if datos["anio"] else 0,
            "monedas": int(datos["monedas"]) if datos["monedas"] else 1,
            "activo": datos["activo"]
        })

        self.cargar_tabla()
        self.vista.set_status(f"JUEGO #{datos['id']} ACTUALIZADO")
