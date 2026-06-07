import psycopg2

class Database:
    @staticmethod
    def conectar():
        try:
            conexao = psycopg2.connect(
                host="localhost",
                database="Sistema_Transporte", 
                user="postgres",              
                password="postgres",  
                port=5432
            )
            
            # Garante que o banco e o Python conversem na mesma codificação de texto
            conexao.set_client_encoding('UTF8')
            return conexao
            
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None