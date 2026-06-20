import tkinter as tk
from tkinter import messagebox, ttk
from dao.AssociadoDAO import AssociadoDAO
from model.Associado import Associado
from model.CalculoMensalidade import ContextoMensalidade

class MenuPrincipalFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.associado_dao = AssociadoDAO()
        
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.mostrar_tela_inscricao()

    def mostrar_tela_inscricao(self):
        for widget in self.container.winfo_children():
            widget.destroy()
            
        tk.Label(self.container, text="ALU - Associação Lagoense de Universitários", font=("Arial", 16, "bold"), fg="#1a365d").grid(row=0, column=0, columnspan=4, pady=10)
        tk.Label(self.container, text="Portal de Inscrição do Universitário", font=("Arial", 11, "italic"), fg="#4a5568").grid(row=1, column=0, columnspan=4, pady=5)
        
        # --- CAMPOS DE CADASTRO ---
        tk.Label(self.container, text="Nome Completo:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=5)
        self.txt_nome = tk.Entry(self.container, width=30, font=("Arial", 10))
        self.txt_nome.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        
        tk.Label(self.container, text="CPF (Apenas números):", font=("Arial", 10, "bold")).grid(row=2, column=2, sticky="w", pady=5)
        self.txt_cpf = tk.Entry(self.container, width=20, font=("Arial", 10))
        self.txt_cpf.grid(row=2, column=3, pady=5, padx=5, sticky="w")
        
        # MUDANÇA AQUI: Campo de seleção com as Universidades solicitadas
        tk.Label(self.container, text="Faculdade / Universidade:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=5)
        self.cb_faculdade = ttk.Combobox(self.container, values=[
            "Universidade de Passo Fundo (UPF)", 
            "Instituto Federal Sul-rio-grandense (IFSul)", 
            "Universidade Federal da Fronteira Sul (UFFS)", 
            "Atitus Educação", 
            "Anhanguera", 
            "IDEAU", 
            "Outros"
        ], width=27, state="readonly", font=("Arial", 10))
        self.cb_faculdade.grid(row=3, column=1, pady=5, padx=5, sticky="w")
        self.cb_faculdade.set("Universidade de Passo Fundo (UPF)") # Valor padrão
        
        tk.Label(self.container, text="Nº Matrícula:", font=("Arial", 10, "bold")).grid(row=3, column=2, sticky="w", pady=5)
        self.txt_matricula = tk.Entry(self.container, width=20, font=("Arial", 10))
        self.txt_matricula.grid(row=3, column=3, pady=5, padx=5, sticky="w")

        tk.Label(self.container, text="Telefone de Contato:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", pady=5)
        self.txt_telefone = tk.Entry(self.container, width=30, font=("Arial", 10))
        self.txt_telefone.grid(row=4, column=1, pady=5, padx=5, sticky="w")
        
        tk.Label(self.container, text="Vínculo ALU:", font=("Arial", 10, "bold")).grid(row=4, column=2, sticky="w", pady=5)
        self.cb_tipo = ttk.Combobox(self.container, values=["NOVO", "ANTIGO"], width=17, state="readonly", font=("Arial", 10))
        self.cb_tipo.grid(row=4, column=3, pady=5, padx=5, sticky="w")
        self.cb_tipo.set("NOVO")

        tk.Label(self.container, text="Turno de IDA:", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky="w", pady=5)
        self.cb_ida = ttk.Combobox(self.container, values=["Manhã", "Tarde", "Noite"], width=27, state="readonly", font=("Arial", 10))
        self.cb_ida.grid(row=5, column=1, pady=5, padx=5, sticky="w")
        self.cb_ida.set("Noite")

        tk.Label(self.container, text="Turno de VOLTA:", font=("Arial", 10, "bold")).grid(row=5, column=2, sticky="w", pady=5)
        self.cb_volta = ttk.Combobox(self.container, values=["Manhã", "Tarde", "Noite"], width=17, state="readonly", font=("Arial", 10))
        self.cb_volta.grid(row=5, column=3, pady=5, padx=5, sticky="w")
        self.cb_volta.set("Noite")

        # --- SELEÇÃO DE DIAS ESPECÍFICOS DA SEMANA ---
        tk.Label(self.container, text="Selecione os dias que utilizará o transporte:", font=("Arial", 10, "bold"), fg="#1a365d").grid(row=6, column=0, columnspan=4, pady=10, sticky="w")
        
        self.dias_vars = {
            "Segunda": tk.BooleanVar(), "Terça": tk.BooleanVar(),
            "Quarta": tk.BooleanVar(), "Quinta": tk.BooleanVar(), "Sexta": tk.BooleanVar()
        }
        
        frame_checkboxes = tk.Frame(self.container)
        frame_checkboxes.grid(row=7, column=0, columnspan=4, pady=5, sticky="w")
        
        for dia, var in self.dias_vars.items():
            tk.Checkbutton(frame_checkboxes, text=dia, variable=var, font=("Arial", 10)).pack(side=tk.LEFT, padx=12)

        # Botão de Envio do Aluno
        btn_salvar = tk.Button(self.container, text="Confirmar My Inscrição", bg="#2ecc71", fg="white", font=("Arial", 11, "bold"), width=25, command=self.acao_inscrever)
        btn_salvar.grid(row=8, column=0, columnspan=4, pady=25)

    def acao_inscrever(self):
        dias_selecionados = [dia for dia, var in self.dias_vars.items() if var.get()]
        qtd_dias = len(dias_selecionados)
        
        if not self.txt_nome.get().strip() or not self.txt_cpf.get().strip() or not self.txt_matricula.get().strip():
            messagebox.showwarning("Validação ALU", "Os campos Nome, CPF e Matrícula são obrigatórios!")
            return
        if qtd_dias == 0:
            messagebox.showwarning("Validação ALU", "Você deve selecionar pelo menos 1 dia da semana para usar o transporte!")
            return
            
        # Junta a instituição escolhida com a matrícula para salvar de forma limpa e organizada
        identificacao_academica = f"{self.cb_faculdade.get()} - Matrícula: {self.txt_matricula.get().strip()}"
        
        universitario = Associado(
            nome=self.txt_nome.get().strip(),
            cpf=self.txt_cpf.get().strip(),
            matricula=identificacao_academica,
            telefone=self.txt_telefone.get().strip() if self.txt_telefone.get().strip() else "(54) 3358-0000",
            tipo_associado=self.cb_tipo.get(),
            senha=",".join(dias_selecionados) # Salva a string dos dias marcados (Ex: "Segunda,Sexta")
        )
        
        contexto_calculo = ContextoMensalidade(dias_semana=qtd_dias)
        valor_calculado = contexto_calculo.executar_calculo(universitario.tipo_associado)
        
        sucesso, msg = self.associado_dao.salvar(universitario)
        if sucesso:
            messagebox.showinfo("Recibo de Inscrição ALU", 
                                f"Sua inscrição foi enviada com sucesso para a Diretoria!\n\n"
                                f"Passageiro: {universitario.nome}\n"
                                f"Dias Escolhidos: {', '.join(dias_selecionados)} ({qtd_dias} dias)\n"
                                f"Valor da Mensalidade Estimado: R$ {valor_calculado:.2f}")
            self.txt_nome.delete(0, tk.END)
            self.txt_cpf.delete(0, tk.END)
            self.txt_matricula.delete(0, tk.END)
            self.txt_telefone.delete(0, tk.END)
            for var in self.dias_vars.values(): var.set(False)
        else:
            messagebox.showerror("Erro", msg)

    def mostrar_tela_sobre(self):
        for widget in self.container.winfo_children(): widget.destroy()
        tk.Label(self.container, text="Sobre o Sistema ALU", font=("Arial", 16, "bold"), fg="#1a365d").pack(pady=20)
        texto = "ALU - Sistema Customizado de Gestão de Fretamento Universitário\n\nAutor: Keila de Sales\nLPOO & APS - 2026/1"
        tk.Label(self.container, text=texto, font=("Arial", 11), justify="center").pack(pady=10)