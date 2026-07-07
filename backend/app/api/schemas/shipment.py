from datetime import datetime
from random import randint
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field
from app.database.models import ShipmentEvent, ShipmentStatus, Tag, TagName


def random_destination():
    return randint(11000, 11999)


class BaseShipment(BaseModel):
    content: str = Field(
        description="Describes the content of the shipment", max_length=30
    )
    weight: float = Field(description="Weight of the shipment in kilograms(kg)", le=25)
    destination: int | None = Field(
        description="Destination zipcode, if not provided random zipcode will be generated",
        default_factory=random_destination,
    )


class TagRead(BaseModel):
    name: TagName
    instruction: str


class ShipmentRead(BaseShipment):
    id: UUID
    timeline: list[ShipmentEvent]
    estimated_delivery: datetime
    tags: list[TagRead]


class ShipmentCreate(BaseShipment):
    client_contact_email: EmailStr
    client_contact_phone: str | None = Field(default=None)


class ShipmentUpdate(BaseModel):
    location: int | None = Field(default=None)
    status: ShipmentStatus | None = Field(default=None)
    verification_code: str | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
    description: str | None = Field(default=None)


class ShipmentReview(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None)
