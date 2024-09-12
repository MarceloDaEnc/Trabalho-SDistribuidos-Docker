from linha import LinhaProducao

class Fabrica:
    def __init__(self, nome, linhas_config):
        self.nome = nome
        self.linhas = {nome: LinhaProducao(nome, config["tamanho_buffer"]) for nome, config in linhas_config.items()}
    
    def produzir_em_linha(self, linha_nome, produto, estoque):
        linha = self.linhas.get(linha_nome)
        if linha:
            linha.produzir(produto, estoque)
        else:
            print(f"Linha {linha_nome} não encontrada na fábrica {self.nome}.")
    
    def consumir_em_linha(self, linha_nome):
        linha = self.linhas.get(linha_nome)
        if linha:
            linha.consumir()
        else:
            print(f"Linha {linha_nome} não encontrada na fábrica {self.nome}.")
    
    def status_buffer_linha(self, linha_nome):
        linha = self.linhas.get(linha_nome)
        if linha:
            return linha.status_buffer()
        else:
            print(f"Linha {linha_nome} não encontrada na fábrica {self.nome}.")
            return None