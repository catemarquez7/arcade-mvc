import tkinter as tk
from .theme import (
    BG, NEON_CYAN, NEON_GREEN,
    NeonEntry, neon_button
)


class FormJugador(tk.Toplevel):

    def __init__(self, parent, jugador=None, on_guardar=None):
        super().__init__(parent)

        self.title("JUGADOR")
        self.configure(bg=BG)
        self.resizable(False, False)

        self.on_guardar = on_guardar
        self.jugador_id = jugador["id"] if jugador else None

        # inputs
        self.f_nombre = NeonEntry(self, "NOMBRE")
        self.f_email = NeonEntry(self, "EMAIL")

        for w in [self.f_nombre, self.f_email]:
            w.pack(padx=12, pady=5)

        # carga datos si es edición
        if jugador:
            self.f_nombre.set(jugador["nombre"])
            self.f_email.set(jugador["email"])

        neon_button(self, "GUARDAR", NEON_GREEN,
                    self._guardar).pack(pady=10)

    def _guardar(self):
        datos = {
            "id": self.jugador_id,
            "nombre": self.f_nombre.get(),
            "email": self.f_email.get(),
        }

        self.destroy()

        if self.on_guardar:
            self.on_guardar(datos)
