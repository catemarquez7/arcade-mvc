import tkinter as tk
from tkinter import ttk, messagebox
from .theme import (
    BG, BG2, NEON_CYAN, NEON_GREEN,
    DIM, DANGER,
    neon_button, separator, apply_treeview_style,
)


class VistaJugadores(tk.Frame):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=BG, **kwargs)

        # callbacks
        self.on_nuevo = lambda: None
        self.on_editar = lambda jugador_id: None
        self.on_eliminar = lambda jugador_id: None

        apply_treeview_style()
        self._build()

# vistas
    def _build(self):
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", pady=(0, 4))

        tk.Label(
            top,
            text="JUGADORES",
            bg=BG,
            fg=NEON_CYAN,
            font=("Courier New", 18, "bold")
        ).pack(side="left")

        # botones
        neon_button(top, "NUEVO", NEON_GREEN,
                    lambda: self.on_nuevo()).pack(side="right", padx=2)

        neon_button(top, "EDITAR", NEON_CYAN,
                    self._editar_click).pack(side="right", padx=2)

        neon_button(top, "ELIMINAR", DANGER,
                    self._eliminar_click).pack(side="right", padx=2)

        separator(self, NEON_CYAN).pack(fill="x", pady=4)

        self._build_tabla()

    def _build_tabla(self):
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True)

        cols = ("ID", "NOMBRE", "EMAIL", "SCORE")

        self.tree = ttk.Treeview(
            container,
            columns=cols,
            show="headings",
            style="Neon.Treeview",
            selectmode="browse"
        )

        widths = [50, 200, 250, 100]

        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        scroll = tk.Scrollbar(
            container,
            orient="vertical",
            command=self.tree.yview,
            bg=BG2
        )

        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

# selección de jugador para editar / eliminar
    def _editar_click(self):
        sel = self.tree.selection()
        if sel:
            self.on_editar(int(sel[0]))
        else:
            self.mostrar_aviso("Seleccioná un jugador primero.")

    def _eliminar_click(self):
        sel = self.tree.selection()
        if sel:
            self.on_eliminar(int(sel[0]))
        else:
            self.mostrar_aviso("Seleccioná un jugador primero.")

# vuelven datos del controller
    def refresh_tabla(self, jugadores: list):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for j in jugadores:
            self.tree.insert(
                "",
                "end",
                iid=j["id"],
                values=(
                    j["id"],
                    j["nombre"],
                    j["email"],
                    j["score"]
                )
            )

    def confirmar_eliminar(self, jugador_id):
        return messagebox.askyesno(
            "CONFIRM",
            f"¿Eliminar jugador #{jugador_id}?",
            parent=self
        )

    def mostrar_error(self, msg):
        messagebox.showerror("ERROR", msg, parent=self)

    def mostrar_aviso(self, msg):
        messagebox.showwarning("AVISO", msg, parent=self)
