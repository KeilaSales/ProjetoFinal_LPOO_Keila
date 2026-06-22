# CAMADA VIEW: Painel Avançado de Logística e Ocupação por Turnos (Tkinter)
import tkinter as tk
from tkinter import messagebox, ttk
from controler.fretamento_controller import FretamentoController


class GerenciamentoFretamentoView:
    def __init__(self, root, controller):
        self.root = root
        self.fretamento_controller = FretamentoController(controller)
        self.inicializar_tela_fretamento()

    def inicializar_tela_fretamento(self):
        #Cria a janela principal de análise de fluxos por turno
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
        
        #Titulo do cabeçalho
        self.tabela_frota.heading("Dia", text="Dia Útil")
        self.tabela_frota.heading("Ida Manhã", text="Ida Manhã")
        self.tabela_frota.heading("Volta Manhã", text="Volta Manhã")
        self.tabela_frota.heading("Ida Tarde", text="Ida Tarde")
        self.tabela_frota.heading("Volta Tarde", text="Volta Tarde")
        self.tabela_frota.heading("Ida Noite", text="Ida Noite")
        self.tabela_frota.heading("Volta Noite", text="Volta Noite")

        self.tabela_frota.column("Dia", width=110, anchor="center")

# Loop para configurar a largura padrão de todas as colunas numéricas de turno
        for col in colunas_frota[1:]:
            self.tabela_frota.column(col, width=95, anchor="center")
       
        self.tabela_frota.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

# Dispara o processamento matemático para preencher os números na tela
        self.atualizar_frota()
        
        frame_botoes = tk.Frame(self.window)
        frame_botoes.pack(pady=15)

        #Abre a sub-janela com a recomendação inteligente de veículo para o dia clicado
        tk.Button(frame_botoes, text="Analisar Transporte para o Dia", font=("Arial", 10, "bold"), bg="#2ecc71", fg="white", width=28, command=self.abrir_analise_veiculo).pack(side=tk.LEFT, padx=5)
        tk.Button(self.window, text="Fechar Painel de Logística", font=("Arial", 9), bg="#34495e", fg="white", width=25, command=self.window.destroy).pack(pady=15)

    def atualizar_frota(self):
        # View delegando a contagem de dados para a camada Controller
        for row in self.tabela_frota.get_children(): 
            self.tabela_frota.delete(row)

        # Solicita a matriz de contagem processada pelo controlador de fretamento
        self.contagem_global = self.fretamento_controller.gerar_matriz_contagem()

        dias_uteis = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
        for dia in dias_uteis:
            c = self.contagem_global[dia]
            self.tabela_frota.insert("", tk.END, values=(dia, c["IM"], c["VM"], c["IT"], c["VT"], c["IN"], c["VN"]))
        
    def abrir_analise_veiculo(self):
         #Abre a janela interna pedindo as decisões de veículos para o Controller 
        selecao = self.tabela_frota.selection() # Pega a linha que o usuário selecionou
        if not selecao:
            messagebox.showwarning("Aviso", "Por favor, selecione um dia da semana na tabela primeiro!")
            return
            
        valores = self.tabela_frota.item(selecao, "values")
        dia_selecionado = valores[0] #Extrai o nome do dia util clicado
        
        c = self.contagem_global[dia_selecionado] #Captura a contagem daquele dia em especifico 
            
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
        

        # OTIMIZAÇÃO MVC: A View envia o pico de passageiros e o Controller devolve o texto do veículo resolvido
        sugestao_manha = self.fretamento_controller.decidir_veiculo(max(c['IM'], c['VM']))
        sugestao_tarde = self.fretamento_controller.decidir_veiculo(max(c['IT'], c['VT']))
        sugestao_noite = self.fretamento_controller.decidir_veiculo(max(c['IN'], c['VN']))

        
        # ALGORITMO DE OTIMIZAÇÃO (MÁXIMO): Usa a função max() para dimensionar o veículo
        # pelo maior número entre a Ida e a Volta daquele turno, evitando que falte espaço.
        tabela_interna.insert("", tk.END, values=("Manhã", f"{c['IM']} ida / {c['VM']} volta", sugestao_manha))
        tabela_interna.insert("", tk.END, values=("Tarde", f"{c['IT']} ida / {c['VT']} volta", sugestao_tarde))
        tabela_interna.insert("", tk.END, values=("Noite", f"{c['IN']} ida / {c['VN']} volta", sugestao_noite))

        tk.Button(janela_sugestao, text="Fechar Análise", font=("Arial", 9), width=15, command=janela_sugestao.destroy).pack(pady=15)
     
        
       