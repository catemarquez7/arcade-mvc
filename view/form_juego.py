import tkinter as tk
from .theme import (
    BG, NEON_PINK, NEON_GREEN,
    NeonEntry, neon_button
)


class FormJuego(tk.Toplevel):

    def __init__(self, parent, juego=None, on_guardar=None):
        super().__init__(parent)

        self.title("JUEGO")
        self.configure(bg=BG)
        self.resizable(False, False)

        self.on_guardar = on_guardar
        self.juego_id = juego["id"] if juego else None

        # inputs
        self.f_nombre = NeonEntry(self, "NOMBRE")
        self.f_genero = NeonEntry(self, "GÉNERO")
        self.f_anio = NeonEntry(self, "AÑO")
        self.f_monedas = NeonEntry(self, "MONEDAS")

        for w in [self.f_nombre, self.f_genero, self.f_anio, self.f_monedas]:
            w.pack(padx=12, pady=5)

        # on / off
        self.f_activo = tk.BooleanVar(value=True)
        tk.Checkbutton(
            self,
            text="ONLINE",
            variable=self.f_activo,
            bg=BG,
            fg=NEON_PINK,
            selectcolor=BG,
            activebackground=BG,
            activeforeground=NEON_PINK,
            cursor="hand2"
        ).pack(pady=5)

        # carga datos si es edición
        if juego:
            self.f_nombre.set(juego["nombre"])
            self.f_genero.set(juego["genero"])
            self.f_anio.set(str(juego["anio"]))
            self.f_monedas.set(str(juego["monedas"]))
            self.f_activo.set(juego["activo"])

        neon_button(self, "GUARDAR", NEON_GREEN,
                    self._guardar).pack(pady=10)

    def _guardar(self):
        datos = {
            "id": self.juego_id,
            "nombre": self.f_nombre.get(),
            "genero": self.f_genero.get(),
            "anio": self.f_anio.get(),
            "monedas": self.f_monedas.get(),
            "activo": self.f_activo.get()
        }

        self.destroy()

        if self.on_guardar:
            self.on_guardar(datos)
