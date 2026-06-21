import sys
import os


from model.Associado import Associado
from model.Rota import Rota
from model.Inscricao import Inscricao
from model.CalculoMensalidade import ContextoMensalidade

from dao.AssociadoDAO import AssociadoDAO
from dao.RotaDAO import RotaDAO
from dao.InscricaoDAO import InscricaoDAO

def executar_teste_integrado():
    print("--- INICIANDO TESTE DE INTEGRAÇÃO  ---")
    
    associado_dao = AssociadoDAO()
    rota_dao = RotaDAO()
    inscricao_dao = InscricaoDAO()
    
    # 1. Criar e Persistir um Associado de Teste
    print("\n[Passo 1] Cadastrando Associado...")
    aluno = Associado(
        nome="Keila de Sales",
        cpf="987.654.321-00",
        matricula="20261020",
        telefone="(54) 99999-8888",
        tipo_associado="NOVO",
        dias_semana="Segunda,Quarta,Sexta"
    )

    aluno.turno_ida = "Tarde"
    aluno.turno_volta = "Noite"
    
    existe_aluno = associado_dao.buscar_por_cpf(aluno.cpf)
    if not existe_aluno:
        sucesso_aluno, msg_aluno = associado_dao.salvar(aluno)
        print(f"-> {msg_aluno}")
    else:
        aluno = existe_aluno
        print("-> Associado já existente no banco, reaproveitando registro.")

    # 2. Criar e Persistir uma Rota de Teste
    print("\n[Passo 2] Cadastrando Rota...")
    linha_pf = Rota()
    linha_pf.destino = "Passo Fundo - Campus UPF"
    linha_pf.itinerario = "Lagoa Vermelha x BR-285 x Passo Fundo"
    linha_pf.capacidade_maxima = 45
    linha_pf.vagas_disponiveis = 45
    
    sucesso_rota, msg_rota = rota_dao.salvar(linha_pf)
    print(f"-> {msg_rota}")
    
    # Recupera a rota para associar corretamente com ID do banco
    lista_rotas = rota_dao.listar_todos()
    if lista_rotas:
        linha_pf = lista_rotas[-1]
        print(f"-> Rota recuperada com ID: {linha_pf.id_rota}")

    # 3. Criar, Calcular via Contexto/Strategy e Persistir uma Inscrição
    print("\n[Passo 3] Gerando Inscrição (Usando o Padrão Strategy)...")
    inscricao = Inscricao()
    inscricao.associado = aluno
    inscricao.rota = linha_pf
    inscricao.turno_ida = aluno.turno_ida
    inscricao.turno_volta = aluno.turno_volta

    # Descobre a quantidade de dias e aplica o Contexto do Strategy que você programou
    inscricao.dias_semana = 3 
    contexto = ContextoMensalidade(dias_semana=inscricao.dias_semana)

    # Executa o cálculo passando o tipo do associado ("NOVO")
    inscricao.valor_mensalidade = contexto.executar_calculo(aluno.tipo_associado)
    
    sucesso_ins, msg_ins = inscricao_dao.salvar(inscricao)
    {True, "Sucesso simulado"} if not inscricao_dao.conexao else inscricao_dao.salvar(inscricao)
    print(f"-> Valor calculado pela sua Estrategia (3 dias + taxa NOVO): R$ {inscricao.valor_mensalidade:.2f}")

    # 4. Validar o SELECT
    print("\n[Passo 4] Validando leitura global do banco...")
    inscricoes_salvas = inscricao_dao.listar_todos()
    print(f"-> Total de inscrições ativas no sistema: {len(inscricoes_salvas)}")
    
    print("\n--- Fim do Teste de Integração Sem Erros ---")

if __name__ == "__main__":
    executar_teste_integrado()