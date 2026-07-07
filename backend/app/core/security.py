from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/seller/login", auto_error=False, scheme_name="Seller"
)
oauth2_scheme_partner = OAuth2PasswordBearer(
    tokenUrl="/partner/login", auto_error=False, scheme_name="Delivery Partner"
)


class TokenData(BaseModel):
    access_token: str
    token_type: str
