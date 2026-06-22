# CAMADA MODEL: Molde puro de dados que representa a entidade Associado
class Associado:
    # CONSTRUTOR: Método que inicializa e define a estrutura do objeto na memória ao ser instanciado
    def __init__(self, id_associado=None, nome=None, matricula=None, cpf=None, telefone=None, tipo_associado="NOVO", dias_semana = None):

       # NOVO ( matrícula) e ANTIGO (rematrícula)

        #self.id_associado = id_associado
        self.nome = nome
        self.matricula = matricula
        self.cpf = cpf
        self.telefone = telefone
        self.tipo_associado = tipo_associado  
        self.dias_semana = dias_semana

        # Atributos logísticos padrões que são injetados pelo Controller após a escolha na tela
        self.turno_ida = "Noite"       
        self.turno_volta = "Noite"