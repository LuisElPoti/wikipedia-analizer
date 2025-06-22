import pytest
from httpx import AsyncClient
# @pytest.mark.asyncio
# async def test_create_and_list_saved_articles(client: AsyncClient):
#     payload = {
#         "title": "Barack Obama",
#         "url": "https://en.wikipedia.org/wiki/Barack_Obama",
#         "summary": "Barack Obama was the 44th President of the United States.",
#         "top_words": ["barack", "obama", "president", "united", "states"],
#         "sentiment": {"polarity": 0.1, "subjectivity": 0.5},
#         "named_entities": [["Barack Obama", "PERSON"]],
#         "note": "Test article"
#     }

#     # Crear
#     response = client.post("/saved_articles/", json=payload)
#     assert response.status_code == 200
#     saved = response.json()
#     assert saved["title"] == payload["title"]

#     # Listar
#     response = client.get("/saved_articles/")
#     assert response.status_code == 200
#     articles = response.json()
#     assert any(a["title"] == "Barack Obama" for a in articles)


# @pytest.mark.asyncio
# async def test_create_and_list_saved_articles(client: AsyncClient):
#     payload = {
#         "title": "Barack Obama",
#         "url": "https://en.wikipedia.org/wiki/Barack_Obama",
#         "summary": "Barack Obama was the 44th President of the United States.",
#         "top_words": ["barack", "obama", "president", "united", "states"],
#         "sentiment": {"polarity": 0.1, "subjectivity": 0.5},
#         "named_entities": [["Barack Obama", "PERSON"]],
#         "note": "Test article"
#     }

#     # Crear
#     response = await client.post("/saved_articles/", json=payload)
#     print("STATUS CODE:", response.status_code)
#     print("RESPONSE BODY:", response.text)  # 👈 esto mostrará el traceback

#     assert response.status_code == 200

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_and_list_saved_articles(client):
    payload = {
        "title": "Barack Obama",
        "url": "https://en.wikipedia.org/wiki/Barack_Obama",
        "summary": "Barack Obama was the 44th President of the United States.",
        "top_words": ["barack", "obama", "president", "united", "states"],
        "sentiment": {"polarity": 0.1, "subjectivity": 0.5},
        "named_entities": [["Barack Obama", "PERSON"]], 
        "note": "Test article"
    }

    # Crear
    response = client.post("/saved_articles/", json=payload)
    assert response.status_code == 200
    created_article = response.json()
    assert "id" in created_article
    assert created_article["title"] == "Barack Obama"

    # Listar
    list_response = client.get("/saved_articles/")
    assert list_response.status_code == 200
    articles = list_response.json()
    assert any(article["title"] == "Barack Obama" for article in articles)
