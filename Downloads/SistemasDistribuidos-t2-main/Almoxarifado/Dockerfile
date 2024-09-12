FROM python:3.8

# Atualizar o pip para a versão mais recente
RUN python -m pip install --upgrade pip

# Copie o código do Almoxarifado para o container
COPY almoxarifado.py /app/almoxarifado.py

# Defina o diretório de trabalho
WORKDIR /app

# Instale as bibliotecas necessárias (no caso, pika para RabbitMQ)
RUN pip install pika

# Comando para executar o script do Almoxarifado
CMD ["python", "almoxarifado.py"]
