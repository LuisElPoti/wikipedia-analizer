import requests 


def search_wikipedia(query: str) -> dict:
    """
    Search Wikipedia for a given query and return the results.
    
    Args:
        query (str): The search term to look up on Wikipedia.
        
    Returns:
        dict: A dictionary containing the search results.
    """
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
    }
    
    response = requests.get(url, params=params)   
    response.raise_for_status()
    data = response.json()
    return data.get("query", {}).get("search", [])


def get_article_summary(title: str):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()