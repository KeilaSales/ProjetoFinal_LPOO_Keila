import psycopg2
from psycopg2 import Error

class DatabaseConfig: 
    @staticmethod
    def get_connection():
        try:
            conexao = psycopg2.connect(
                user="postgres",
                password="postgres", 
                host="localhost",
                port="5432",
                database="Sistema_Transporte"
            )
            return conexao
        except Error as e:
            print(f"Erro ao conectar ao PostgreSQL: {e}")
            return None