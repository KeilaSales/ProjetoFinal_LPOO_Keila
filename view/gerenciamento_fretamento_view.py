import tkinter as tk
from tkinter import messagebox, ttk

class GerenciamentoFretamentoView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.inicializar_tela_fretamento()

    def inicializar_tela_fretamento(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Painel de Controle da Diretoria - Fretamento")
        self.window.geometry("980x420")
        self.window.resizable(False, False)
        self.window.transient(self.root)
        self.window.lift()
        
        tk.Label(self.window, text="Logística de Ocupação Detalhada de Frota por Turno", font=("Arial", 14, "bold"), fg="#1a365d").pack(pady=15)
        
        # TABELA DO FRETAMENTO DENTRO DA PARTE DA DIRETORIA
        colunas_frota = ("Dia", "Ida Manhã", "Volta Manhã", "Ida Tarde", "Volta Tarde", "Ida Noite", "Volta Noite")
        self.tabela_frota = ttk.Treeview(self.window, columns=colunas_frota, show="headings", height=6)
        
        self.tabela_frota.heading("Dia", text="Dia Útil")
        self.tabela_frota.heading("Ida Manhã", text="Ida Manhã")
        self.tabela_frota.heading("Volta Manhã", text="Volta Manhã")
        self.tabela_frota.heading("Ida Tarde", text="Ida Tarde")
        self.tabela_frota.heading("Volta Tarde", text="Volta Tarde")
        self.tabela_frota.heading("Ida Noite", text="Ida Noite")
        self.tabela_frota.heading("Volta Noite", text="Volta Noite")

        self.tabela_frota.column("Dia", width=110, anchor="center")
        
        for col in colunas_frota[1:]:
            self.tabela_frota.column(col, width=95, anchor="center")
       
        self.tabela_frota.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.atualizar_frota()
        
        frame_botoes = tk.Frame(self.window)
        frame_botoes.pack(pady=15)

        tk.Button(frame_botoes, text="Analisar Transporte para o Dia", font=("Arial", 10, "bold"), bg="#2ecc71", fg="white", width=28, command=self.abrir_analise_veiculo).pack(side=tk.LEFT, padx=5)
        tk.Button(self.window, text="Fechar Painel de Logística", font=("Arial", 9), bg="#34495e", fg="white", width=25, command=self.window.destroy).pack(pady=15)

    def atualizar_frota(self):
        for row in self.tabela_frota.get_children(): 
            self.tabela_frota.delete(row)

        try:
            lista = self.controller.buscar_todos()
        except Exception as e:
            print(f"Erro ao buscar associados: {e}")
            lista = []

        dias_uteis = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
        
          #IM (Ida Manhã), VM (Volta Manhã), IT (Ida Tarde), VT (Volta Tarde), IN (Ida Noite), VN (Volta Noite)
        self.contagem_global = {dia: {"IM": 0, "VM": 0, "IT": 0, "VT": 0, "IN": 0, "VN": 0} for dia in dias_uteis}
        
        for u in lista:
            if not u.dias_semana:
                continue
                
            dias_aluno = [d.strip() for d in str(u.dias_semana).split(",")]
            
            # Obtém os turnos salvos no banco (usa "Noite" como padrão caso esteja nulo)
            turno_ida = getattr(u, 'turno_ida', 'Noite') if getattr(u, 'turno_ida', 'Noite') else "Noite"
            turno_volta = getattr(u, 'turno_volta', 'Noite') if getattr(u, 'turno_volta', 'Noite') else "Noite"
            
            for dia in dias_aluno:
                if dia in self.contagem_global:
                    # Incrementa a contagem exata da IDA baseada no turno do aluno
                    if turno_ida == "Manhã": self.contagem_global[dia]["IM"] += 1
                    elif turno_ida == "Tarde": self.contagem_global[dia]["IT"] += 1
                    elif turno_ida == "Noite": self.contagem_global[dia]["IN"] += 1
                    
                    # Incrementa a contagem exata da VOLTA baseada no turno do aluno
                    if turno_volta == "Manhã": self.contagem_global[dia]["VM"] += 1
                    elif turno_volta == "Tarde": self.contagem_global[dia]["VT"] += 1
                    elif turno_volta == "Noite": self.contagem_global[dia]["VN"] += 1
                        
        for dia in dias_uteis:
            c = self.contagem_global[dia]
            self.tabela_frota.insert("", tk.END, values=(dia, c["IM"], c["VM"], c["IT"], c["VT"], c["IN"], c["VN"]))

    def abrir_analise_veiculo(self):
        selecao = self.tabela_frota.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Por favor, selecione um dia da semana na tabela primeiro!")
            return
            
        valores = self.tabela_frota.item(selecao, "values")
        dia_selecionado = valores[0]
        
        c = self.contagem_global[dia_selecionado]
        
        def calcular_veiculo(qtd):
            if qtd == 0: return "Nenhum transporte necessário"
            elif qtd <= 15: return "Alocar Van Executiva (Capacidade: 15)"
            elif qtd <= 28: return "Alocar Micro-ônibus (Capacidade: 28)"
            else: return "Alocar Ônibus Fretado Convencional"
            
        janela_sugestao = tk.Toplevel(self.window)
        janela_sugestao.title(f"Sugestão de Frota - {dia_selecionado}")
        janela_sugestao.geometry("560x320")
        janela_sugestao.resizable(False, False)
        janela_sugestao.transient(self.window)
        janela_sugestao.grab_set()
        
        tk.Label(janela_sugestao, text=f"Frota Recomendada para: {dia_selecionado}", font=("Arial", 12, "bold"), fg="#1a365d").pack(pady=15)
        
        colunas_sugestao = ("Turno", "Passageiros (Ida / Volta)", "Veículo Recomendado")
        tabela_interna = ttk.Treeview(janela_sugestao, columns=colunas_sugestao, show="headings", height=3)
        
        tabela_interna.heading("Turno", text="Turno")
        tabela_interna.heading("Passageiros (Ida / Volta)", text="Passageiros (Ida / Volta)")
        tabela_interna.heading("Veículo Recomendado", text="Veículo Recomendado")
        
        tabela_interna.column("Turno", width=90, anchor="center")
        tabela_interna.column("Passageiros (Ida / Volta)", width=150, anchor="center")
        tabela_interna.column("Veículo Recomendado", width=280, anchor="w")
        tabela_interna.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)
        
        tabela_interna.insert("", tk.END, values=("Manhã", f"{c['IM']} ida / {c['VM']} volta", calcular_veiculo(max(c['IM'], c['VM']))))
        tabela_interna.insert("", tk.END, values=("Tarde", f"{c['IT']} ida / {c['VT']} volta", calcular_veiculo(max(c['IT'], c['VT']))))
        tabela_interna.insert("", tk.END, values=("Noite", f"{c['IN']} ida / {c['VN']} volta", calcular_veiculo(max(c['IN'], c['VN']))))
        
        tk.Button(janela_sugestao, text="Fechar Análise", font=("Arial", 9), width=15, command=janela_sugestao.destroy).pack(pady=15)
     
        
       