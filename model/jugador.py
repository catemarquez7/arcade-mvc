from dataclasses import dataclass
from typing import Optional
from .database import get_conn


class JugadorModel:

    def listar(self, filtro: str = "") -> list[dict]:
        with get_conn() as conn:
            if filtro:
                f = f"%{filtro}%"
                rows = conn.execute(
                    """
                    SELECT id, nombre, email, score_max as score
                    FROM jugadores
                    WHERE nombre LIKE ? OR email LIKE ?
                    ORDER BY score_max DESC
                    """,
                    (f, f),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT id, nombre, email, score_max as score
                    FROM jugadores
                    ORDER BY score_max DESC
                    """
                ).fetchall()

        return [dict(r) for r in rows]

    def obtener(self, id_: int) -> Optional[dict]:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT * FROM jugadores WHERE id=?", (id_,)
            ).fetchone()

        return dict(row) if row else None

    def crear(self, j) -> int:
        with get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO jugadores (nombre, email, score_max) VALUES (?,?,?)",
                (
                    j["nombre"] if isinstance(j, dict) else j.nombre,
                    j["email"] if isinstance(j, dict) else j.email,
                    0
                ),
            )
            return cur.lastrowid

    def actualizar(self, j) -> None:
        with get_conn() as conn:
            if isinstance(j, dict):
                conn.execute(
                    "UPDATE jugadores SET nombre=?, email=? WHERE id=?",
                    (j["nombre"], j["email"], j["id"]),
                )
            else:
                if j.id is None:
                    raise ValueError(
                        "No se puede actualizar un Jugador sin id.")
                conn.execute(
                    "UPDATE jugadores SET nombre=?, email=? WHERE id=?",
                    (j.nombre, j.email, j.id),
                )

    def eliminar(self, id_: int) -> None:
        with get_conn() as conn:
            conn.execute("DELETE FROM jugadores WHERE id=?", (id_,))

    def ranking_por_juego(self, id_juego: int) -> list[dict]:
        with get_conn() as conn:
            cur = conn.execute("""
                SELECT j.id, j.nombre, MAX(p.score) as score
                FROM jugadores j
                JOIN partidas p ON j.id = p.fk_jugador
                WHERE p.fk_juego = ?
                GROUP BY j.id, j.nombre
                ORDER BY score DESC
                """, (id_juego,))
        return [dict(row) for row in cur.fetchall()]
