FROM python:3.8

# Atualizar o pip para a versão mais recente
RUN python -m pip install --upgrade pip

# Copie o código da Linha de Produção para o container
COPY linha_de_producao.py /app/linha_de_producao.py

# Defina o diretório de trabalho
WORKDIR /app

# Instale as bibliotecas necessárias (no caso, paho-mqtt)
RUN pip install pika

# Comando para executar o script da Linha de Produção
CMD ["python", "linha_de_producao.py"]
