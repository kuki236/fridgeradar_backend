from sqlalchemy.orm import Session

from app.models import Zone


class ZoneRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_household(self, household_id: str) -> list[Zone]:
        return (
            self.db.query(Zone)
            .filter(Zone.household_id == household_id)
            .order_by(Zone.sort_order)
            .all()
        )

    def get_by_id(self, zone_id: str) -> Zone | None:
        return self.db.query(Zone).filter(Zone.id == zone_id).first()

    def create(
        self,
        household_id: str,
        name: str,
        type: str,
        sort_order: int,
        refrigerator_id: str | None = None,
    ) -> Zone:
        zone = Zone(
            household_id=household_id,
            name=name,
            type=type,
            sort_order=sort_order,
            refrigerator_id=refrigerator_id,
        )
        self.db.add(zone)
        self.db.commit()
        self.db.refresh(zone)
        return zone

    def update(
        self,
        zone: Zone,
        name: str | None,
        type: str | None,
        sort_order: int | None,
        refrigerator_id: str | None = None,
    ) -> Zone:
        if name is not None:
            zone.name = name
        if type is not None:
            zone.type = type
        if sort_order is not None:
            zone.sort_order = sort_order
        # Only assign to a fridge; explicit unassigns happen via the FK
        # cascade when a refrigerator is deleted (SET NULL).
        if refrigerator_id is not None:
            zone.refrigerator_id = refrigerator_id
        self.db.commit()
        self.db.refresh(zone)
        return zone

    def delete(self, zone: Zone) -> None:
        self.db.delete(zone)
        self.db.commit()
