import psycopg2

class Database:
    @staticmethod
    def conectar():
        try:
            conexao = psycopg2.connect(
                host="localhost",
                database="Sistema_Transporte", 
                user="postgres",              
                password="postgress",  # Verifique se essa é sua senha real
                port=5432
            )
            conexao.set_client_encoding('UTF8')
            return conexao
            
        except UnicodeDecodeError as ude:
            # Se o erro for de texto/encoding, nós capturamos ele aqui de forma limpa!
            print("\n[Aviso] O Windows gerou uma mensagem de erro com acentos que o Python não conseguiu ler.")
            print("Isso geralmente significa uma das duas coisas:")
            print("1. A senha 'postgres' está incorreta para o seu banco local.")
            print("2. O banco de dados chamado 'Sistema_Transporte' não foi criado no seu pgAdmin.\n")
            return None
            
        except Exception as e:
            # Qualquer outro erro cai aqui
            try:
                erro_limpo = str(e).encode('utf-8', errors='replace').decode('utf-8', errors='replace')
                print(f"Erro ao conectar ao banco de dados: {erro_limpo}")
            except:
                print("Erro ao conectar ao banco de dados (erro de comunicação/autenticação).")
            return None