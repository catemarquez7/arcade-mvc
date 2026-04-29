import tkinter as tk
from tkinter import ttk
from .theme import (
    BG, BG2, NEON_YELLOW,
    DIM,
    neon_button, separator, apply_treeview_style
)


class VistaRanking(tk.Frame):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=BG, **kwargs)

        apply_treeview_style()
        self._build()

    def _build(self):
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", pady=(0, 4))

        tk.Label(
            top,
            text="RANKING PAC-MAN",
            bg=BG,
            fg=NEON_YELLOW,
            font=("Courier", 18, "bold")
        ).pack(side="left")

        separator(self, NEON_YELLOW).pack(fill="x", pady=4)

        self._build_tabla()

    def _build_tabla(self):
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True)
        frame = tk.Frame(
            container,
            bg=BG2,
            highlightthickness=1,
            highlightbackground=DIM
        )
        frame.pack(fill="both", expand=True)

        cols = ("POS", "NOMBRE", "SCORE")

        self.tree = ttk.Treeview(
            frame,
            columns=cols,
            show="headings",
            style="Neon.Treeview",
            selectmode="browse"
        )

        widths = [60, 250, 120]

        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        scroll = tk.Scrollbar(
            frame,
            orient="vertical",
            command=self.tree.yview,
            bg=BG2
        )

        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def refresh_tabla(self, jugadores: list):
        for row in self.tree.get_children():
            self.tree.delete(row)

        jugadores = sorted(jugadores, key=lambda x: x["score"], reverse=True)

        for i, j in enumerate(jugadores, start=1):
            self.tree.insert(
                "",
                "end",
                iid=j["id"],
                values=(i, j["nombre"], j["score"])
            )
