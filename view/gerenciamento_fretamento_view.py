import tkinter as tk
from tkinter import messagebox, ttk

class GerenciamentoFretamentoView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        # 🎯 BARREIRA DE SEGURANÇA: Só abre com senha da diretoria
        self.solicitar_acesso_diretoria()

    def solicitar_acesso_diretoria(self):
        self.janela_login = tk.Toplevel(self.root)
        self.janela_login.title("Segurança - Diretoria de Logística")
        self.janela_login.geometry("360x240")
        self.janela_login.resizable(False, False)
        self.janela_login.transient(self.root)
        self.janela_login.grab_set()
        
        tk.Label(self.janela_login, text="Área Restrita: Diretoria de Logística", font=("Arial", 11, "bold"), fg="#1a365d").pack(pady=15)
        tk.Label(self.janela_login, text="Digite a Senha de Fretamento:", font=("Arial", 10)).pack(pady=2)
        
        self.txt_senha = tk.Entry(self.janela_login, show="*", width=22, font=("Arial", 10))
        self.txt_senha.pack(pady=10)
        
        btn_validar = tk.Button(self.janela_login, text="Acessar Painel", bg="#1a365d", fg="white", font=("Arial", 9, "bold"), width=15, command=self.validar_senha_diretoria)
        btn_validar.pack(pady=5)
        
        btn_sair = tk.Button(self.janela_login, text="Cancelar", bg="#95a5a6", fg="white", font=("Arial", 9), width=15, command=self.janela_login.destroy)
        btn_sair.pack(pady=5)

    def validar_senha_diretoria(self):
        if self.txt_senha.get() == "frotadir123":
            self.janela_login.destroy()
            self.inicializar_tela_fretamento()
        else:
            messagebox.showerror("Acesso Negado", "Senha de controle de fretamento incorreta!")

    def inicializar_tela_fretamento(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Painel de Controle da Diretoria - Fretamento")
        self.window.geometry("980x420")
        self.window.resizable(False, False)
        self.window.transient(self.root)
        self.window.lift()
        
        tk.Label(self.window, text="Logística de Ocupação Detalhada de Frota por Turno", font=("Arial", 14, "bold"), fg="#1a365d").pack(pady=15)
        
        # 🎯 A TABELA DO FRETAMENTO DENTRO DA PARTE DA DIRETORIA
        colunas_frota = ("Dia", "Ida Manhã", "Volta Manhã", "Ida Tarde", "Volta Tarde", "Ida Noite", "Volta Noite", "Frota Recomendada")
        self.tabela_frota = ttk.Treeview(self.window, columns=colunas_frota, show="headings", height=6)
        
        self.tabela_frota.heading("Dia", text="Dia Útil")
        self.tabela_frota.heading("Ida Manhã", text="Ida Manhã")
        self.tabela_frota.heading("Volta Manhã", text="Volta Manhã")
        self.tabela_frota.heading("Ida Tarde", text="Ida Tarde")
        self.tabela_frota.heading("Volta Tarde", text="Volta Tarde")
        self.tabela_frota.heading("Ida Noite", text="Ida Noite")
        self.tabela_frota.heading("Volta Noite", text="Volta Noite")
        self.tabela_frota.heading("Frota Recomendada", text="Sugestão de Transporte Adequado")
        
        for col in colunas_frota[:-1]:
            self.tabela_frota.column(col, width=95, anchor="center")
        self.tabela_frota.column("Frota Recomendada", width=245, anchor="w")
        self.tabela_frota.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        self.atualizar_frota()
        
        tk.Button(self.window, text="Fechar Painel de Logística", font=("Arial", 9), bg="#34495e", fg="white", width=25, command=self.window.destroy).pack(pady=15)

    def atualizar_frota(self):
        for row in self.tabela_frota.get_children(): 
            self.tabela_frota.delete(row)
        lista = self.controller.buscar_todos()
        
        cronograma = {"Segunda": 0, "Terça": 0, "Quarta": 0, "Quinta": 0, "Sexta": 0}
        for u in lista:
            if u.dias_semana:
                for dia in str(u.dias_semana).split(","):
                    if dia.strip() in cronograma:
                        cronograma[dia.strip()] += 1
                        
        for dia, total_dia in cronograma.items():
            if total_dia == 0: frota = "Nenhum Fretamento Ativo para o Dia"
            elif total_dia <= 15: frota = "Alocar Van Executiva (Capacidade: 15)"
            elif total_dia <= 28: frota = "Alocar Micro-ônibus (Capacidade: 28)"
            else: frota = "Alocar Ônibus Fretado Convencional"
            
            # Preenche a listagem logística com base nos dados reais vindos do banco
            self.tabela_frota.insert("", tk.END, values=(dia, 0, 0, 0, 0, total_dia, total_dia, frota))