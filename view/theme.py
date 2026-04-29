import tkinter as tk
from tkinter import ttk

BG = "#0a0a0f"
BG2 = "#12121a"
BG3 = "#1a1a28"
NEON_CYAN = "#00f5ff"
NEON_PINK = "#ff00aa"
NEON_YELLOW = "#ffee00"
NEON_GREEN = "#39ff14"
DIM = "#3a3a5c"
TEXT = "#e0e0ff"
TEXT_DIM = "#7070a0"
DANGER = "#ff4466"

FONT_TITLE = ("Segoe UI", 28, "bold")
FONT_SUB = ("Segoe UI", 13, "bold")
FONT_BODY = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 9)
FONT_MONO = ("Segoe UI", 12)


def neon_button(parent, text, color, command, width=18):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=BG,
        fg=color,
        activebackground=BG,
        activeforeground=color,
        font=FONT_BODY,
        relief="flat",
        bd=0,
        width=width,
        cursor="hand2",
        pady=7,
        highlightthickness=1,
        highlightbackground=color,
        highlightcolor=color,
        borderwidth=0,
    )


def separator(parent, color=DIM):
    return tk.Frame(parent, bg=color, height=1)


def apply_treeview_style():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Neon.Treeview",
        background=BG2, foreground=TEXT,
        fieldbackground=BG2, rowheight=28,
        font=("Courier New", 10),
    )
    style.configure(
        "Neon.Treeview.Heading",
        background=BG3, foreground=NEON_CYAN,
        font=("Courier New", 10, "bold"), relief="flat",
    )
    style.map(
        "Neon.Treeview",
        background=[("selected", BG3)],
        foreground=[("selected", NEON_CYAN)],
    )


class NeonEntry(tk.Frame):
    """Label + Entry con estética neon."""

    def __init__(self, parent, label, width=22, **kwargs):
        super().__init__(parent, bg=BG2, **kwargs)
        tk.Label(self, text=label, bg=BG2, fg=TEXT_DIM,
                 font=FONT_SMALL).pack(anchor="w")
        self.var = tk.StringVar()
        self.entry = tk.Entry(
            self, textvariable=self.var,
            bg=BG3, fg=NEON_CYAN, insertbackground=NEON_CYAN,
            font=FONT_MONO, relief="flat", bd=0, width=width,
            highlightthickness=1, highlightbackground=DIM,
            highlightcolor=NEON_CYAN,
        )
        self.entry.pack(fill="x", ipady=5, padx=1)

    def get(self):
        return self.var.get()

    def set(self, val):
        self.var.set(val)

    def clear(self):
        self.var.set("")
