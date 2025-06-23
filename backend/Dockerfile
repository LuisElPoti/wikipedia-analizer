FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Node.js para Prisma CLI
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g prisma@5.17.0

# Instalar textblob
RUN python -m textblob.download_corpora

# Instalar spaCy y el modelo en_core_web_sm
RUN python -m spacy download en_core_web_sm

COPY . .

CMD ["uvicorn", "app.main:app", "--host", a"0.0.0.0", "--port", "8000", "--reload"]
