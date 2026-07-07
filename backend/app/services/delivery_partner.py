from typing import Sequence

from sqlmodel import select, any_

from app.api.schemas.delivery_partner import DeliveryPartnerCreate
from app.core.exceptions import DeliveryPartnerNotAvailable
from app.database.models import DeliveryPartner, Location, Shipment
from app.services.user import UserService


class DeliveryPartnerService(UserService):
    def __init__(self, session):
        super().__init__(DeliveryPartner, session)

    async def add(self, delivery_partner: DeliveryPartnerCreate):
        partner = await self._add_user(
            delivery_partner.model_dump(exclude={"servicable_zip_codes"}),
            "partner",
        )

        for zip_code in delivery_partner.servicable_zip_codes:
            location = await self.session.get(Location, zip_code)
            partner.servicable_locations.append(
                location if location else Location(zip_code=zip_code)
            )

        return await self._update(partner)

    async def update(self, partner: DeliveryPartner):
        return await self._update(partner)

    async def get_partner_by_zipcode(self, zipcode: int) -> Sequence[DeliveryPartner]:
        result = await self.session.scalars(
            select(DeliveryPartner)
            .join(DeliveryPartner.servicable_locations)
            .where(Location.zip_code == zipcode)
        )
        return result.all()

    async def assign_shipment(self, shipment: Shipment):
        eligible_partner = await self.get_partner_by_zipcode(shipment.destination)

        for partner in eligible_partner:
            if partner.current_handling_capacity > 0:
                partner.shipments.append(shipment)
                return partner

        raise DeliveryPartnerNotAvailable()

    async def login(self, email, password):
        return await self._generate_token(email, password)
