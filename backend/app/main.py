from fastapi import FastAPI
from fastapi.routing import APIRoute
from scalar_fastapi import get_scalar_api_reference

from app.api.router import master_router
from app.core.exceptions import add_exception_handlers
from fastapi.middleware.cors import CORSMiddleware


description = """
Delivery Management system for sellers and delivery agents

### Seller
- Submit Shipment effortlessly
- Share tracking links with customers

### Delivery Agent
- Auto accept shipments
- Track and update shipment status
- Email and sms notifications

"""


def custom_generate_unique_id_function(route: APIRoute) -> str:
    return route.name


app = FastAPI(
    title="FastShip",
    description=description,
    generate_unique_id_function=custom_generate_unique_id_function,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(master_router)

add_exception_handlers(app)


@app.get("/")
def read_root():
    return {"detail": "server is running correctly..."}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
