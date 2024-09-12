import pika
import time

pecasNaFabrica = [20] * 100  # Inicializa a lista com 100 peças, cada uma com 20 unidades
nfab = int(input("Digite o número da fábrica: "))

def callback(ch, method, properties, body):
    msg = body.decode("utf-8")
    print("Mensagem recebida:", msg)
    comando = msg.split("/")
    if comando[0] == "linha":
        pecasPedidas = comando[2].split(",")
        pecas = list(map(int, pecasPedidas))
        enviarPecas(comando[1], pecas)

def enviarPecas(linha, pecas):
    pecas_em_falta = [peca for peca in pecas if pecasNaFabrica[peca] == 0]
    if not pecas_em_falta:
        for peca in pecas:
            pecasNaFabrica[peca] -= 1
        enviaPecas(linha, pecas)
    else:
        pedirPecas(pecas_em_falta)

def enviaPecas(linha, pecas):
    envio = ",".join(map(str, pecas))
    channel.basic_publish(exchange='',
                          routing_key='fabrica',
                          body=f"fabrica/{linha}/{envio}")

def pedirPecas(pecas):
    pedido = ",".join(map(str, pecas))
    channel.basic_publish(exchange='',
                          routing_key='fabricas',
                          body=f"fabrica/{nfab}/{pedido}")

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='fabrica')
channel.queue_declare(queue='fabricas')

channel.basic_consume(queue='fabrica', on_message_callback=callback, auto_ack=True)

print("Aguardando mensagens...")
channel.start_consuming()