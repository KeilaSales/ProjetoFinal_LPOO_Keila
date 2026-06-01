from model.Associado import Associado
from model.Rota import Rota
from model.CalculoMensalidade import ContextoMensalidade

class Inscricao:
    def __init__(self, id_inscricao=None, associado: Associado = None, rota: Rota = None, 
                 turno_ida=None, turno_volta=None, dias_semana=0, status="ATIVA"):
        """
        Une o Associado à sua rota e turnos escolhidos.
        Permite turnos de ida e volta diferentes.
        """
        self.id_inscricao = id_inscricao
        self.associado = associado       
        self.rota = rota                 
        self.turno_ida = turno_ida        
        self.turno_volta = turno_volta    
        self.dias_semana = dias_semana   
        self.status = status           
        self.valor_mensalidade = 0.0
        
        if dias_semana > 0 and associado is not None:
            self.atualizar_mensalidade()

    def atualizar_mensalidade(self):
        """
        Invoca o padrão Strategy para calcular o valor da mensalidade do associado.
        """
        contexto = ContextoMensalidade(self.dias_semana)
        self.valor_mensalidade = contexto.executar_calculo(self.associado.tipo_associado)