# 1. Base Python
FROM python:3.12-slim AS builder
WORKDIR /app

# 2. Instala dependências e Coexum CLI
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Build do frontend estático (assume que frontend/dist já exista ou será montado via volume)
# Se você quiser buildar aqui, monte o src e rode npm/yarn para gerar static/assets

# 3. Imagem final
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app /app
# Instala novamente as dependências no estágio final para garantir que os binários estejam no PATH
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000 9000
# Carrega variáveis de ambiente, se existirem
ENV API_PORT=8000 \
    P2P_PORT=9000 \
    REGISTRY_URL=http://backend:8000 \
    SCHEDULE_INTERVAL=30

# Inicia por padrão o backend; scheduler e node serão executados como serviços separados
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
