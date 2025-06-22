from collections import Counter
from typing import List, Tuple, Dict
import spacy
from textblob import TextBlob

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
    return [word for word, _ in word_counts.most_common(10)]


def analyze_sentiment(text: str) -> Dict[str, float]:
    """
    Analiza el sentimiento del texto usando TextBlob.
    
    Args:
        text (str): Texto a analizar.
    
    Returns:
        Dict[str, float]: Diccionario con 'polarity' (-1 a 1) y 'subjectivity' (0 a 1).
    """
    blob = TextBlob(text)
    return {
        "polarity": blob.sentiment.polarity,
        "subjectivity": blob.sentiment.subjectivity,
    }


def extract_named_entities(text: str) -> List[Tuple[str, str]]:
    """
    Extrae las entidades nombradas del texto usando spaCy.
    
    Args:
        text (str): Texto a analizar.
        
    Returns:
        List[Tuple[str, str]]: Lista de tuplas (entidad, etiqueta).
    """
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]


# Ejemplo rápido para test
if __name__ == "__main__":
    sample_text = (
        "Barack Obama was the president of the United States and lives in Washington."
    )

    print("Top words:", analyze_text(sample_text))
    print("Sentiment:", analyze_sentiment(sample_text))
    print("Named Entities:", extract_named_entities(sample_text))
