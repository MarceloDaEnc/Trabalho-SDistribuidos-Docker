from buffer import Buffer

class LinhaProducao:
    def __init__(self, nome, tamanho_buffer):
        self.nome = nome
        self.buffer = Buffer(tamanho_buffer)
    
    def produzir(self, produto, estoque):
        partes_necessarias = produto.partes_necessarias()
        for parte, quantidade in partes_necessarias.items():
            if estoque.decrementar(parte, quantidade):
                self.buffer.adicionar((parte, quantidade))
                print(f"[{self.nome}] Produzido {produto.nome}, consumindo {quantidade} de {parte}")
            else:
                print(f"[{self.nome}] Estoque insuficiente de {parte}")
    
    def consumir(self):
        item = self.buffer.consumir()
        if item:
            parte, quantidade = item
            print(f"[{self.nome}] Consumido {quantidade} de {parte} do buffer")
        else:
            print(f"[{self.nome}] Buffer vazio, nada a consumir.")
    
    def status_buffer(self):
        return self.buffer.nivel_atual()