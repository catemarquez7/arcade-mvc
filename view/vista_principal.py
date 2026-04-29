import tkinter as tk

from .theme import (
    BG, BG2, BG3,
    NEON_CYAN, NEON_PINK, NEON_YELLOW, NEON_GREEN,
    DIM, TEXT, TEXT_DIM,
    FONT_TITLE, FONT_BODY, FONT_SMALL, FONT_MONO, FONT_SUB,
    neon_button, separator,
)
from .vista_jugadores import VistaJugadores
from .vista_juegos import VistaJuegos
from .vista_ranking import VistaRanking


class VistaPrincipal(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("ARCADE MANAGER")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(bg=BG)
        self.resizable(True, True)

    # referencias a vistas activas
        self.vista_jugadores: VistaJugadores | None = None
        self.vista_juegos:    VistaJuegos | None = None
        self.vista_ranking: VistaRanking | None = None
        self.on_datos_cambiados = lambda: None

        self._build_header()
        self._build_nav()
        self._build_content()
        self.show_inicio()

# arranca

    def _build_header(self):
        hdr = tk.Frame(self, bg=BG, pady=8)
        hdr.pack(fill="x", padx=20, pady=(12, 0))

        tk.Label(hdr, text="Arcade Manager", bg=BG, fg=NEON_CYAN,
                 font=FONT_TITLE).pack(side="left")

    def _build_nav(self):
        separator(self, NEON_CYAN).pack(fill="x", padx=0, pady=(8, 0))

        nav = tk.Frame(self, bg=BG)
        nav.pack(fill="x", padx=20, pady=6)

        self._nav_btns = {}
        items = [
            ("INICIO",    self.show_inicio),
            ("JUGADORES", self.show_jugadores),
            ("JUEGOS",    self.show_juegos),
            ("RANKING",   self.show_ranking),
        ]
        for label, cmd in items:
            btn = tk.Button(
                nav, text=label,
                command=lambda c=cmd, l=label: self._nav_click(c, l),
                bg=BG, fg=TEXT_DIM, font=FONT_BODY, relief="flat", bd=0,
                cursor="hand2", padx=16, pady=4,
                activebackground=BG, activeforeground=NEON_CYAN,
            )
            btn.pack(side="left", padx=2)
            self._nav_btns[label] = btn

        separator(self, DIM).pack(fill="x", padx=0)

    def _nav_click(self, cmd, label):
        for lbl, btn in self._nav_btns.items():
            btn.config(fg=NEON_CYAN if lbl == label else TEXT_DIM)
        cmd()

    def _build_content(self):
        self._content = tk.Frame(self, bg=BG)
        self._content.pack(fill="both", expand=True, padx=20, pady=10)

    def _clear_content(self):
        for w in self._content.winfo_children():
            w.destroy()
        self.vista_jugadores = None
        self.vista_juegos = None
        self.vista_ranking = None

# vistas

    def show_inicio(self):
        self._clear_content()

        tk.Label(self._content, text="", bg=BG).pack(pady=40)

        tk.Label(
            self._content,
            text="Bienvenido al sistema.",
            bg=BG, fg=NEON_CYAN,
            font=FONT_TITLE,
        ).pack()

        tk.Label(
            self._content,
            text="GESTIÓN DE ARCADE",
            bg=BG, fg=NEON_PINK,
            font=FONT_SUB,
        ).pack()

        separator(self._content, DIM).pack(fill="x", pady=(0, 30))

        tk.Label(
            self._content,
            text="Seleccione una opción para continuar.",
            bg=BG, fg=TEXT_DIM,
            font=FONT_BODY,
        ).pack()

    def show_jugadores(self):
        # crea vista, la muestra y avisa a los controllers
        self._clear_content()
        self.vista_jugadores = VistaJugadores(self._content)
        self.vista_jugadores.pack(fill="both", expand=True)
        self.on_datos_cambiados()

    def show_juegos(self):
        self._clear_content()
        self.vista_juegos = VistaJuegos(self._content)
        self.vista_juegos.pack(fill="both", expand=True)
        self.on_datos_cambiados()

    def show_ranking(self):
        self._clear_content()
        self.vista_ranking = VistaRanking(self._content)
        self.vista_ranking.pack(fill="both", expand=True)
        self.on_datos_cambiados()

    def set_status(self, texto):
        print(texto)
