from dao.AssociadoDAO import AssociadoDAO
from model.Associado import Associado
from model.CalculoMensalidade import ContextoMensalidade

class AssociadoController:
    def __init__(self):
        self.associado_dao = AssociadoDAO()

    def cadastrar_universitario(self, nome, cpf, faculdade, matricula, telefone, vinculo, dias_selecionados, turno_ida="Noite", turno_volta="Noite"):
        identificacao_academica = f"{faculdade} - Matrícula: {matricula}"
        string_dias = ",".join(dias_selecionados)
        
        universitario = Associado(
            nome=nome,
            cpf=cpf,
            matricula=identificacao_academica,
            telefone=telefone,
            tipo_associado=vinculo,
            senha=string_dias
        )
        # Adiciona os turnos escolhidos no objeto antes de enviar ao DAO
        universitario.turno_ida = turno_ida
        universitario.turno_volta = turno_volta
        
        qtd_dias = len(dias_selecionados)
        contexto = ContextoMensalidade(dias_semana=qtd_dias)
        total_primeiro_mes = contexto.executar_calculo(vinculo)
        
        taxa_adesao = 200.00 if str(vinculo).upper() == "NOVO" else 80.00
        mensalidade_pura = total_primeiro_mes - taxa_adesao
        
        sucesso, msg = self.associado_dao.salvar(universitario)
        if sucesso:
            return True, {
                "nome": universitario.nome,
                "dias": string_dias,
                "qtd": qtd_dias,
                "mensalidade_pura": mensalidade_pura,
                "taxa": taxa_adesao,
                "total_primeiro_mes": total_primeiro_mes
            }
        return False, msg
    
    def remover_universitario(self, cpf):
        return self.associado_dao.remover(cpf)

    def buscar_todos(self):
        return self.associado_dao.listar_todos()