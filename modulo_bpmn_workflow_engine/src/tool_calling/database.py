"""Base de datos SQLite para la demostración de tool calling."""

from __future__ import annotations

import sqlite3
from datetime import date, timedelta
from pathlib import Path


MODULE_ROOT = Path(__file__).resolve().parents[2]
DATA_DIRECTORY = MODULE_ROOT / "data"
DATABASE_PATH = DATA_DIRECTORY / "tool_calling_demo.db"


def get_connection() -> sqlite3.Connection:
    """
    Crea una conexión SQLite configurada para devolver filas por nombre.

    La carpeta data se crea automáticamente cuando todavía no existe.
    """
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(str(DATABASE_PATH))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_schema(connection: sqlite3.Connection) -> None:
    """Crea las tablas utilizadas por las herramientas del sistema."""
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS productos_vencimiento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT NOT NULL,
            tienda TEXT NOT NULL,
            fecha_vencimiento TEXT NOT NULL,
            cantidad INTEGER NOT NULL CHECK (cantidad >= 0),
            precio_actual REAL NOT NULL CHECK (precio_actual >= 0),
            estado TEXT NOT NULL,
            evidencia TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS cambios_precio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            precio_anterior REAL NOT NULL CHECK (precio_anterior >= 0),
            precio_nuevo REAL NOT NULL CHECK (precio_nuevo >= 0),
            estado_aprobacion TEXT NOT NULL,
            solicitado_por TEXT NOT NULL,
            fecha_solicitud TEXT NOT NULL,
            FOREIGN KEY (producto_id)
                REFERENCES productos_vencimiento(id)
        );

        CREATE TABLE IF NOT EXISTS acciones_comerciales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            tipo_accion TEXT NOT NULL,
            estado TEXT NOT NULL,
            responsable TEXT NOT NULL,
            fecha_registro TEXT NOT NULL,
            FOREIGN KEY (producto_id)
                REFERENCES productos_vencimiento(id)
        );
        """
    )


def seed_database(connection: sqlite3.Connection) -> None:
    """
    Inserta datos demostrativos de App Detección Prod.

    Los registros se insertan solamente cuando la tabla principal está vacía.
    """
    total_products = connection.execute(
        "SELECT COUNT(*) FROM productos_vencimiento"
    ).fetchone()[0]

    if total_products > 0:
        return

    today = date.today()

    products = [
        (
            "Yogur natural 1 litro",
            "Supermercado Central - Sala 12",
            (today + timedelta(days=23)).isoformat(),
            24,
            18.50,
            "PENDIENTE",
            "Fotografía del producto y fecha de vencimiento registrada",
        ),
        (
            "Leche deslactosada 1 litro",
            "Supermercado Central - Sala 8",
            (today + timedelta(days=12)).isoformat(),
            15,
            12.00,
            "PENDIENTE",
            "Fotografía frontal y lote del producto",
        ),
        (
            "Queso fresco 500 gramos",
            "Supermercado Central - Sala 4",
            (today + timedelta(days=35)).isoformat(),
            10,
            28.90,
            "PENDIENTE",
            "Fotografía de góndola y fecha de vencimiento",
        ),
        (
            "Arroz premium 1 kilogramo",
            "Supermercado Central - Sala 2",
            (today + timedelta(days=180)).isoformat(),
            40,
            22.00,
            "MONITOREO",
            "Registro de inventario vigente",
        ),
    ]

    connection.executemany(
        """
        INSERT INTO productos_vencimiento (
            producto,
            tienda,
            fecha_vencimiento,
            cantidad,
            precio_actual,
            estado,
            evidencia
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        products,
    )

    product_rows = connection.execute(
        """
        SELECT id, producto
        FROM productos_vencimiento
        """
    ).fetchall()

    product_ids = {
        row["producto"]: row["id"]
        for row in product_rows
    }

    price_changes = [
        (
            product_ids["Yogur natural 1 litro"],
            18.50,
            15.50,
            "PENDIENTE",
            "Vendedor sala 12",
            today.isoformat(),
        ),
        (
            product_ids["Leche deslactosada 1 litro"],
            12.00,
            10.50,
            "APROBADO",
            "Supervisor comercial",
            today.isoformat(),
        ),
    ]

    connection.executemany(
        """
        INSERT INTO cambios_precio (
            producto_id,
            precio_anterior,
            precio_nuevo,
            estado_aprobacion,
            solicitado_por,
            fecha_solicitud
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        price_changes,
    )

    commercial_actions = [
        (
            product_ids["Yogur natural 1 litro"],
            "DESCUENTO",
            "PENDIENTE",
            "Vendedor sala 12",
            today.isoformat(),
        ),
        (
            product_ids["Queso fresco 500 gramos"],
            "BANDEO",
            "PENDIENTE",
            "Supervisor comercial",
            today.isoformat(),
        ),
        (
            product_ids["Leche deslactosada 1 litro"],
            "RETIRO PREVENTIVO",
            "COMPLETADA",
            "Mercaderista sala 8",
            today.isoformat(),
        ),
    ]

    connection.executemany(
        """
        INSERT INTO acciones_comerciales (
            producto_id,
            tipo_accion,
            estado,
            responsable,
            fecha_registro
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        commercial_actions,
    )

    connection.commit()


def initialize_database(reset: bool = False) -> Path:
    """
    Crea la base, sus tablas y los datos de demostración.

    Cuando reset es True, elimina primero la base anterior.
    """
    if reset and DATABASE_PATH.exists():
        DATABASE_PATH.unlink()

    with get_connection() as connection:
        create_schema(connection)
        seed_database(connection)

    return DATABASE_PATH


def table_counts() -> dict[str, int]:
    """Devuelve la cantidad de registros almacenados en cada tabla."""
    tables = (
        "productos_vencimiento",
        "cambios_precio",
        "acciones_comerciales",
    )

    with get_connection() as connection:
        return {
            table: connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]
            for table in tables
        }