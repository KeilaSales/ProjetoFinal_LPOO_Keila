import sys
import os

from model.Inscricao import Inscricao
from dao.db_config import DatabaseConfig
from dao.Generic_dao import GenericDAO

class InscricaoDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    def salvar(self, inscricao: Inscricao):
        if not self.conexao: return False, "Sem conexão"
        cursor = None
        sql = """
            INSERT INTO inscricao (cpf_associado, id_rota, turno, dias_semana, valor_mensalidade) 
            VALUES (%s, %s, %s, %s, %s);
        """
        try:
            cursor = self.conexao.cursor()
            # Transforma a lista de dias em string simples para persistência
            dias_str = ",".join(inscricao.dias_semana) if isinstance(inscricao.dias_semana, list) else inscricao.dias_semana
            cursor.execute(sql, (
                inscricao.associado.cpf, 
                inscricao.rota.id_rota, 
                inscricao.turno, 
                dias_str, 
                inscricao.valor_mensalidade
            ))
            self.conexao.commit()
            return True, "Inscrição realizada com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao inscrever: {e}"
        finally:
            if cursor: cursor.close()

    def listar_todos(self):
        # Implementação básica de leitura necessária para a listagem na Treeview
        if not self.conexao: return []
        cursor = None
        sql = "SELECT id_inscricao, cpf_associado, id_rota, turno, dias_semana, valor_mensalidade FROM inscricao;"
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar inscrições: {e}")
            return []
        finally:
            if cursor: cursor.close()

    def remover(self, id_inscricao: int):
        if not self.conexao: return False, "Sem conexão"
        cursor = None
        sql = "DELETE FROM inscricao WHERE id_inscricao = %s;"
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql, (id_inscricao,))
            self.conexao.commit()
            return True, "Inscrição cancelada com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao remover: {e}"
        finally:
            if cursor: cursor.close()

    def atualizar(self, inscricao: Inscricao):
        if not self.conexao: return False, "Sem conexão"
        cursor = None
        sql = "UPDATE inscricao SET turno=%s, dias_semana=%s, valor_mensalidade=%s WHERE id_inscricao=%s;"
        try:
            cursor = self.conexao.cursor()
            dias_str = ",".join(inscricao.dias_semana) if isinstance(inscricao.dias_semana, list) else inscricao.dias_semana
            cursor.execute(sql, (inscricao.turno, dias_str, inscricao.valor_mensalidade, inscricao.id_inscricao))
            self.conexao.commit()
            return True, "Inscrição modificada com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao atualizar: {e}"
        finally:
            if cursor: cursor.close()