from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

from app.api.dependencies import SellerDep, SellerServiceDep, get_seller_access_token
from app.core.security import TokenData
from app.database.redis import add_jti_to_blacklist
from app.utils import TEMPLATE_DIR
from app.config import app_settings
from app.api.schemas.shipment import ShipmentRead

from ..schemas.seller import SellerCreate, SellerRead

router = APIRouter(prefix="/seller", tags=["Seller"])


@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    return await service.add(seller)


@router.post("/login", response_model=TokenData)
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.login(request_form.username, request_form.password)
    return {"access_token": token, "token_type": "jwt"}


# Verify Seller Email
@router.get("/verify")
async def verify_seller_email(token: str, service: SellerServiceDep):
    await service.verify_email(token)
    return {"detail": "Account verified"}


# Email Password Reset Link
@router.get("/forgot_password")
async def forgot_password(email: EmailStr, service: SellerServiceDep):
    await service.send_password_reset_link(email, router.prefix)
    return {"detail": "Check Email for password reset link"}


@router.get("/me", response_model=SellerRead)
async def get_seller_profile(seller: SellerDep):
    return seller


@router.get("/shipments", response_model=list[ShipmentRead])
async def get_shipments(seller: SellerDep):
    return seller.shipments


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


# Reset Seller Password
@router.post("/reset_password")
async def reset_password(
    request: Request,
    token: str,
    password: Annotated[str, Form()],
    service: SellerServiceDep,
):
    is_sucess = await service.reset_password(token, password)
    templates = Jinja2Templates(TEMPLATE_DIR)

    return templates.TemplateResponse(
        request=request,
        name="password/reset_success.html"
        if is_sucess
        else "password/reset_failed.html",
    )


@router.get("/logout")
async def logout_seller(token_data: Annotated[dict, Depends(get_seller_access_token)]):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Successfully logged out"}
