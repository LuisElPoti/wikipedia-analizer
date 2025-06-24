import requests 


def search_wikipedia(query: str) -> dict:
    """
    Busqueda en Wikipedia utilizando la API de MediaWiki.
    
    Args:
        query (str): el termino de búsqueda.
        
    Returns:
        dict: Un diccionario con los resultados de la búsqueda.
    """
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts|pageimages",
        "exintro": True,
        "generator": "search",
        "explaintext": True,
        "gsrsearch": query,
        "origins": "*",
        
    }
    
    response = requests.get(url, params=params)   
    response.raise_for_status()
    data = response.json()
    return  data.get("query", {}).get("pages", {})


def get_full_article(title: str) -> str:
    """
    Obtener el texto completo de un artículo de Wikipedia.
    
    Args:
        title (str): El titulo del artículo.
        
    Returns:
        str: El texto completo del artículo.
    """
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": True,
        "titles": title,
        "format": "json",
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    page = next(iter(data["query"]["pages"].values()))
    return page.get("extract", "")

def get_article_summary(title: str) -> str:
    
    """Obtener un resumen de un artículo de Wikipedia.
    Args:
        title (str): El título del artículo.
    Returns:
        str: El texto resumido.
    """
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    
    # Obtener el extract del artículo
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    # Retornar el extract y url del artículo
    return data.get("extract", ""), data.get("content_urls", {}).get("desktop", {}).get("page", "")

