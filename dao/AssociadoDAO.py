import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.Associado import Associado
from dao.db_config import DatabaseConfig
from dao.Generic_dao import GenericDAO

class AssociadoDAO(GenericDAO):
    def __init__(self):
        # Retém a conexão no construtor da classe igual ao VeiculoDAO dela
        self.conexao = DatabaseConfig.get_connection()
        
    def salvar(self, associado: Associado):
        """ Insere um novo associado no banco de dados (CREATE) """
        if not self.conexao:
            return False, "Sem conexão com o banco de dados"
            
        cursor = None
        sql = """
            INSERT INTO associado (nome, cpf, matricula, telefone, tipo_associado, dias_semana, turno_ida, turno_volta)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            cursor = self.conexao.cursor()
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
            self.conexao.commit()
            print("Associado salvo com sucesso no banco!")
            return True, "Associado cadastrado com sucesso"
        except Exception as e:
            self.conexao.rollback() # Regra estrita dela: desfaz em caso de erro
            print(f"Erro ao inserir associado: {e}")
            return False, f"Erro ao inserir associado: {e}"
        finally:
            if cursor: 
                cursor.close()

    def listar_todos(self):
        """ Retorna todos os associados cadastrados (READ ALL) """
        if not self.conexao:
            return []
            
        cursor = None
        sql = "SELECT nome, cpf, matricula, telefone, tipo_associado, dias_semana, turno_ida, turno_volta FROM associado ORDER BY nome;"
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql)
            linhas = cursor.fetchall()
            
            # Converte a lista de tuplas do Postgres em uma lista de objetos Associado
            associados = []
            for linha in linhas:
                obj = Associado(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5])
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
        """ Busca um associado específico pelo CPF """
        if not self.conexao:
            return None
            
        cursor = None
        sql = "SELECT nome, cpf, matricula, telefone, tipo_associado, dias_semana, turno_ida, turno_volta FROM associado WHERE cpf = %s;"
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql, (cpf,))
            linha = cursor.fetchone()
            
            if linha:
                novo_associado = Associado(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5])
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
        """ Atualiza os dados de um associado pela chave do CPF (UPDATE) """
        if not self.conexao:
            return False, "Sem conexão com o banco de dados"
            
        cursor = None
        sql = """
            UPDATE associado 
            SET nome = %s, matricula = %s, telefone = %s, tipo_associado = %s, senha = %s 
            WHERE cpf = %s;
        """
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql, (
                associado.nome, 
                associado.matricula, 
                associado.telefone, 
                associado.tipo_associado, 
                associado.senha,
                associado.cpf
            ))
            self.conexao.commit()
            return True, "Dados do associado atualizados com sucesso"
        except Exception as e:
            self.conexao.rollback()
            print(f"Erro ao atualizar associado: {e}")
            return False, f"Erro ao atualizar associado: {e}"
        finally:
            if cursor: 
                cursor.close()

    def remover(self, cpf: str):
        """ Remove um associado do banco pelo CPF (DELETE) """
        if not self.conexao:
            return False, "Sem conexão com o banco de dados"
            
        cursor = None
        sql = "DELETE FROM associado WHERE cpf = %s;"
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql, (cpf,))
            self.conexao.commit()
            return True, "Associado removido com sucesso"
        except Exception as e:
            self.conexao.rollback()
            print(f"Erro ao remover associado: {e}")
            return False, f"Erro ao remover associado: {e}"
        finally:
            if cursor: 
                cursor.close()