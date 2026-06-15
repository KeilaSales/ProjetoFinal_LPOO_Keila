import sys
import os

from model.Rota import Rota
from dao.db_config import DatabaseConfig
from dao.Generic_dao import GenericDAO

class RotaDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    def salvar(self, rota: Rota):
        if not self.conexao:
            return False, "Sem conexão com o banco"
        cursor = None
        sql = "INSERT INTO rota (destino, itinerario, capacidade_maxima, vagas_disponiveis) VALUES (%s, %s, %s, %s);"
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql, (rota.destino, rota.itinerario, rota.capacidade_maxima, rota.vagas_disponiveis))
            self.conexao.commit()
            return True, "Rota cadastrada com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao salvar rota: {e}"
        finally:
            if cursor: cursor.close()

    def listar_todos(self):
        if not self.conexao: return []
        cursor = None
        sql = "SELECT id_rota, destino, itinerario, capacidade_maxima, vagas_disponiveis FROM rota;"
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql)
            linhas = cursor.fetchall()
            rotas = []
            for l in linhas:
                # Instancia o objeto Rota mapeando os dados do banco
                r = Rota()
                r.id_rota, r.destino, r.itinerario, r.capacidade_maxima, r.vagas_disponiveis = l
                rotas.append(r)
            return rotas
        except Exception as e:
            print(f"Erro ao listar rotas: {e}")
            return []
        finally:
            if cursor: cursor.close()

    def remover(self, id_rota: int):
        if not self.conexao: return False, "Sem conexão"
        cursor = None
        sql = "DELETE FROM rota WHERE id_rota = %s;"
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql, (id_rota,))
            self.conexao.commit()
            return True, "Rota removida com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao remover: {e}"
        finally:
            if cursor: cursor.close()

    def atualizar(self, rota: Rota):
        if not self.conexao: return False, "Sem conexão"
        cursor = None
        sql = "UPDATE rota SET destino=%s, itinerario=%s, capacidade_maxima=%s, vagas_disponiveis=%s WHERE id_rota=%s;"
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql, (rota.destino, rota.itinerario, rota.capacidade_maxima, rota.vagas_disponiveis, rota.id_rota))
            self.conexao.commit()
            return True, "Rota atualizada com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao atualizar: {e}"
        finally:
            if cursor: cursor.close()