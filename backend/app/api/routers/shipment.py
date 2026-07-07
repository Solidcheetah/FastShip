from typing import Annotated
from uuid import UUID


from fastapi import APIRouter, Form, Request

from fastapi.templating import Jinja2Templates


from app.api.dependencies import (
    DeliveryPartnerDep,
    SellerDep,
    ServiceDep,
    SessionDep,
    UserDep,
)
from app.core.exceptions import NothingToUpdate
from app.api.schemas.shipment import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentUpdate,
)
from app.database.models import Shipment, TagName
from app.utils import TEMPLATE_DIR
from app.config import app_settings


router = APIRouter(prefix="/shipment", tags=["Shipment"])

templates = Jinja2Templates(TEMPLATE_DIR)


@router.get("/", response_model=ShipmentRead)
async def get_shipment(id: UUID, _: UserDep, service: ServiceDep):
    """Fetch a single shipment by id. Available to sellers and delivery partners."""
    return await service.get(id)


@router.get("/track")
async def get_tracking(request: Request, id: UUID, service: ServiceDep):
    shipment = await service.get(id)
    context = shipment.model_dump()
    context["partner"] = shipment.delivery_partner.name
    context["status"] = shipment.status
    context["timeline"] = shipment.timeline
    context["timeline"].reverse()

    return templates.TemplateResponse(
        request=request,
        name="track.html",
        context=context,
    )


@router.post("/", response_model=ShipmentRead)
async def submit_shipment(
    seller: SellerDep,
    shipment: ShipmentCreate,
    service: ServiceDep,
) -> Shipment:
    """Create a new shipment on behalf of the authenticated seller."""
    return await service.add(shipment, seller)


@router.patch("/", response_model=ShipmentRead)
async def patch_shipment(
    id: UUID,
    shipment_update: ShipmentUpdate,
    service: ServiceDep,
    partner: DeliveryPartnerDep,
):
    """Update shipment fields. Restricted to the delivery partner handling it."""
    if not shipment_update.model_dump(exclude_none=True):
        raise NothingToUpdate()

    return await service.update(id, shipment_update, partner)


### Add a tag to shipment
@router.get("/tag", response_model=ShipmentRead)
async def add_tag_to_shipment(
    id: UUID,
    tag_name: TagName,
    service: ServiceDep,
):
    return await service.add_tag(id, tag_name)


### Get all shipments with a tag
@router.get("/tagged", response_model=list[ShipmentRead])
async def get_shipments_with_tag(
    tag_name: TagName,
    session: SessionDep,
):
    tag = await tag_name.tag(session)
    return tag.shipments


### Remove a tag from the shipment
@router.delete("/tag", response_model=ShipmentRead)
async def remove_tag_from_shipment(
    id: UUID,
    tag_name: TagName,
    service: ServiceDep,
):
    return await service.remove_tag(id, tag_name)


# Cancel shipment
@router.get("/cancel", response_model=ShipmentRead)
async def delete_shipment(
    id: UUID,
    seller: SellerDep,
    service: ServiceDep,
):
    """Cancel a shipment. Restricted to the seller who created it."""
    return await service.cancel(id, seller)


# Get review form
@router.get("/review")
async def get_review_form(
    request: Request,
    token: str,
):
    return templates.TemplateResponse(
        request=request,
        name="review.html",
        context={
            "review_url": f"http://{app_settings.APP_DOMAIN}/shipment/review?token={token}"
        },
    )


# Submit a review
@router.post("/review")
async def submit_review(
    token: str,
    rating: Annotated[int, Form(ge=1, le=5)],
    service: ServiceDep,
    comment: Annotated[str | None, Form()] = None,
):
    await service.rate(token, rating, comment)
    return {"detail": "Review submitted"}
