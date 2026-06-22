# CAMADA DAO: Gerencia a persistência da tabela física de Rotas
import sys
import os

from model.Rota import Rota
from dao.db_config import DatabaseConfig
from dao.Generic_dao import GenericDAO

# POLIMORFISMO E HERANÇA: Assina o contrato com o GenericDAO implementando o CRUD completo
class RotaDAO(GenericDAO):
    def __init__(self):
        #Captura a conexão ativa com o BD
        self.conexao = DatabaseConfig.get_connection()

    def salvar(self, rota: Rota):
        # CREATE - Insere uma rota física no sistema
        if not self.conexao:
            return False, "Sem conexão com o banco"
        cursor = None
        sql = "INSERT INTO rota (destino, itinerario, capacidade_maxima, vagas_disponiveis) VALUES (%s, %s, %s, %s);"
        try:
            cursor = self.conexao.cursor()
            # Mapeia as propriedades do objeto Rota para os marcadores %s
            cursor.execute(sql, (rota.destino, rota.itinerario, rota.capacidade_maxima, rota.vagas_disponiveis))
            self.conexao.commit()
            return True, "Rota cadastrada com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao salvar rota: {e}"
        finally:
            if cursor: cursor.close()

    def listar_todos(self):
        #READ - Lista todos os trajetos ativos
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
                # INSTANCIAÇÃO: Cria o objeto da Model preenchendo seus atributos linha por linha
                r.id_rota, r.destino, r.itinerario, r.capacidade_maxima, r.vagas_disponiveis = l
                rotas.append(r) #Devolve a lista cheia 
            return rotas
        except Exception as e:
            print(f"Erro ao listar rotas: {e}")
            return []
        finally:
            if cursor: cursor.close()

    def remover(self, id_rota: int):
        #Delete - REmove a rota do sistema com base na chave primária 
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
        #Update - Altera informações de itinerário ou capacidade da rota
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