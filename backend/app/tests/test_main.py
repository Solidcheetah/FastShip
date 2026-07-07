from httpx import AsyncClient
import pytest
from app.tests import example


# @pytest.mark.asyncio
async def test_main_app(client: AsyncClient):
    response = await client.get("/")
    print("Server is up and running, welcome back lets do some tests: \n\n\n")
    assert response.status_code == 200
