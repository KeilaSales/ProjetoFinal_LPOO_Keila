# CAMADA MODEL: Molde puro de dados que representa a entidade Rota
class Rota:
    # CONSTRUTOR: Define as propriedades básicas do trajeto físico do transporte
    def __init__(self, id_rota=None, nome_rota=None, destino=None):
        self.id_rota = id_rota
        self.nome_rota = nome_rota
        self.destino = destino #Universidade