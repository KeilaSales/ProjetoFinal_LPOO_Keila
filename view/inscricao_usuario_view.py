import tkinter as tk
from tkinter import messagebox, ttk

class InscricaoUsuarioView:
    def __init__(self, root, controller):
        self.window = tk.Toplevel(root)
        self.window.title("Inscrição — Sistema de Transporte Universitário")
        self.window.geometry("680x520")
        self.window.resizable(False, False)
        self.window.grab_set()
        self.controller = controller
        
        tk.Label(self.window, text="Formulário de Inscrição de Passageiro", font=("Arial", 14, "bold"), fg="#1a365d").pack(pady=15)
        
        frame_form = tk.Frame(self.window)
        frame_form.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
        
        # --- CAMPOS DO FORMULÁRIO ---
        tk.Label(frame_form, text="Nome Completo:").grid(row=0, column=0, sticky="w", pady=5)
        self.txt_nome = tk.Entry(frame_form, width=28, font=("Arial", 10))
        self.txt_nome.grid(row=0, column=1, pady=5, padx=5, sticky="w")
        
        tk.Label(frame_form, text="CPF:").grid(row=0, column=2, sticky="w", pady=5)
        self.txt_cpf = tk.Entry(frame_form, width=20, font=("Arial", 10))
        self.txt_cpf.grid(row=0, column=3, pady=5, padx=5, sticky="w")
        
        tk.Label(frame_form, text="Universidade / Faculdade:").grid(row=1, column=0, sticky="w", pady=5)
        self.cb_faculdade = ttk.Combobox(frame_form, values=[
            "Universidade de Passo Fundo (UPF)", "Instituto Federal Sul-rio-grandense (IFSul)", 
            "Universidade Federal da Fronteira Sul (UFFS)", "Atitus Educação", "Anhanguera", "IDEAU", "Outros"
        ], width=25, state="readonly", font=("Arial", 10))
        self.cb_faculdade.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        self.cb_faculdade.set("Universidade de Passo Fundo (UPF)")
        
        tk.Label(frame_form, text="Nº Matrícula:").grid(row=1, column=2, sticky="w", pady=5)
        self.txt_matricula = tk.Entry(frame_form, width=20, font=("Arial", 10))
        self.txt_matricula.grid(row=1, column=3, pady=5, padx=5, sticky="w")

        tk.Label(frame_form, text="Telefone de Contato:").grid(row=2, column=0, sticky="w", pady=5)
        self.txt_telefone = tk.Entry(frame_form, width=28, font=("Arial", 10))
        self.txt_telefone.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        
        tk.Label(frame_form, text="Situação Vínculo:").grid(row=2, column=2, sticky="w", pady=5)
        self.cb_tipo = ttk.Combobox(frame_form, values=["NOVO", "ANTIGO"], width=17, state="readonly", font=("Arial", 10))
        self.cb_tipo.grid(row=2, column=3, pady=5, padx=5, sticky="w")
        self.cb_tipo.set("NOVO")

        tk.Label(frame_form, text="Turno de IDA:").grid(row=3, column=0, sticky="w", pady=5)
        self.cb_ida = ttk.Combobox(frame_form, values=["Manhã", "Tarde", "Noite"], width=25, state="readonly", font=("Arial", 10))
        self.cb_ida.grid(row=3, column=1, pady=5, padx=5, sticky="w")
        self.cb_ida.set("Noite")

        tk.Label(frame_form, text="Turno de VOLTA:").grid(row=3, column=2, sticky="w", pady=5)
        self.cb_volta = ttk.Combobox(frame_form, values=["Manhã", "Tarde", "Noite"], width=17, state="readonly", font=("Arial", 10))
        self.cb_volta.grid(row=3, column=3, pady=5, padx=5, sticky="w")
        self.cb_volta.set("Noite")

        tk.Label(frame_form, text="Selecione os dias de uso na semana:", font=("Arial", 10, "bold"), fg="#2c3e50").grid(row=4, column=0, columnspan=4, pady=15, sticky="w")
        
        self.dias_vars = {
            "Segunda": tk.BooleanVar(), "Terça": tk.BooleanVar(),
            "Quarta": tk.BooleanVar(), "Quinta": tk.BooleanVar(), "Sexta": tk.BooleanVar()
        }
        frame_dias = tk.Frame(frame_form)
        frame_dias.grid(row=5, column=0, columnspan=4, pady=5, sticky="w")
        for dia, var in self.dias_vars.items():
            tk.Checkbutton(frame_dias, text=dia, variable=var, font=("Arial", 9)).pack(side=tk.LEFT, padx=12)

        frame_botoes = tk.Frame(self.window)
        frame_botoes.pack(pady=25)
        
        btn_salvar = tk.Button(frame_botoes, text="Confirmar Inscrição", font=("Arial", 10, "bold"), bg="#2ecc71", fg="white", width=18, command=self.salvar)
        btn_salvar.pack(side=tk.LEFT, padx=10)
        
        btn_cancelar = tk.Button(frame_botoes, text="Sair / Voltar", font=("Arial", 10), bg="#95a5a6", fg="white", width=12, command=self.window.destroy)
        btn_cancelar.pack(side=tk.LEFT, padx=10)

    def salvar(self):
        nome = self.txt_nome.get().strip()
        cpf = self.txt_cpf.get().strip()
        matricula = self.txt_matricula.get().strip()
        telefone = self.txt_telefone.get().strip()
        vinculo = self.cb_tipo.get()
        dias = [dia for dia, var in self.dias_vars.items() if var.get()]
        
        # Validações estritas de segurança na interface
        if not nome or not cpf or not matricula:
            messagebox.showwarning("Validação", "Os campos Nome, CPF e Matrícula são obrigatórios!")
            return
        if any(char.isdigit() for char in nome):
            messagebox.showwarning("Erro", "O campo Nome Completo não deve conter números!")
            return
        if not cpf.isdigit() or len(cpf) != 11:
            messagebox.showwarning("Erro de CPF", "O campo CPF deve conter exatamente 11 dígitos numéricos!")
            return
        if not matricula.isdigit():
            messagebox.showwarning("Erro", "O campo Nº Matrícula deve conter apenas números!")
            return
        if not telefone.isdigit() or len(telefone) < 9:
            messagebox.showwarning("Erro de Telefone", "O campo Telefone deve conter no mínimo 9 dígitos numéricos!")
            return
        if len(dias) == 0:
            messagebox.showwarning("Validação", "Selecione ao menos 1 dia da semana para o transporte!")
            return

        info_turnos = f"Ida: {self.cb_ida.get()} | Volta: {self.cb_volta.get()}"
        
        sucesso, resultado = self.controller.cadastrar_universitario(nome, cpf, self.cb_faculdade.get(), matricula, telefone, vinculo, dias)
        
        if sucesso:
            termo_tax = "Taxa de Rematrícula" if vinculo == "ANTIGO" else "Taxa de Inscrição/Matrícula"

            # Renderiza o recibo completo utilizando as saídas do seu Strategy
            messagebox.showinfo("Recibo de Inscrição Universitária", 
                                f"Inscrição cadastrada com sucesso!\n\n"
                                f"Passageiro: {resultado['nome']}\n"
                                f"Logística: {info_turnos}\n"
                                f"Frequência Semanal: {resultado['dias']} ({resultado['qtd']} dias)\n\n"
                                f"--- Demonstrativo Financeiro (Calculado via Strategy) ---\n"
                                f"• Custo Mensal Rateado: R$ {resultado['mensalidade_pura']:.2f}\n"
                                f"• {termo_tax}: R$ {resultado['taxa']:.2f}\n"
                                f" TOTAL DO PRIMEIRO MÊS (Com Taxas): R$ {resultado['total_primeiro_mes']:.2f}\n"
                                f" MENSALIDADES SEGUINTES (Líquidas): R$ {resultado['mensalidade_pura']:.2f}")
            self.window.destroy()
        else:
            messagebox.showerror("Erro de Inscrição", resultado)