from httpx import AsyncClient
from app.tests import example


_base_url = "/shipment/"


async def test_shipment_auth(client: AsyncClient):
    response = await client.post(
        url=_base_url,
        json={},
    )
    assert response.status_code == 401
    print(response.json())


async def test_submit_shipment(client: AsyncClient, seller_login: str):
    response = await client.post(
        url=_base_url,
        json=example.shipment,
        headers={"Authorization": f"Bearer {seller_login}"},
    )

    assert response.status_code == 200

    response = await client.get(
        url=_base_url,
        params={"id": response.json()["id"]},
        headers={"Authorization": f"Bearer {seller_login}"},
    )

    assert response.status_code == 200
