import pika
import time

nfornecedor = int(input("Digite o número do fornecedor: "))

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

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='almoxarifado')

channel.basic_consume(queue='almoxarifado', on_message_callback=callback, auto_ack=True)

print("Aguardando mensagens...")
channel.start_consuming()