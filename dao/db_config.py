# CONFIGURAÇÃO: Centraliza os parâmetros de rede e login do BD
import psycopg2
from psycopg2 import Error

class DatabaseConfig: 
    # MÉTODO ESTÁTICO: Pode ser chamado diretamente sem precisar criar um objeto da classe (DatabaseConfig.get_connection())
    @staticmethod
    def get_connection():
        try:
            conexao = psycopg2.connect(
                user="postgres",
                password="postgres", 
                host="localhost",
                port="5432", # Porta padrão do serviço PostgreSQL
                database="lpoo_projeto_keila"
            )
            return conexao
        except Error as e:
            print(f"Erro ao conectar ao PostgreSQL: {e}")
            return None