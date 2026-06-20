import tkinter as tk
from tkinter import messagebox, ttk
from view.MenuPrincipal import MenuPrincipalFrame
from dao.AssociadoDAO import AssociadoDAO

class AplicacaoPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("ALU - Sistema de Transporte Estudantil")
        self.root.geometry("800x480")
        self.root.resizable(False, False)
        
        self.associado_dao = AssociadoDAO()
        
        barra_menu = tk.Menu(self.root)
        self.root.config(menu=barra_menu)
        
        self.tela_principal = MenuPrincipalFrame(self.root)
        self.tela_principal.pack(fill=tk.BOTH, expand=True)
        
        menu_navegacao = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Navegação Sistema", menu=menu_navegacao)
        menu_navegacao.add_command(label="Portal de Inscrições", command=self.tela_principal.mostrar_tela_inscricao)
        menu_navegacao.add_command(label="Área da Diretoria (Restrito)", command=self.solicitar_login_diretoria)
        menu_navegacao.add_separator()
        menu_navegacao.add_command(label="Sobre a ALU", command=self.tela_principal.mostrar_tela_sobre)
        menu_navegacao.add_command(label="Sair", command=self.root.quit)

    def solicitar_login_diretoria(self):
        self.janela_login = tk.Toplevel(self.root)
        self.janela_login.title("Autenticação de Segurança")
        self.janela_login.geometry("350x180")
        self.janela_login.resizable(False, False)
        self.janela_login.grab_set()
        
        tk.Label(self.janela_login, text="Área Restrita - Diretoria ALU", font=("Arial", 11, "bold"), fg="#1a365d").pack(pady=10)
        tk.Label(self.janela_login, text="Senha do Administrador:").pack(pady=2)
        
        self.txt_senha_adm = tk.Entry(self.janela_login, show="*", width=25, font=("Arial", 10))
        self.txt_senha_adm.pack(pady=5)
        
        tk.Button(self.janela_login, text="Entrar no Painel", bg="#1a365d", fg="white", font=("Arial", 10, "bold"), command=self.validar_senha_diretoria).pack(pady=10)

    def validar_senha_diretoria(self):
        if self.txt_senha_adm.get() == "alu123":
            self.janela_login.destroy()
            self.abrir_caixa_diretoria()
        else:
            messagebox.showerror("Acesso Negado", "Senha administrativa incorreta!")

    def abrir_caixa_diretoria(self):
        janela_adm = tk.Toplevel(self.root)
        janela_adm.title("ALU - Painel Administrativo da Diretoria")
        janela_adm.geometry("950x580")
        
        tk.Label(janela_adm, text="Gerenciamento Geral de Passageiros Cadastrados", font=("Arial", 12, "bold")).pack(pady=10)
        
        colunas = ("Nome", "CPF", "Acadêmico", "Vínculo", "Telefone")
        self.tabela_adm = ttk.Treeview(janela_adm, columns=colunas, show="headings", height=10)
        self.tabela_adm.heading("Nome", text="Nome Completo")
        self.tabela_adm.heading("CPF", text="CPF")
        self.tabela_adm.heading("Acadêmico", text="Instituição / Matrícula")
        self.tabela_adm.heading("Vínculo", text="Vínculo")
        self.tabela_adm.heading("Telefone", text="Telefone")
        
        self.tabela_adm.column("Nome", width=220, anchor="w")
        self.tabela_adm.column("CPF", width=120, anchor="center")
        self.tabela_adm.column("Acadêmico", width=280, anchor="w")
        self.tabela_adm.column("Vínculo", width=90, anchor="center")
        self.tabela_adm.column("Telefone", width=120, anchor="center")
        self.tabela_adm.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        frame_acoes = tk.Frame(janela_adm)
        frame_acoes.pack(pady=10)
        
        tk.Button(frame_acoes, text="Cancelar Matrícula Selecionada", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), command=self.remover_passageiro).pack(side=tk.LEFT, padx=10)
        
        tk.Label(janela_adm, text="Dimensionamento Estatístico Diário de Frota", font=("Arial", 11, "bold"), fg="#1a365d").pack(pady=5)
        
        self.txt_logistica = tk.Text(janela_adm, height=7, width=110, font=("Courier", 10))
        self.txt_logistica.pack(padx=20, pady=5)
        
        self.atualizar_dados_adm()

    def atualizar_dados_adm(self):
        for row in self.tabela_adm.get_children(): 
            self.tabela_adm.delete(row)
        
        lista = self.associado_dao.listar_todos()
        cronograma_presenca = {"Segunda": 0, "Terça": 0, "Quarta": 0, "Quinta": 0, "Sexta": 0}
        
        for u in lista:
            self.tabela_adm.insert("", tk.END, values=(u.nome, u.cpf, u.matricula, u.tipo_associado, u.telefone))
            
            for dia in cronograma_presenca.keys():
                if u.senha and dia in u.senha:
                    cronograma_presenca[dia] += 1
                    
        relatorio = "Mapeamento de Necessidade de Transporte Diário (Fretamentos Ativos):\n"
        for dia, total in cronograma_presenca.items():
            if total == 0: frota = "Nenhum Fretamento Requerido"
            elif total <= 15: frota = "Alocar Van Executiva"
            elif total <= 28: frota = "Alocar Micro-ônibus da Associação"
            else: frota = "Alocar Ônibus Fretado Convencional"
            relatorio += f" -> {dia}: {total} Alunos Confirmados | Sugestão para a Diretoria: {frota}\n"
            
        self.txt_logistica.delete("1.0", tk.END)
        self.txt_logistica.insert(tk.END, relatorio)

    def remover_passageiro(self):
        selecao = self.tabela_adm.selection()
        if not selecao:
            messagebox.showwarning("Diretoria ALU", "Por favor, selecione um passageiro na tabela antes de clicar em excluir!")
            return
            
        valores = self.tabela_adm.item(selecao, "values")
        cpf_original = str(valores[1]).strip()
        
        if messagebox.askyesno("Confirmar Operação", f"Deseja mesmo revogar a matrícula e remover o CPF {cpf_original} das listas?"):
            sucesso, msg = self.associado_dao.remover(cpf_original)
            
            if not sucesso:
                cpf_limpo = cpf_original.replace(".", "").replace("-", "").strip()
                sucesso, msg = self.associado_dao.remover(cpf_limpo)
            
            if sucesso:
                messagebox.showinfo("Sucesso ALU", "A matrícula foi cancelada com sucesso na base de dados!")
                self.atualizar_dados_adm()
            else:
                messagebox.showerror("Erro ao Deletar", f"O PostgreSQL não conseguiu remover: {msg}")

if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicacaoPrincipal(raiz)
    raiz.mainloop()