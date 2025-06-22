# Wikipedia Analyzer - Backend

Este es el backend de **Wikipedia Analyzer**, una aplicación que permite buscar artículos de Wikipedia, analizarlos lingüísticamente (palabras clave, sentimiento, entidades nombradas), y guardarlos para su posterior revisión.

## 🧠 Funcionalidad principal

- Buscar artículos en Wikipedia.
- Obtener resumen y contenido completo.
- Analizar texto: palabras clave, análisis de sentimiento y entidades nombradas.
- Guardar artículos analizados con notas opcionales.
- Listar artículos guardados.

Todos los endpoints están documentados en Swagger:
👉 http://localhost:8000/docs


## 🚀 Tecnologías usadas

- **FastAPI**: Framework backend asincrónico en Python.
- **Prisma (via Prisma Client Python)**: ORM para conectarse con la base de datos PostgreSQL.
- **TextBlob**: Análisis de sentimiento y palabras más comunes.
- **spaCy**: Detección de entidades nombradas (NLP).
- **Uvicorn**: Servidor ASGI para correr FastAPI.
- **Docker / Docker Compose**: Contenedores para el entorno de ejecución.


## ⚙️ Cómo correr el backend

### Opción recomendada (Docker)

```bash
docker-compose up --buil
```

- Backend disponible en http://localhost:8000
- PostgreSQL ya configurado
- Migraciones automáticas

### Opción manual (sin Docker)

```bash
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
cd app
python main.py
```
NOTA: Asegúrate de tener un PostgreSQL local y configurar DATABASE_URL en .env.


## Apuntes técnicos importantes a resaltar

- TextBlob evita dependencias pesadas como NLTK para análisis de texto básico (ya maneja tokenización y sentimiento).

- spaCy (modelo en inglés) es más confiable que NLTK para NER.

- Top palabras se filtran usando solo tokens alfabéticos y excluyen stopwords.

- Prisma facilita el trabajo con PostgreSQL y mantiene el esquema tipado.