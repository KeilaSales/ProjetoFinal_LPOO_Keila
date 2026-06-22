# SCRIPT DE TESTE: Valida a integração entre a Model e o Banco (DAO)
from model.Associado import Associado
from dao.AssociadoDAO import AssociadoDAO

def executar_teste():
    print("--- Iniciando Teste do CRUD do Associado ---")
    # INSTANCIAÇÃO DO DAO: Cria o objeto responsável por disparar comandos SQL no banco
    dao = AssociadoDAO()
    
    # INSTANCIAÇÃO DA MODEL: Cria um objeto do tipo Associado com dados fictícios para o teste
    novo_aluno = Associado(
        nome="Keila de Sales", 
        cpf="123.456.789-00", 
        matricula="20261010", 
        telefone="(54) 99999-9999", 
        tipo_associado="NOVO", 
        #senha="senha_da_keila_123" 
    )
    
    print("\n[Testando INSERÇÃO]...")
    dao.salvar(novo_aluno)
    
    print("\n[Testando BUSCA]...")
    aluno_buscado = dao.buscar_por_cpf("123.456.789-00")
    
    # VERIFICAÇÃO LÓGICA: Valida se o banco de dados de fato retornou a linha gravada
    if aluno_buscado:
        # Se o objeto foi recuperado com sucesso, imprime as informações na tela do terminal
        print(f"Aluno encontrado com sucesso no banco!")
        print(f"Nome: {aluno_buscado.nome} | Matrícula: {aluno_buscado.matricula}")
    else:
        print("Erro: Aluno não foi encontrado na busca.")
        
    print("\n--- Fim do Teste ---")

if __name__ == "__main__":
    executar_teste()