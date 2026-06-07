from config.Database import Database
from model.Associado import Associado

class AssociadoDAO:
    
    def salvar(self, associado: Associado):
        
        sql = """
            INSERT INTO associado (nome, cpf, matricula, telefone, tipo_associado, senha)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        conexao = Database.conectar()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(sql, (
                    associado.nome, 
                    associado.cpf, 
                    associado.matricula, 
                    associado.telefone,  
                    associado.tipo_associado, 
                    associado.senha
                ))
                conexao.commit()
                print("Associado salvo com sucesso no banco!")
            except Exception as e:
                print(f"Erro ao salvar associado: {e}")
            finally:
                cursor.close()
                conexao.close()

    def buscar_por_cpf(self, cpf: str):
        # Adicionamos o telefone no SELECT
        sql = "SELECT nome, cpf, matricula, telefone, tipo_associado, senha FROM associado WHERE cpf = %s;"
        conexao = Database.conectar()  
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(sql, (cpf,))
                resultado = cursor.fetchone()
                
                if resultado:
                    # Mapeamos as 6 colunas retornadas do banco na ordem correta
                    return Associado(
                        nome=resultado[0], 
                        cpf=resultado[1], 
                        matricula=resultado[2], 
                        telefone=resultado[3],  # Pegando o telefone do banco
                        tipo_associado=resultado[4],
                        senha=resultado[5]
                    )
                return None
            except Exception as e:
                print(f"Erro ao buscar associado: {e}")
            finally:
                cursor.close()
                conexao.close()

    def atualizar(self, associado: Associado):
        sql = """
            UPDATE associado 
            SET nome = %s, matricula = %s, tipo_associado = %s, senha = %s 
            WHERE cpf = %s;
        """
        conexao = Database.conectar()  # Corrigido aqui de get_connection para conectar()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(sql, (
                    associado.nome, 
                    associado.matricula, 
                    associado.tipo_associado, 
                    associado.senha, 
                    associado.cpf
                ))
                conexao.commit()
                print("Associado atualizado com sucesso!")
            except Exception as e:
                print(f"Erro ao atualizar associado: {e}")
            finally:
                cursor.close()
                conexao.close()

    def deletar(self, cpf: str):
        sql = "DELETE FROM associado WHERE cpf = %s;"
        conexao = Database.conectar()  # Corrigido aqui de get_connection para conectar()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(sql, (cpf,))
                conexao.commit()
                print("Associado deletado com sucesso!")
            except Exception as e:
                print(f"Erro ao deletar associado: {e}")
            finally:
                cursor.close()
                conexao.close()