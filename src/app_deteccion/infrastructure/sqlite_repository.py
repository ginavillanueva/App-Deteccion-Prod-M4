from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from datetime import date
from pathlib import Path

from app_deteccion.domain.entities import CriticalProductCase, PriceAudit
from app_deteccion.domain.enums import CaseStatus, CommercialAction
from app_deteccion.domain.events import DomainEvent


class SQLiteCaseRepository:
    """Tiny SQLite adapter for demo persistence.

    It is intentionally simple. The production DTI can evolve this adapter to Postgres/RDS.
    """

    def __init__(self, db_path: str = "app_deteccion_demo.db") -> None:
        self.db_path = db_path
        self._init_schema()

    def _connect(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True) if "/" in self.db_path else None
        return sqlite3.connect(self.db_path)

    def _init_schema(self) -> None:
        with closing(self._connect()) as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS cases (
                    id TEXT PRIMARY KEY,
                    payload TEXT NOT NULL
                )
                """
            )
            con.commit()

    def add(self, case: CriticalProductCase) -> CriticalProductCase:
        with closing(self._connect()) as con:
            con.execute(
                "INSERT OR REPLACE INTO cases (id, payload) VALUES (?, ?)",
                (case.id, json.dumps(case.to_dict(), ensure_ascii=False)),
            )
            con.commit()
        return case

    def update(self, case: CriticalProductCase) -> CriticalProductCase:
        return self.add(case)

    def get(self, case_id: str) -> CriticalProductCase | None:
        with closing(self._connect()) as con:
            row = con.execute("SELECT payload FROM cases WHERE id = ?", (case_id,)).fetchone()
        if row is None:
            return None
        return self._from_payload(json.loads(row[0]))

    def list_all(self) -> list[CriticalProductCase]:
        with closing(self._connect()) as con:
            rows = con.execute("SELECT payload FROM cases ORDER BY rowid").fetchall()
        return [self._from_payload(json.loads(row[0])) for row in rows]

    def clear(self) -> None:
        with closing(self._connect()) as con:
            con.execute("DELETE FROM cases")
            con.commit()

    @staticmethod
    def _from_payload(data: dict) -> CriticalProductCase:
        price = data["price_audit"]
        case = CriticalProductCase(
            id=data["id"],
            store=data["store"],
            product_name=data["product_name"],
            batch=data["batch"],
            expiration_date=date.fromisoformat(data["expiration_date"]),
            quantity=data["quantity"],
            commercial_action=CommercialAction(data["commercial_action"]),
            price_audit=PriceAudit(
                current_price=price["current_price"],
                new_price=price["new_price"],
                price_change_approved=price["price_change_approved"],
                price_change_reason=price.get("price_change_reason", ""),
            ),
            evidence_note=data.get("evidence_note", ""),
            created_by=data.get("created_by", "mercaderista.demo"),
            created_at=date.fromisoformat(data["created_at"]),
        )
        case.status = CaseStatus(data.get("status", "REGISTRADO"))
        case.validated_by = data.get("validated_by")
        return case


class SQLiteEventPublisher:
    def __init__(self, db_path: str = "app_deteccion_demo.db") -> None:
        self.db_path = db_path
        self._init_schema()

    def _connect(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True) if "/" in self.db_path else None
        return sqlite3.connect(self.db_path)

    def _init_schema(self) -> None:
        with closing(self._connect()) as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS outbox_events (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    aggregate_id TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    occurred_at TEXT NOT NULL
                )
                """
            )
            con.commit()

    def publish_many(self, events: list[DomainEvent]) -> None:
        with closing(self._connect()) as con:
            con.executemany(
                "INSERT OR REPLACE INTO outbox_events (id, name, aggregate_id, payload, occurred_at) VALUES (?, ?, ?, ?, ?)",
                [
                    (
                        event.id,
                        event.name,
                        event.aggregate_id,
                        json.dumps(event.payload, ensure_ascii=False),
                        event.occurred_at.isoformat(),
                    )
                    for event in events
                ],
            )
            con.commit()

    def list_all(self) -> list[DomainEvent]:
        with closing(self._connect()) as con:
            rows = con.execute(
                "SELECT id, name, aggregate_id, payload, occurred_at FROM outbox_events ORDER BY rowid"
            ).fetchall()
        # For dashboard we only need count/list shape; payload date rehydration is not necessary.
        return [
            DomainEvent(name=row[1], aggregate_id=row[2], payload=json.loads(row[3]), id=row[0])
            for row in rows
        ]

    def clear(self) -> None:
        with closing(self._connect()) as con:
            con.execute("DELETE FROM outbox_events")
            con.commit()
