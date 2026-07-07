from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import DeliveryPartner, Location, Seller
from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"])

# Matches ShipmentCreate (content, weight, destination + BaseShipment fields)
shipment = {
    "content": "Books",
    "weight": 5.0,
    "destination": 11050,
    "client_contact_email": "client@example.com",
}

# Matches SellerCreate
seller = {
    "name": "Acme Seller",
    "email": "seller@example.com",
    "password": "secret123",
    "address": "123 Market Street",
    "zip_code": 11050,
}

# Matches DeliveryPartnerCreate
delivery_partner = {
    "name": "Fast Delivery Co",
    "email": "partner@example.com",
    "servicable_zip_codes": [11050, 11051, 11052],
    "max_handling_capacity": 100,
    "password": "secret123",
}


async def create_test_db(session: AsyncSession):
    session.add(
        Seller(
            **seller,
            email_verified=True,
            password_hash=password_context.hash(seller["password"]),
        )
    )

    session.add(
        DeliveryPartner(
            **{
                key: value
                for key, value in delivery_partner.items()
                if key != "servicable_zip_codes"
            },
            email_verified=True,
            password_hash=password_context.hash(delivery_partner["password"]),
            servicable_locations=[
                Location(zip_code=zip_code)
                for zip_code in delivery_partner["servicable_zip_codes"]
            ],
        )
    )

    await session.commit()
