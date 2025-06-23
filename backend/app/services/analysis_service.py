from collections import Counter
from typing import List, Tuple, Dict
import spacy
from textblob import TextBlob
import re

nlp = spacy.load("en_core_web_sm")


def analyze_text(text: str) -> List[str]:
    """
    Analiza el texto para obtener las 10 palabras más comunes excluyendo stopwords.
    
    Args:
        text (str): Texto a analizar.
        
    Returns:
        List[str]: Lista de palabras más frecuentes (excluyendo stopwords).
    """
    doc = nlp(text)
    words = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
    word_counts = Counter(words)
    return [word for word, _ in word_counts.most_common(5)]


def analyze_sentiment(text: str) -> str:
    """
    Analiza el sentimiento del texto usando TextBlob.
    
    Args:
        text (str): Texto a analizar.
    
    Returns:
        Dict[str, float]: Diccionario con 'polarity' (-1 a 1) y 'subjectivity' (0 a 1).
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0.1:
        sentiment = "positivo"
    elif polarity < -0.1:
        sentiment = "negativo"
    else:
        sentiment = "neutral"

    return sentiment


def generate_article_analysis(extract: str) -> Dict:
    """
    Genera análisis del resumen: complejidad, tiempo de lectura, temas y estadísticas básicas.

    Args:
        title (str): Título del artículo
        extract (str): Resumen o texto del artículo

    Returns:
        Dict: Diccionario con análisis del artículo
    """
    # Limpiar y dividir texto
    sentences = [s.strip() for s in re.split(r'[.!?]', extract) if s.strip()]
    word_count = len(extract.split())
    sentence_count = len(sentences)
    avg_words_per_sentence = round(word_count / sentence_count) if sentence_count > 0 else 0
    estimated_reading_time = max(1, round(word_count / 200))  # palabras por minuto

    # Temas principales simulados
    topics = []
    extract_lower = extract.lower()
    if "historia" in extract_lower or "histórico" in extract_lower:
        topics.append("Historia")
    if "ciencia" in extract_lower or "científico" in extract_lower:
        topics.append("Ciencia")
    if "arte" in extract_lower or "cultura" in extract_lower:
        topics.append("Arte y Cultura")
    if "política" in extract_lower or "gobierno" in extract_lower:
        topics.append("Política")
    if not topics:
        topics.append("General")

    # Complejidad
    if avg_words_per_sentence > 20:
        complexity = "Avanzada"
    elif avg_words_per_sentence > 15:
        complexity = "Intermedia"
    else:
        complexity = "Básica"

    # Insights
    insights = [
        f"Este artículo contiene {word_count} palabras distribuidas en {sentence_count} oraciones.",
        f"La complejidad del texto es {complexity.lower()} con un promedio de {avg_words_per_sentence} palabras por oración.",
        f"Tiempo estimado de lectura: {estimated_reading_time} minuto{'s' if estimated_reading_time > 1 else ''}.",
    ]

    result = {
        "frequent_words": analyze_text(extract),
        "sentiment": analyze_sentiment(extract),
        "topics": topics,
        "complexity": complexity,
        "word_count": word_count,
        "sentences": sentence_count,
        "avg_words_per_sentence": avg_words_per_sentence,
        "estimated_reading_time": estimated_reading_time,
        "key_insights": insights,
    }
    # Debugging output
    print(result)
    
    return result
    


