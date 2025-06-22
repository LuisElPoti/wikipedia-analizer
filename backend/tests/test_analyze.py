import pytest
from httpx import AsyncClient 

@pytest.mark.asyncio
async def test_analyze_article(client): 
    response = client.get("/articles/Barack_Obama") 
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "top_words" in data
    assert "sentiment" in data
    assert "named_entities" in data