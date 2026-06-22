# PADRÃO DE PROJETO STRATEGY: Isola as regras de cálculo financeiro
from abc import ABC, abstractmethod

class StrategyMensalidade(ABC):
    # CLASSE ABSTRATA: Define a interface comum para todas as estratégias de cálculo
    @abstractmethod
    def calcular(self, tipo_associado: str) -> float:
        pass

# ESTRATÉGIAS CONCRETAS: Cada classe abaixo implementa de forma isolada a matemática de uma quantidade de dias
class EstrategiaUmDia(StrategyMensalidade):
    def calcular(self, tipo_associado: str) -> float:
        taxa_base = 1 * 280.0 
        taxa_adesao = 200.0 if tipo_associado == "NOVO" else 80.0

        return taxa_base + taxa_adesao


class EstrategiaDoisDias(StrategyMensalidade):
    def calcular(self, tipo_associado: str) -> float:
        taxa_base = 2 * 240.0  
        taxa_adesao = 200.0 if tipo_associado == "NOVO" else 80.0
        return taxa_base + taxa_adesao


class EstrategiaTresDias(StrategyMensalidade):
    def calcular(self, tipo_associado: str) -> float:
        taxa_base = 3 * 200.0  
        taxa_adesao = 200.0 if tipo_associado == "NOVO" else 80.0
        return taxa_base + taxa_adesao


class EstrategiaQuatroDias(StrategyMensalidade):
    def calcular(self, tipo_associado: str) -> float:
        taxa_base = 4 * 180.0  
        taxa_adesao = 200.0 if tipo_associado == "NOVO" else 80.0
        return taxa_base + taxa_adesao


class EstrategiaCincoDias(StrategyMensalidade):
    def calcular(self, tipo_associado: str) -> float:
        taxa_base = 5 * 160.0  
        taxa_adesao = 200.0 if tipo_associado == "NOVO" else 80.0
        return taxa_base + taxa_adesao


class ContextoMensalidade:

    def __init__(self, dias_semana: int):
        # POLIMORFISMO: Instancia a estratégia correta com base no número de dias passados
        if dias_semana == 1:
            self._estrategia = EstrategiaUmDia()
        elif dias_semana == 2:
            self._estrategia = EstrategiaDoisDias()
        elif dias_semana == 3:
            self._estrategia = EstrategiaTresDias()
        elif dias_semana == 4:
            self._estrategia = EstrategiaQuatroDias()
        elif dias_semana == 5:
            self._estrategia = EstrategiaCincoDias()
        else:
            raise ValueError("Quantidade de dias inválida. Escolha entre 1 e 5 dias.")

    def executar_calculo(self, tipo_associado: str) -> float:
        return self._estrategia.calcular(tipo_associado)