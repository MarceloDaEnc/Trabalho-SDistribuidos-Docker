# Use a imagem oficial do Python como base
FROM python:3.8-slim

# Instale o cliente Redis
RUN pip install redis

# Copie o código da aplicação
COPY . /app
WORKDIR /app

# Comando para rodar a aplicação
CMD ["python", "main.py"]