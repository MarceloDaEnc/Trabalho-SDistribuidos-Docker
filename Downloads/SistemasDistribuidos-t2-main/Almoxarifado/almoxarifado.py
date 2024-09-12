import pika
import random
import time

nalmoxarifado = 1

class BufferEstoquePartes:
    def __init__(self, capacidade_maxima):
        self.parte = {}
        self.capacidade_maxima = capacidade_maxima
        for i in range(100):
            num_aleat = random.randint(int(capacidade_maxima*0.6), capacidade_maxima)
            nome_parte = "Parte_" + str(i)
            self.parte[nome_parte] = num_aleat

    def check_out(self, quantidade, item):
        if self.parte.get(item, 0) >= quantidade:
            self.parte[item] -= quantidade
            if self.parte[item] <= self.capacidade_maxima*0.40:
                solicitarReabastecimento(item)
            return True
        return False

    def check_in(self, quantidade, item):
        if self.parte.get(item, 0) + quantidade <= self.capacidade_maxima:
            self.parte[item] += quantidade
            return True
        return False

    def obter_valor_atual(self, item):
        return self.parte.get(item, 0)

    def obter_cor_estoque(self, item):
        if self.parte.get(item, 0) < self.capacidade_maxima * 0.33:
            return "Vermelho"
        elif self.parte.get(item, 0) < self.capacidade_maxima * 0.66:
            return "Amarelo"
        else:
            return "Verde"
    
def obter_cor_parte(item):
    global buffer_estoque
    return buffer_estoque.obter_valor_atual(item)

def obter_quantia_parte(item):
    global buffer_estoque
    return buffer_estoque.obter_cor_estoque(item)

buffer_estoque = BufferEstoquePartes(capacidade_maxima=200)

def callback(ch, method, properties, body):
    msg = body.decode("utf-8")
    print("Mensagem recebida:", msg)
    comando = msg.split("/")
    if comando[0] == "fabrica":
        pecasUtilizadas = comando[2].split(",")
        for peca in pecasUtilizadas:
            buffer_estoque.check_out(1, "Parte_" + peca)
    elif comando[0] == "fornecedor":
        peca = comando[2].split(",")
        buffer_estoque.check_out(buffer_estoque.obter_valor_atual("Parte_" + peca), "Parte_" + peca)

def atualizarEstoque(quantidade, peca):
    buffer_estoque.check_out(quantidade, "Parte_" + peca)

def solicitarReabastecimento(peca):
    message = f"reabastecer/{nalmoxarifado}/{peca}"
    channel.basic_publish(exchange='',
                          routing_key='fornecedor',
                          body=message)

parameters = pika.ConnectionParameters("rabbitmq",5672,)
while True:
    try:
        connection = pika.BlockingConnection(parameters)
        hannel = connection.channel()
    except pika.exceptions.AMQPConnectionError:
        print("RabbitMQ not available yet, retrying in 5 seconds...")
        time.sleep(5)

channel.queue_declare(queue='fabrica')
channel.queue_declare(queue='fornecedor')

channel.basic_consume(queue='fabrica', on_message_callback=callback, auto_ack=True)

print("Aguardando mensagens...")
channel.start_consuming()
