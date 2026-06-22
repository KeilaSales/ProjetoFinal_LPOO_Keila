# CAMADA MODEL: Classe associativa que une Aluno, Rota e o Financeiro
from model.Associado import Associado
from model.Rota import Rota
from model.CalculoMensalidade import ContextoMensalidade

class Inscricao:
    #Construtor: inicializa o contrato de transporte do estudante 
    def __init__(self, id_inscricao=None, associado: Associado = None, rota: Rota = None, 
                 turno_ida=None, turno_volta=None, dias_semana=0, status="ATIVA"):
        
        #Une o Associado à sua rota e turnos escolhidos.
        #Permite turnos de ida e volta diferentes.
        
        #self.id_inscricao = id_inscricao

        # RELACIONAMENTO ENTRE OBJETOS: Guarda instâncias inteiras das outras classes da Model
        self.associado = associado  # Atributo recebe um objeto completo da classe Associado     
        self.rota = rota            # Atributo recebe um objeto completo da classe Rota    

        #Atrubutos logisticos específicos desta inscrição  
        self.turno_ida = turno_ida        
        self.turno_volta = turno_volta    
        self.dias_semana = dias_semana  #Quantidade de dias (inteiro) usado para disparar o Strategy 
        self.status = status           
        self.valor_mensalidade = 0.0   # Começa zerado e é modificado após o cálculo matemático
        
        if dias_semana > 0 and associado is not None:
            self.atualizar_mensalidade()

    def atualizar_mensalidade(self):
        
        # Invoca o padrão Strategy para calcular o valor da mensalidade do associado.
        
        contexto = ContextoMensalidade(self.dias_semana)
        # POLIMORFISMO: Executa o cálculo enviando o tipo de vínculo do objeto associado anexado
        self.valor_mensalidade = contexto.executar_calculo(self.associado.tipo_associado)