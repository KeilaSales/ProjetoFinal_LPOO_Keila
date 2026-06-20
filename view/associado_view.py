import tkinter as tk
from tkinter import messagebox, ttk

class AssociadoView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Label(self, text="ALU - Associação Lagoense de Universitários", font=("Arial", 16, "bold"), fg="#1a365d").grid(row=0, column=0, columnspan=4, pady=10)
        tk.Label(self, text="Portal de Inscrição do Universitário", font=("Arial", 11, "italic"), fg="#4a5568").grid(row=1, column=0, columnspan=4, pady=5)
        
        tk.Label(self, text="Nome Completo:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=5)
        self.txt_nome = tk.Entry(self, width=30, font=("Arial", 10))
        self.txt_nome.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        
        tk.Label(self, text="CPF (Apenas números):", font=("Arial", 10, "bold")).grid(row=2, column=2, sticky="w", pady=5)
        self.txt_cpf = tk.Entry(self, width=20, font=("Arial", 10))
        self.txt_cpf.grid(row=2, column=3, pady=5, padx=5, sticky="w")
        
        tk.Label(self, text="Faculdade / Universidade:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=5)
        self.cb_faculdade = ttk.Combobox(self, values=[
            "Universidade de Passo Fundo (UPF)", "Instituto Federal Sul-rio-grandense (IFSul)", 
            "Universidade Federal da Fronteira Sul (UFFS)", "Atitus Educação", "Anhanguera", "IDEAU", "Outros"
        ], width=27, state="readonly", font=("Arial", 10))
        self.cb_faculdade.grid(row=3, column=1, pady=5, padx=5, sticky="w")
        self.cb_faculdade.set("Universidade de Passo Fundo (UPF)")
        
        tk.Label(self, text="Nº Matrícula:", font=("Arial", 10, "bold")).grid(row=3, column=2, sticky="w", pady=5)
        self.txt_matricula = tk.Entry(self, width=20, font=("Arial", 10))
        self.txt_matricula.grid(row=3, column=3, pady=5, padx=5, sticky="w")

        tk.Label(self, text="Telefone de Contato:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", pady=5)
        self.txt_telefone = tk.Entry(self, width=30, font=("Arial", 10))
        self.txt_telefone.grid(row=4, column=1, pady=5, padx=5, sticky="w")
        
        tk.Label(self, text="Vínculo ALU:", font=("Arial", 10, "bold")).grid(row=4, column=2, sticky="w", pady=5)
        self.cb_tipo = ttk.Combobox(self, values=["NOVO", "ANTIGO"], width=17, state="readonly", font=("Arial", 10))
        self.cb_tipo.grid(row=4, column=3, pady=5, padx=5, sticky="w")
        self.cb_tipo.set("NOVO")

        tk.Label(self, text="Selecione os dias que utilizará o transporte:", font=("Arial", 10, "bold"), fg="#1a365d").grid(row=5, column=0, columnspan=4, pady=15, sticky="w")
        
        self.dias_vars = {
            "Segunda": tk.BooleanVar(), "Terça": tk.BooleanVar(),
            "Quarta": tk.BooleanVar(), "Quinta": tk.BooleanVar(), "Sexta": tk.BooleanVar()
        }
        frame_dias = tk.Frame(self)
        frame_dias.grid(row=6, column=0, columnspan=4, pady=5, sticky="w")
        for dia, var in self.dias_vars.items():
            tk.Checkbutton(frame_dias, text=dia, variable=var, font=("Arial", 10)).pack(side=tk.LEFT, padx=12)

        btn_salvar = tk.Button(self, text="Confirmar Minha Inscrição", bg="#2ecc71", fg="white", font=("Arial", 11, "bold"), width=25, command=self.salvar)
        btn_salvar.grid(row=7, column=0, columnspan=4, pady=25)

    def salvar(self):
        dias = [dia for dia, var in self.dias_vars.items() if var.get()]
        sucesso, resultado = self.controller.cadastrar_universitario(
            self.txt_nome.get().strip(), self.txt_cpf.get().strip(), self.cb_faculdade.get(),
            self.txt_matricula.get().strip(), self.txt_telefone.get().strip(), self.cb_tipo.get(), dias
        )
        if sucesso:
            messagebox.showinfo("Recibo de Inscrição ALU", 
                                f"Inscrição realizada com sucesso!\n\n"
                                f"Passageiro: {resultado['nome']}\n"
                                f"Dias: {resultado['dias']} ({resultado['qtd']} dias)\n"
                                f"Mensalidade Estimada: R$ {resultado['mensalidade']:.2f}")
            self.limpar()
        else:
            messagebox.showerror("Erro de Inscrição", resultado)

    def limpar(self):
        self.txt_nome.delete(0, tk.END)
        self.txt_cpf.delete(0, tk.END)
        self.txt_matricula.delete(0, tk.END)
        self.txt_telefone.delete(0, tk.END)
        for var in self.dias_vars.values(): var.set(False)