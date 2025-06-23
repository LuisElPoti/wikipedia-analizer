# Wikipedia Analyzer 

Este es el proyecto de **Wikipedia Analyzer**, una aplicación que permite buscar artículos de Wikipedia, analizarlos lingüísticamente (palabras clave, sentimiento, entidades nombradas), y guardarlos para su posterior revisión.

## 🧠 Funcionalidad principal

- Buscar artículos en Wikipedia.
- Obtener resumen y contenido completo.
- Analizar texto: palabras clave, análisis de sentimiento.
- Temas principales, Palabras mas repetidas, complejidad texto, oraciones, palabras/oracion, min. de lectura.
- Insights claves sobre el articulo
- Guardar artículos analizados con notas opcionales.
- Listar artículos guardados.

Todos los endpoints están documentados en Swagger:
👉 http://localhost:8000/docs


## 🚀 Tecnologías usadas

- **FastAPI**: Framework backend asincrónico en Python.
- **SQLAlchemy**: ORM para conectarse con la base de datos PostgreSQL.
- **TextBlob**: Análisis de sentimiento y palabras más comunes.
- **spaCy**: Detección de entidades nombradas (NLP).
- **Uvicorn**: Servidor ASGI para correr FastAPI.
- **Frontend**: Se utilizó Next js para la realziación del frontend


## ⚙️ Cómo correr el backend

```bash
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
cd backend/app
python main.py
```
NOTA: Asegúrate de tener un PostgreSQL local y configurar DATABASE_URL en .env.


## ⚙️ Cómo correr el Frontend

```bash
cd frontend
npm i
npm run dev
```

NOTA: Asegúrate de tener NEXT_PUBLIC_API_URL = http://localhost:8000 en .env.

## Apuntes técnicos importantes a resaltar

- TextBlob evita dependencias pesadas como NLTK para análisis de texto básico (ya maneja tokenización y sentimiento).

- spaCy (modelo en inglés) es más confiable que NLTK para NER.

- Top palabras se filtran usando solo tokens alfabéticos y excluyen stopwords.

- Análisis básico realizado para dar mayor información sobre el artículo de manera resumida.