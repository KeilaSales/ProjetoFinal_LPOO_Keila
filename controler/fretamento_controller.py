# ====================================================================
# CAMADA CONTROLLER: Centraliza a inteligência e regras de logística
# ====================================================================

class FretamentoController:
    def __init__(self, associado_controller):
        # INJEÇÃO DE DEPENDÊNCIA: Reaproveita o controlador geral para ler os dados do banco
        self.associado_controller = associado_controller

    def gerar_matriz_contagem(self) -> dict:
        # Varre os dados recuperados do banco e monta o cruzamento Dia x Turno 
        try:
            # Busca a lista de objetos cadastrados diretamente do banco de dados
            lista = self.associado_controller.buscar_todos()
        except Exception as e:
            print(f"Erro ao buscar associados no controller: {e}")
            lista = []

        dias_uteis = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
        
        # MATRIZ DE CONTAGEM: Inicializa os contadores de cada turno zerados por dia útil
        # IM (Ida Manhã), VM (Volta Manhã), IT (Ida Tarde), VT (Volta Tarde), IN (Ida Noite), VN (Volta Noite)
        contagem = {dia: {"IM": 0, "VM": 0, "IT": 0, "VT": 0, "IN": 0, "VN": 0} for dia in dias_uteis}
        
        for u in lista:
            if not u.dias_semana:
                continue

            # Quebra a string "Segunda,Terça" armazenada no banco em uma lista real de palavras
            dias_aluno = [d.strip() for d in str(u.dias_semana).split(",")]
            
            # Recuperação segura dos atributos de turno com fallback para "Noite" caso estejam nulos
            turno_ida = getattr(u, 'turno_ida', 'Noite') if getattr(u, 'turno_ida', 'Noite') else "Noite"
            turno_volta = getattr(u, 'turno_volta', 'Noite') if getattr(u, 'turno_volta', 'Noite') else "Noite"
            
            # Percorre os dias do aluno e incrementa o turno exato de ida e volta na matriz
            for dia in dias_aluno:
                if dia in contagem:
                    if turno_ida == "Manhã": contagem[dia]["IM"] += 1
                    elif turno_ida == "Tarde": contagem[dia]["IT"] += 1
                    elif turno_ida == "Noite": contagem[dia]["IN"] += 1
                    
                    if turno_volta == "Manhã": contagem[dia]["VM"] += 1
                    elif turno_volta == "Tarde": contagem[dia]["VT"] += 1
                    elif turno_volta == "Noite": contagem[dia]["VN"] += 1
                    
        return contagem

    def decidir_veiculo(self, quantidade_passageiros: int) -> str:
        """ REGRA DE NEGÓCIO: Define o tamanho do veículo baseado na faixa de capacidade """
        if quantidade_passageiros == 0: 
            return "Nenhum transporte necessário"
        elif quantidade_passageiros <= 15: 
            return "Alocar Van Executiva (Capacidade: 15)"
        elif quantidade_passageiros <= 28: 
            return "Alocar Micro-ônibus (Capacidade: 28)"
        else: 
            return "Alocar Ônibus Fretado Convencional"