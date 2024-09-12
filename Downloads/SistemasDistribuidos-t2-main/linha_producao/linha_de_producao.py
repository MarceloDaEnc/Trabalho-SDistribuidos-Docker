import pika
import time

npecas = 10
produto1 = [0, 1, 2, 3, 4, 5, 8, 9]
pecasNaLinha = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
nlinha = 1

def callback(ch, method, properties, body):
    msg = body.decode("utf-8")
    print("Mensagem recebida:", msg)
    comando = msg.split("/")
    if comando[0] == "fabrica" and comando[1] == str(nlinha):
        pecas = comando[2].split(",")
        for peca in pecas:
            peca = int(peca)
            pecasNaLinha[peca] += 1

def pedirpecas(pecas):
    pedido = ",".join(map(str, pecas))
    channel.basic_publish(exchange='',
                          routing_key='fabrica',
                          body=f"linha/{nlinha}/{pedido}")

def montarproduto(produto):
    contador = 0
    pecas_faltantes = []
    pecas_consumidas = []
    if produto == 1:
        for peca in produto1:
            if pecasNaLinha[peca] > 0:
                pecas_consumidas.append(peca)
            else:
                contador += 1
                pecas_faltantes.append(peca)
    if contador == 0:
        for peca in pecas_consumidas:
            pecasNaLinha[peca] -= 1
        return True
    else:
        pedirpecas(pecas_faltantes)
        return False

def montarpedido(pedido):
    return montarproduto(pedido)

parameters = pika.ConnectionParameters("rabbitmq",5672,)
while True:
    try:
        connection = pika.BlockingConnection(parameters)
        hannel = connection.channel()
    except pika.exceptions.AMQPConnectionError:
        print("RabbitMQ not available yet, retrying in 5 seconds...")
        time.sleep(5)

channel.queue_declare(queue='fabrica')

channel.basic_consume(queue='fabrica', on_message_callback=callback, auto_ack=True)

print("Aguardando mensagens...")
channel.start_consuming()

pedidos = [1, 1, 1, 1]
pedidoatual = 0

while pedidoatual < len(pedidos):
    print(f"Montando pedido {pedidoatual}")
    if montarpedido(pedidos[pedidoatual]):
        pedidoatual += 1
        print("Pedido montado")
    time.sleep(1)
