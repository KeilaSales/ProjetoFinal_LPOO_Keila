class Associado:
    def __init__(self, id_associado=None, nome=None, matricula=None, cpf=None, telefone=None, tipo_associado="NOVO", senha=None):
        """
        NOVO ( matrícula) e ANTIGO (rematrícula)
        """
        self.id_associado = id_associado
        self.nome = nome
        self.matricula = matricula
        self.cpf = cpf
        self.telefone = telefone
        self.tipo_associado = tipo_associado  
        self.senha = senha 