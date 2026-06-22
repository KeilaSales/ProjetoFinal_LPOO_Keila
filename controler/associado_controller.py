# CAMADA CONTROLLER: Intermediário entre as Telas (View) e o Banco (DAO)
from dao.AssociadoDAO import AssociadoDAO
from model.Associado import Associado
from model.CalculoMensalidade import ContextoMensalidade

class AssociadoController:
    def __init__(self):
        # Cria a conexão com a camada de banco de dados do Associado
        self.associado_dao = AssociadoDAO()

    def cadastrar_universitario(self, nome, cpf, faculdade, matricula, telefone, vinculo, dias_selecionados, turno_ida="Noite", turno_volta="Noite"):
        identificacao_academica = f"{faculdade} - Matrícula: {matricula}"

        # --- TRATAMENTO DE STRING: Limpa o texto para salvar apenas a sigla da faculdade ---
        faculdade_texto = str(faculdade)
        if "(" in faculdade_texto and ")" in faculdade_texto:
            # Captura o texto que está entre os parênteses 
            sigla = faculdade_texto.split("(")[1].split(")")[0].strip()
        else:
            sigla = faculdade_texto
            
        identificacao_academica = f"{sigla} - {matricula}"  
        
        # Converte a lista de dias ['Segunda', 'Terça'] em texto separado por vírgula: "Segunda,Terça"
        string_dias = ",".join(dias_selecionados)
        
        # INSTANCIAÇÃO: Cria o objeto da Model preenchendo os atributos tratados
        universitario = Associado(
            nome=nome,
            cpf=cpf,
            matricula=identificacao_academica,
            telefone=telefone,
            tipo_associado=vinculo,
            dias_semana=string_dias
        )
        # ENCAPSULAMENTO: Adiciona os turnos escolhidos no objeto antes de enviar ao DAO

        universitario.turno_ida = turno_ida
        universitario.turno_volta = turno_volta
        
        # --- PADRÃO STRATEGY ---
        qtd_dias = len(dias_selecionados)
        contexto = ContextoMensalidade(dias_semana=qtd_dias)
        total_primeiro_mes = contexto.executar_calculo(vinculo) # Roda a matemática isolada do Strategy
        
        # Separa o valor das taxas da mensalidade pura para exibir no recibo da tela
        taxa_adesao = 200.00 if str(vinculo).upper() == "NOVO" else 80.00
        mensalidade_pura = total_primeiro_mes - taxa_adesao
        
        # --- PERSISTÊNCIA: Envia o objeto montado para o DAO gravar no BD ---
        sucesso, msg = self.associado_dao.salvar(universitario)
        if sucesso:
            # Se salvar no banco, devolve um dicionário com os dados prontos para a tela desenhar o recibo
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
        # Repassa o CPF recebido da tela para o DAO deletar o registro no banco 
        return self.associado_dao.remover(cpf)

    def buscar_todos(self):
        # Chama o DAO para fazer o SELECT geral e listar todos na tabela
        return self.associado_dao.listar_todos()