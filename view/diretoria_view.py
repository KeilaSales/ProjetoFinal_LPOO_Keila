import tkinter as tk
from tkinter import messagebox, ttk

class DiretoriaView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        tk.Label(self, text="Painel Administrativo da Diretoria ALU", font=("Arial", 14, "bold"), fg="#1a365d").pack(pady=10)
        
        # Tabela formatada e alinhada
        colunas = ("Nome", "CPF", "Acadêmico", "Vínculo", "Telefone")
        self.tabela = ttk.Treeview(self, columns=colunas, show="headings", height=8)
        self.tabela.heading("Nome", text="Nome Completo")
        self.tabela.heading("CPF", text="CPF")
        self.tabela.heading("Acadêmico", text="Instituição / Matrícula")
        self.tabela.heading("Vínculo", text="Vínculo")
        self.tabela.heading("Telefone", text="Telefone")
        
        self.tabela.column("Nome", width=200)
        self.tabela.column("CPF", width=110, anchor="center")
        self.tabela.column("Acadêmico", width=260)
        self.tabela.column("Vínculo", width=80, anchor="center")
        self.tabela.column("Telefone", width=110, anchor="center")
        self.tabela.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
        
        tk.Button(self, text="Cancelar Matrícula Selecionada", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), command=self.remover).pack(pady=5)
        
        tk.Label(self, text="Dimensionamento Estatístico Diário de Frota", font=("Arial", 11, "bold"), fg="#2c3e50").pack(pady=5)
        self.txt_logistica = tk.Text(self, height=6, width=95, font=("Courier", 10))
        self.txt_logistica.pack(padx=20, pady=5)
        
        self.atualizar_dados()

    def atualizar_dados(self):
        for row in self.tabela.get_children(): self.tabela.delete(row)
        
        lista = self.controller.buscar_todos()
        cronograma = {"Segunda": 0, "Terça": 0, "Quarta": 0, "Quinta": 0, "Sexta": 0}
        
        for u in lista:
            self.tabela.insert("", tk.END, values=(u.nome, u.cpf, u.matricula, u.tipo_associado, u.telefone))
            for dia in cronograma.keys():
                if u.senha and dia in u.senha:
                    cronograma[dia] += 1
                    
        relatorio = "Mapeamento de Necessidade de Fretamento por Dia Útil:\n"
        for dia, total in cronograma.items():
            if total == 0: frota = "Nenhum Fretamento Ativo"
            elif total <= 15: frota = "Alocar Van Executiva"
            elif total <= 28: frota = "Alocar Micro-ônibus da Associação"
            else: frota = "Alocar Ônibus Fretado Convencional"
            relatorio += f" -> {dia}: {total} Alunos Confirmados | Sugestão: {frota}\n"
            
        self.txt_logistica.delete("1.0", tk.END)
        self.txt_logistica.insert(tk.END, relatorio)

    def remover(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Diretoria", "Selecione um passageiro na tabela!")
            return
        valores = self.tabela.item(selecao, "values")
        cpf = valores[1]
        
        if messagebox.askyesno("Confirmar", f"Deseja mesmo remover a matrícula do CPF {cpf}?"):
            sucesso, msg = self.controller.remover_universitario(cpf)
            if sucesso:
                messagebox.showinfo("Sucesso", "Matrícula excluída!")
                self.atualizar_dados()
            else:
                messagebox.showerror("Erro", msg)