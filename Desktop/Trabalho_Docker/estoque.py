import redis

class Estoque:
    def __init__(self, host='localhost', port=6379):
        self.redis = redis.Redis(host=host, port=port, db=0)

    def incrementar(self, parte, quantidade):
        atual = int(self.redis.get(parte) or 0)
        self.redis.set(parte, atual + quantidade)

    def decrementar(self, parte, quantidade):
        atual = int(self.redis.get(parte) or 0)
        if atual >= quantidade:
            self.redis.set(parte, atual - quantidade)
            return True
        return False

    def verificar(self, parte):
        return int(self.redis.get(parte) or 0)