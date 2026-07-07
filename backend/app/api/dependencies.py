from typing import Annotated
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.exceptions import ClientNotAuthorized, InvalidToken
from app.database.models import DeliveryPartner, Seller
from app.database.redis import is_jti_blacklisted
from app.database.session import get_session
from app.services.delivery_partner import DeliveryPartnerService
from app.services.seller import SellerService
from app.services.shipment import ShipmentService
from app.core.security import oauth2_scheme, oauth2_scheme_partner
from app.services.shipment_event import ShipmentEventService
from app.utils import decode_access_token


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def _get_access_token(token: str) -> dict:
    data = decode_access_token(token)

    if data is None or await is_jti_blacklisted(data["jti"]):
        raise InvalidToken()

    return data


async def get_seller_access_token(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> dict:
    return await _get_access_token(token)


async def get_partner_access_token(
    token: Annotated[str, Depends(oauth2_scheme_partner)],
) -> dict:
    return await _get_access_token(token)


async def get_current_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token)], session: SessionDep
):
    seller = await session.get(Seller, UUID(token_data["user"]["id"]))
    if seller is None:
        raise ClientNotAuthorized()
    return seller


async def get_current_partner(
    token_data: Annotated[dict, Depends(get_partner_access_token)], session: SessionDep
):
    partner = await session.get(DeliveryPartner, UUID(token_data["user"]["id"]))
    if partner is None:
        raise ClientNotAuthorized()
    return partner


async def get_current_user(
    token_data: Annotated[dict, Depends(get_seller_access_token)], session: SessionDep
) -> Seller | DeliveryPartner:
    """Authenticate the caller as either a seller or a delivery partner.

    Both token types carry the same ``{"user": {"id": ...}}`` payload and are
    sent as a bearer token, so we resolve the id against either table.
    """
    user_id = UUID(token_data["user"]["id"])
    user = await session.get(Seller, user_id) or await session.get(
        DeliveryPartner, user_id
    )
    if user is None:
        raise ClientNotAuthorized()
    return user


def get_shipment_service(
    session: SessionDep,
):
    return ShipmentService(
        session,
        DeliveryPartnerService(session),
        ShipmentEventService(session),
    )


def get_seller_service(session: SessionDep):
    return SellerService(session)


def get_partner_service(session: SessionDep):
    return DeliveryPartnerService(session)


ServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]

SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]

SellerDep = Annotated[Seller, Depends(get_current_seller)]

DeliveryPartnerDep = Annotated[DeliveryPartner, Depends(get_current_partner)]

UserDep = Annotated[Seller | DeliveryPartner, Depends(get_current_user)]

DeliveryPartnerServiceDep = Annotated[
    DeliveryPartnerService, Depends(get_partner_service)
]
