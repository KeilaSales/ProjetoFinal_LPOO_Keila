# CAMADA VIEW: Painel de Gerenciamento e Logística da Diretoria (Tkinter)
import tkinter as tk
from tkinter import messagebox, ttk

# HERANÇA: Herda de tk.Frame para criar o painel container da área administrativa
class DiretoriaView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller # Dependência do Controlador intermediário
        
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
        
        # Dispara o método de exclusão física (D do CRUD)
        tk.Button(self, text="Cancelar Matrícula Selecionada", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), command=self.remover).pack(pady=5)
        
        # Caixa de texto de múltiplas linhas onde é injetado o relatório de frota
        tk.Label(self, text="Dimensionamento Estatístico Diário de Frota", font=("Arial", 11, "bold"), fg="#2c3e50").pack(pady=5)
        self.txt_logistica = tk.Text(self, height=6, width=95, font=("Courier", 10))
        self.txt_logistica.pack(padx=20, pady=5)
        
        # Gatilho de inicialização: busca os dados do banco assim que a tela abre
        self.atualizar_dados()

    def atualizar_dados(self):
        # Limpa a tela, lê o banco e monta a sugestão de frota 
        for row in self.tabela.get_children(): self.tabela.delete(row)
        
        # Busca a lista atualizada de objetos do banco de dados através do Controller
        lista = self.controller.buscar_todos()

        # Dicionário de controle: inicializa os contadores de passageiros zerados para cada dia útil
        cronograma = {"Segunda": 0, "Terça": 0, "Quarta": 0, "Quinta": 0, "Sexta": 0}
        
        for u in lista:
            # Insere visualmente os dados do objeto do estudante na tabela da tela
            self.tabela.insert("", tk.END, values=(u.nome, u.cpf, u.matricula, u.tipo_associado, u.telefone))

            # Recupera a string de dias (proteção caso a propriedade se chame 'senha' ou 'dias_semana')
            dias_do_aluno = getattr(u, 'dias_semana', getattr(u, 'senha', ''))

            # Varre o cronograma e soma +1 passageiro no dia correspondente se estiver no texto do aluno
            for dia in cronograma.keys():
                if u.dias_do_aluno and dia in u.dias_do_aluno:
                    cronograma[dia] += 1
                    
        relatorio = "Mapeamento de Necessidade de Fretamento por Dia Útil:\n"
        for dia, total in cronograma.items():
            if total == 0: frota = "Nenhum Fretamento Ativo"
            elif total <= 15: frota = "Alocar Van Executiva"
            elif total <= 28: frota = "Alocar Micro-ônibus da Associação"
            else: frota = "Alocar Ônibus Fretado Convencional"
            relatorio += f" -> {dia}: {total} Alunos Confirmados | Sugestão: {frota}\n"
            
        # Limpa o campo de texto e insere o relatório de frota calculado em tempo real
        self.txt_logistica.delete("1.0", tk.END)
        self.txt_logistica.insert(tk.END, relatorio)

    def remover(self):
        #Cancela o registro selecionado
        selecao = self.tabela.selection() # Captura qual linha foi clicada pelo administrador
        if not selecao:
            messagebox.showwarning("Diretoria", "Selecione um passageiro na tabela!")
            return

        # Pega a tupla de valores da linha e extrai o CPF (índice 1) para usar como chave de exclusão
        valores = self.tabela.item(selecao, "values")
        cpf = valores[1]
        
        # Caixa de confirmação de segurança para evitar cliques acidentais
        if messagebox.askyesno("Confirmar", f"Deseja mesmo remover a matrícula do CPF {cpf}?"):
            # Envia o comando de remoção para o Controller
            sucesso, msg = self.controller.remover_universitario(cpf) #Recarrega a tabela e atualiza frota
            if sucesso:
                messagebox.showinfo("Sucesso", "Matrícula excluída!")
                self.atualizar_dados()
            else:
                messagebox.showerror("Erro", msg)