from dataclasses import dataclass
from typing import Optional
from .database import get_conn


class JuegoModel:

    def listar(self, filtro: str = "") -> list[dict]:
        with get_conn() as conn:
            if filtro:
                f = f"%{filtro}%"
                rows = conn.execute(
                    """SELECT * FROM juegos
                    WHERE nombre LIKE ? OR genero LIKE ?
                    ORDER BY nombre""",
                    (f, f),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM juegos ORDER BY nombre"
                ).fetchall()

        return [dict(r) for r in rows]

    def obtener(self, id_: int) -> Optional[dict]:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT * FROM juegos WHERE id=?",
                (id_,)
            ).fetchone()

        return dict(row) if row else None

    def crear(self, j) -> int:
        with get_conn() as conn:
            cur = conn.execute(
                """INSERT INTO juegos (nombre, genero, anio, monedas, activo)
                   VALUES (?,?,?,?,?)""",
                (
                    j["nombre"] if isinstance(j, dict) else j.nombre,
                    j["genero"] if isinstance(j, dict) else j.genero,
                    j["anio"] if isinstance(j, dict) else j.anio,
                    j["monedas"] if isinstance(j, dict) else j.monedas,
                    int(j["activo"] if isinstance(j, dict) else j.activo),
                ),
            )
            return cur.lastrowid

    def actualizar(self, j) -> None:
        with get_conn() as conn:
            if isinstance(j, dict):
                conn.execute(
                    """UPDATE juegos
                       SET nombre=?, genero=?, anio=?, monedas=?, activo=?
                       WHERE id=?""",
                    (
                        j["nombre"],
                        j["genero"],
                        j["anio"],
                        j["monedas"],
                        int(j["activo"]),
                        j["id"],
                    ),
                )
            else:
                if j.id is None:
                    raise ValueError("No se puede actualizar un Juego sin id.")
                conn.execute(
                    """UPDATE juegos
                       SET nombre=?, genero=?, anio=?, monedas=?, activo=?
                       WHERE id=?""",
                    (*j.as_tuple(), j.id),
                )

    def eliminar(self, id_: int) -> None:
        with get_conn() as conn:
            conn.execute(
                "DELETE FROM juegos WHERE id=?",
                (id_,)
            )
