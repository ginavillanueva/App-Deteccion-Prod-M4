
from datetime import date, timedelta

from app_deteccion.domain.entities import CriticalProductCase, PriceAudit
from app_deteccion.domain.enums import CommercialAction
from app_deteccion.infrastructure.sqlite_repository import SQLiteCaseRepository, SQLiteEventPublisher


def make_case():
    return CriticalProductCase(
        store="Tienda SQLite",
        product_name="Producto SQLite",
        batch="SQL-1",
        expiration_date=date.today() + timedelta(days=30),
        quantity=3,
        commercial_action=CommercialAction.DESCUENTO,
        price_audit=PriceAudit(current_price=10.0, new_price=8.0, price_change_approved=True),
        evidence_note="Foto clara",
        created_by="mercaderista.sqlite",
    )


def test_sqlite_repository_add_get_update_list_and_clear(tmp_path):
    db = tmp_path / "demo.db"
    repo = SQLiteCaseRepository(str(db))
    case = make_case()
    repo.add(case)
    loaded = repo.get(case.id)
    assert loaded is not None
    assert loaded.product_name == "Producto SQLite"
    assert loaded.price_audit.new_price == 8.0
    loaded.validate_by_supervisor("supervisor.sqlite")
    repo.update(loaded)
    assert repo.get(case.id).validated_by == "supervisor.sqlite"
    assert len(repo.list_all()) == 1
    assert repo.get("missing") is None
    repo.clear()
    assert repo.list_all() == []


def test_sqlite_event_publisher_publish_list_and_clear(tmp_path):
    db = tmp_path / "events.db"
    publisher = SQLiteEventPublisher(str(db))
    case = make_case()
    publisher.publish_many(case.events)
    events = publisher.list_all()
    assert len(events) == 3
    assert events[0].name == "ProductCaseRegistered.v1"
    publisher.clear()
    assert publisher.list_all() == []
