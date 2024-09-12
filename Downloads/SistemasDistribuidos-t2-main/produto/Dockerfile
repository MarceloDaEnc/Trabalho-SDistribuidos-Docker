FROM python:3.8

# Atualizar o pip para a versão mais recente
RUN python -m pip install --upgrade pip

# Copie o código do Produto para o container
COPY produto.py /app/produto.py

# Defina o diretório de trabalho
WORKDIR /app

# Instale as bibliotecas necessárias (no caso, paho-mqtt)
RUN pip install pika

# Comando para executar o script do Produto
CMD ["python", "produto.py"]
