import pika
import time

nfornecedor = 1

def callback(ch, method, properties, body):
    msg = body.decode("utf-8")
    print("Mensagem recebida:", msg)
    comando = msg.split("/")
    if comando[0] == "almoxarifado" and int(comando[1]) == nfornecedor:
        peca = int(comando[2])
        fornecerPeca(peca)

def fornecerPeca(peca):
    enviarPecaAoAlmoxarifado(peca)

def enviarPecaAoAlmoxarifado(peca):
    message = f"reabastecido/{nfornecedor}/{peca}"
    channel.basic_publish(exchange='',
                          routing_key='almoxarifado',
                          body=message)

parameters = pika.ConnectionParameters("rabbitmq",5672,)
while True:
    try:
        connection = pika.BlockingConnection(parameters)
        hannel = connection.channel()
    except pika.exceptions.AMQPConnectionError:
        print("RabbitMQ not available yet, retrying in 5 seconds...")
        time.sleep(5)

channel.queue_declare(queue='almoxarifado')

channel.basic_consume(queue='almoxarifado', on_message_callback=callback, auto_ack=True)

print("Aguardando mensagens...")
channel.start_consuming()
