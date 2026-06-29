from pydantic import BaseModel, Field
from datetime import datetime


class ZoneCreate(BaseModel):
    household_id: str
    name: str = Field(min_length=1, max_length=255)
    type: str = "other"
    sort_order: int = 0
    # RF-INV-002: a zone can optionally be linked to a storage unit on
    # creation. The Settings page uses this to nest zones under their
    # refrigerator.
    refrigerator_id: str | None = None


class ZoneUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    sort_order: int | None = None
    refrigerator_id: str | None = None  # explicit "unassign" supported via null


class ZoneResponse(BaseModel):
    id: str
    household_id: str
    name: str
    type: str
    sort_order: int
    refrigerator_id: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
