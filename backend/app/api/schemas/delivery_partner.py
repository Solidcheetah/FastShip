from pydantic import BaseModel, EmailStr, Field, model_validator


class BaseDeliveryPartner(BaseModel):
    name: str
    email: EmailStr
    servicable_zip_codes: list[int]
    max_handling_capacity: int

class DeliveryPartnerRead(BaseDeliveryPartner):
    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    @classmethod
    def extract_zip_codes(cls, data):
        # The ORM object exposes `servicable_locations` (list[Location]),
        # but the API returns a flat list of zip codes.
        locations = getattr(data, "servicable_locations", None)
        if locations is not None:
            return {
                "name": data.name,
                "email": data.email,
                "max_handling_capacity": data.max_handling_capacity,
                "servicable_zip_codes": [loc.zip_code for loc in locations],
            }
        return data

class DeliveryPartnerUpdate(BaseModel):
    servicable_zip_codes: list[int] | None = Field(default=None)
    max_handling_capacity: int | None = Field(default=None)

class DeliveryPartnerCreate(BaseDeliveryPartner):
    password: str