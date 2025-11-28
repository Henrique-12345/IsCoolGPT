# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Instalar curl para healthcheck
RUN apt-get update && apt-get install -y \
curl \
ca-certificates \
&& rm -rf /var/lib/apt/lists/*

# Copiar dependências instaladas do stage builder
COPY --from=builder /root/.local /root/.local

# Copiar código da aplicação
COPY ./app /app/app
COPY ./frontend /app/frontend

# Adicionar binários ao PATH
ENV PATH=/root/.local/bin:$PATH

# Expor porta
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando de execução
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

