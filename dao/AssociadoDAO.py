#CAMADA DAO: Responsável por fazer o CRUD direto no banco
import sys
import os

from model.Associado import Associado
from dao.db_config import DatabaseConfig
from dao.Generic_dao import GenericDAO

# POLIMORFISMO E HERANÇA: Herda de GenericDAO e implementa seus métodos obrigatórios
class AssociadoDAO(GenericDAO):
    def __init__(self):
       # Puxa a conexão ativa com o banco configurada no db_config
        self.conexao = DatabaseConfig.get_connection()
        
    def salvar(self, associado: Associado):
        # Insere um novo associado no banco de dados (CREATE)
        if not self.conexao:
            return False, "Sem conexão com o banco de dados"
            
        cursor = None
        sql = """
            INSERT INTO associado (nome, cpf, matricula, telefone, tipo_associado, dias_semana, turno_ida, turno_volta)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            cursor = self.conexao.cursor()
            # Substitui os %s pelos dados reais contidos no objeto da Model
            cursor.execute(sql, (
                associado.nome, 
                associado.cpf, 
                associado.matricula, 
                associado.telefone,
                associado.tipo_associado, 
                associado.dias_semana,
                associado.turno_ida,  
                associado.turno_volta
            ))
            self.conexao.commit() # Grava as alterações no banco
            print("Associado salvo com sucesso no banco!")
            return True, "Associado cadastrado com sucesso"
        except Exception as e:
            self.conexao.rollback() # Segurança: cancela a operação caso dê algum erro
            print(f"Erro ao inserir associado: {e}")
            return False, f"Erro ao inserir associado: {e}"
        finally:
            if cursor: 
                cursor.close() #Fecha o cursor para liberar memória

    def listar_todos(self):
        # Retorna todos os associados cadastrados (R do CRUD) """
        if not self.conexao:
            return [] 
            
        cursor = None
        sql = "SELECT nome, cpf, matricula, telefone, tipo_associado, dias_semana, turno_ida, turno_volta FROM associado ORDER BY nome;"
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql)
            linhas = cursor.fetchall() # Captura todos os registros retornados do banco
            
            # Converte a lista de tuplas do Postgres em uma lista de objetos Associado
            associados = []

            for linha in linhas:
                
                obj = Associado(
                    nome=linha[0],
                    cpf=linha[1],
                    matricula=linha[2],
                    telefone=linha[3],
                    tipo_associado=linha[4],
                    dias_semana=linha[5]
                )
                obj.turno_ida = linha[6]
                obj.turno_volta = linha[7]
                associados.append(obj)
            return associados
        except Exception as e:
            print(f"Erro ao buscar associados: {e}")
            return []
        finally:
            if cursor: 
                cursor.close()

    def buscar_por_cpf(self, cpf: str):
        # Busca um associado específico pelo CPF 
        if not self.conexao:
            return None
            
        cursor = None
        sql = "SELECT nome, cpf, matricula, telefone, tipo_associado, dias_semana, turno_ida, turno_volta FROM associado WHERE cpf = %s;"
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql, (cpf,))
            linha = cursor.fetchone() # Puxa apenas a primeira linha encontrada
            
            # Transforma a linha do banco em um objeto da Model
            if linha:
                novo_associado = Associado(
                    nome=linha[0],
                    cpf=linha[1],
                    matricula=linha[2],
                    telefone=linha[3],
                    tipo_associado=linha[4],
                    dias_semana=linha[5]
                )
                novo_associado.turno_ida = linha[6]
                novo_associado.turno_volta = linha[7]
                return novo_associado
            return None
        except Exception as e:
            print(f"Erro ao buscar associado por CPF: {e}")
            return None
        finally:
            if cursor: 
                cursor.close()

    def atualizar(self, associado: Associado):
        # Atualiza os dados de um associado pela chave do CPF (UPDATE)
        if not self.conexao:
            return False, "Sem conexão com o banco de dados"
            
        cursor = None
        sql = """
            UPDATE associado 
            SET nome = %s,dias_semana = %s, telefone = %s, turno_ida = %s, turno_volta = %s
            WHERE cpf = %s;
        """
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql, (
                associado.nome,
                associado.dias_semana,
                associado.telefone,
                associado.turno_ida,  
                associado.turno_volta,
                associado.cpf

                
            ))
            self.conexao.commit()
            return True, "Dados do associado atualizados com sucesso"
        except Exception as e:
            self.conexao.rollback() # Desfaz em caso de falha no meio do processo
            print(f"Erro ao atualizar associado: {e}")
            return False, f"Erro ao atualizar associado: {e}"
        finally:
            if cursor: 
                cursor.close()

    def remover(self, cpf: str):
        # Remove um associado do banco pelo CPF (DELETE) 
        if not self.conexao:
            return False, "Sem conexão com o banco de dados"
            
        cursor = None
        sql = "DELETE FROM associado WHERE cpf = %s;"
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql, (cpf,))
            self.conexao.commit() # Confirma a exclusão física do registro
            return True, "Associado removido com sucesso"
        except Exception as e:
            self.conexao.rollback()
            print(f"Erro ao remover associado: {e}")
            return False, f"Erro ao remover associado: {e}"
        finally:
            if cursor: 
                cursor.close()