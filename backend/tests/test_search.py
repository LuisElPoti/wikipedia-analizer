import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_search_articles(client):
    response = client.get("/search?q=Obama")
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    assert len(results) > 0
    assert "title" in results[0]
