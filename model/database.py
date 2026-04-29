import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "arcade.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS jugadores (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre  TEXT    NOT NULL,
                email   TEXT,
                score_max   INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS juegos (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre   TEXT    NOT NULL,
                anio     INTEGER,
                genero   TEXT, 
                monedas  INTEGER DEFAULT 1,
                activo   INTEGER DEFAULT 1
            );
            
            CREATE TABLE IF NOT EXISTS partidas (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                fk_jugador  INTEGER NOT NULL,
                fk_juego    INTEGER NOT NULL,
                score       INTEGER NOT NULL,
                fecha       TEXT,
                FOREIGN KEY (fk_jugador) REFERENCES jugadores(id),
                FOREIGN KEY (fk_juego) REFERENCES juegos(id)
);
            
        """)
        _seed(conn)


def _seed(conn):
    if conn.execute("SELECT COUNT(*) FROM jugadores").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO jugadores (nombre, email, score_max) VALUES (?,?,?)",
            [
                ("vickyycm", "vicky@arcade.com", 98500),
                ("cate", "yo@arcade.com", 65200),
                ("nicolino", "nico@arcade.com", 71000),
                ("ojotac", "cams@arcade.com", 44800),
                ("catafig", "cats@arcade.com", 43300),
            ],
        )

    if conn.execute("SELECT COUNT(*) FROM juegos").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO juegos (nombre, anio, genero, monedas, activo) VALUES (?,?,?,?,?)",
            [
                ("Space Invaders", 1978, "Arcade Shooter", 1, 1),
                ("PAC-MAN", 1980, "Maze Chase", 1, 1),
                ("Frogger", 1981, "Crossing Game", 1, 1),
                ("Donkey Kong", 1981, "Platform", 2, 1),
                ("Street Fighter", 1987, "Fighting Game", 2, 0),
            ],
        )

    if conn.execute("SELECT COUNT(*) FROM partidas").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO partidas (fk_jugador, fk_juego, score, fecha) VALUES (?,?,?,?)",
            [
                # juego 2 (PAC-MAN)
                (1, 2, 55000, "2026-01-01"),
                (1, 2, 62000, "2026-01-02"),
                (2, 2, 48000, "2026-01-01"),
                (3, 2, 35000, "2026-01-03"),
                (4, 2, 57000, "2026-01-01"),
                (5, 2, 79000, "2026-01-02"),

                # otras partidas
                (1, 1, 24000, "2026-01-01"),
                (2, 1, 33000, "2026-01-02"),
                (3, 3, 54000, "2026-01-02"),
                (4, 4, 16000, "2026-01-03"),
                (5, 1, 22500, "2026-01-04"),
            ],
        )

    conn.commit()
