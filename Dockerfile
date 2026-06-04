# Usa a mesma imagem Python leve e estável que você escolheu
FROM python:3.12.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Instala APENAS o essencial do sistema para compilar pacotes e conectar no Postgres
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Instala o Poetry globalmente dentro do container
RUN pip install --no-cache-dir poetry

# 3. Copia os arquivos de dependências corretos do seu projeto atual
COPY pyproject.toml poetry.lock /app/

# 4. Configura o Poetry para instalar os pacotes direto no container (sem criar outra .venv interna)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# 5. Copia os arquivos do projeto para o container
COPY . /app/

# Garante a permissão de execução para o seu script de inicialização
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]