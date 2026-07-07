from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

from app.api.dependencies import (
    DeliveryPartnerDep,
    DeliveryPartnerServiceDep,
    get_partner_access_token,
)
from app.config import app_settings
from app.core.exceptions import NothingToUpdate
from app.core.security import TokenData
from app.database.redis import add_jti_to_blacklist
from app.utils import TEMPLATE_DIR

from ..schemas.delivery_partner import (
    DeliveryPartnerCreate,
    DeliveryPartnerRead,
    DeliveryPartnerUpdate,
)
from ..schemas.shipment import ShipmentRead

router = APIRouter(prefix="/partner", tags=["Delivery Partner"])


### Register a delivery partner
@router.post("/signup", response_model=DeliveryPartnerRead)
async def register_delivery_partner(
    partner: DeliveryPartnerCreate,
    service: DeliveryPartnerServiceDep,
):
    return await service.add(partner)


### Login the delivery partner
@router.post("/login", response_model=TokenData)
async def login_delivery_partner(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: DeliveryPartnerServiceDep,
):
    token = await service.login(request_form.username, request_form.password)
    return {"access_token": token, "token_type": "jwt"}


@router.post("/update", response_model=DeliveryPartnerRead)
async def update_delivery_partner(
    partner_update: DeliveryPartnerUpdate,
    partner: DeliveryPartnerDep,
    service: DeliveryPartnerServiceDep,
):
    update = partner_update.model_dump(exclude_none=True)
    if not update:
        raise NothingToUpdate()
    return await service.update(partner.sqlmodel_update(update))


### Verify Delivery Partner Email
@router.get("/verify")
async def verify_delivery_partner_email(
    token: str,
    service: DeliveryPartnerServiceDep,
):
    await service.verify_email(token)
    return {"detail": "Account verified"}


### Email Password Reset Link
@router.get("/forgot_password")
async def forgot_password(email: EmailStr, service: DeliveryPartnerServiceDep):
    await service.send_password_reset_link(email, router.prefix)
    return {"detail": "Check Email for password reset link"}


### Password Reset Form
@router.get("/reset_password_form")
async def get_reset_password_form(request: Request, token: str):
    templates = Jinja2Templates(TEMPLATE_DIR)

    return templates.TemplateResponse(
        request=request,
        name="password/reset.html",
        context={
            "reset_url": f"http://{app_settings.APP_DOMAIN}{router.prefix}/reset_password?token={token}",
        },
    )


### Reset Delivery Partner Password
@router.post("/reset_password")
async def reset_password(
    request: Request,
    token: str,
    password: Annotated[str, Form()],
    service: DeliveryPartnerServiceDep,
):
    is_sucess = await service.reset_password(token, password)
    templates = Jinja2Templates(TEMPLATE_DIR)

    return templates.TemplateResponse(
        request=request,
        name="password/reset_success.html"
        if is_sucess
        else "password/reset_failed.html",
    )


@router.get("/me", response_model=DeliveryPartnerRead)
async def get_delivery_partner_profile(partner: DeliveryPartnerDep):
    return partner


### Get shipments assigned to the delivery partner
@router.get("/shipments", response_model=list[ShipmentRead])
async def get_partner_shipments(partner: DeliveryPartnerDep):
    return partner.shipments


### Logout the delivery partner
@router.get("/logout")
async def logout_delivery_partner(
    token_data: Annotated[dict, Depends(get_partner_access_token)],
):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Successfully logged out"}
