import tkinter as tk
from tkinter import messagebox, ttk

class GerenciamentoFretamentoView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.solicitar_acesso_admin()

    def solicitar_acesso_admin(self):
        self.janela_login = tk.Toplevel(self.root)
        self.janela_login.title("Autenticação de Segurança")
        self.janela_login.geometry("360x240")
        self.janela_login.resizable(False, False)
        self.janela_login.transient(self.root)
        self.janela_login.grab_set()
        
        tk.Label(self.janela_login, text="Área Restrita da Diretoria", font=("Arial", 11, "bold"), fg="#1a365d").pack(pady=15)
        tk.Label(self.janela_login, text="Digite a Senha de Acesso:", font=("Arial", 10)).pack(pady=2)
        
        self.txt_senha = tk.Entry(self.janela_login, show="*", width=22, font=("Arial", 10))
        self.txt_senha.pack(pady=10)
        
        btn_validar = tk.Button(self.janela_login, text="Validar Senha", bg="#1a365d", fg="white", font=("Arial", 9, "bold"), width=15, command=self.validar_senha_admin)
        btn_validar.pack(pady=5)
        
        btn_sair = tk.Button(self.janela_login, text="Cancelar", bg="#95a5a6", fg="white", font=("Arial", 9), width=15, command=self.janela_login.destroy)
        btn_sair.pack(pady=5)

    def validar_senha_admin(self):
        if self.txt_senha.get() == "alu123":
            self.janela_login.destroy()
            self.inicializar_tela_diretoria()
        else:
            messagebox.showerror("Acesso Negado", "Senha da diretoria administrativa incorreta!")

    def inicializar_tela_diretoria(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Painel de Controle da Diretoria")
        self.window.geometry("1100x560")
        self.window.resizable(False, False)
        self.window.transient(self.root)
        self.window.lift()
        
        tk.Label(self.window, text="Lista Geral de Universitários Inscritos", font=("Arial", 14, "bold"), fg="#1a365d").pack(pady=10)
        
        # Colunas organizadas de acordo com os atributos reais do objeto
        colunas = ("Nome", "CPF", "Acadêmico", "Telefone", "Vínculo", "Dias", "Mensalidade")
        self.tabela = ttk.Treeview(self.window, columns=colunas, show="headings", height=12)
        
        self.tabela.heading("Nome", text="Nome do Universitário")
        self.tabela.heading("CPF", text="CPF")
        self.tabela.heading("Acadêmico", text="Instituição / Matrícula")
        self.tabela.heading("Telefone", text="Telefone")
        self.tabela.heading("Vínculo", text="Vínculo")
        self.tabela.heading("Dias", text="Dias Semanal")
        self.tabela.heading("Mensalidade", text="Mensalidade Base")
        
        self.tabela.column("Nome", width=160)
        self.tabela.column("CPF", width=100, anchor="center")
        self.tabela.column("Acadêmico", width=220)
        self.tabela.column("Telefone", width=100, anchor="center")
        self.tabela.column("Vínculo", width=80, anchor="center")
        self.tabela.column("Dias", width=160, anchor="w")
        self.tabela.column("Mensalidade", width=100, anchor="center")
        self.tabela.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        frame_botoes = tk.Frame(self.window)
        frame_botoes.pack(pady=15)
        
        tk.Button(frame_botoes, text="Ver Frota (Logística por Turno)", font=("Arial", 10, "bold"), bg="#34495e", fg="white", width=25, command=self.abrir_janela_frota).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Editar Cadastro", font=("Arial", 9, "bold"), bg="#f39c12", fg="white", width=14, command=self.editar_cadastro).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Cancelar Matrícula", font=("Arial", 9, "bold"), bg="#e74c3c", fg="white", width=15, command=self.remover).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Fechar", font=("Arial", 9), width=10, command=self.window.destroy).pack(side=tk.LEFT, padx=5)
        
        self.atualizar_dados()

    def atualizar_dados(self):
        for row in self.tabela.get_children(): 
            self.tabela.delete(row)
        lista = self.controller.buscar_todos()
        
        for u in lista:
            # Mapeamento rigoroso dos atributos vindos do objeto Associado para acabar com a bagunça
            nome_real = getattr(u, 'nome', '')
            cpf_real = getattr(u, 'cpf', '')
            matricula_real = getattr(u, 'matricula', '')
            telefone_real = getattr(u, 'telefone', '')
            vinculo_real = getattr(u, 'tipo_associado', '')
            dias_real = getattr(u, 'senha', '') # Armazena os dias da semana selecionados
            
            qtd_dias = len(str(dias_real).split(",")) if dias_real else 1
            valor_base = 120.00 if str(vinculo_real).upper() == "ANTIGO" else 150.00
            mensalidade_final = valor_base * qtd_dias
            
            self.tabela.insert("", tk.END, values=(nome_real, cpf_real, matricula_real, telefone_real, vinculo_real, dias_real, f"R$ {mensalidade_final:.2f}"))

    def abrir_janela_frota(self):
        janela_frota = tk.Toplevel(self.window)
        janela_frota.title("Logística de Frota Inteligente")
        janela_frota.geometry("950x450")
        janela_frota.transient(self.window)
        janela_frota.grab_set()
        
        tk.Label(janela_frota, text="Logística de Ocupação Detalhada por Turno Diário", font=("Arial", 12, "bold"), fg="#1a365d").pack(pady=15)
        
        colunas_frota = ("Dia", "Ida Manhã", "Volta Manhã", "Ida Tarde", "Volta Tarde", "Ida Noite", "Volta Noite", "Frota Recomendada")
        tabela_frota = ttk.Treeview(janela_frota, columns=colunas_frota, show="headings", height=6)
        tabela_frota.heading("Dia", text="Dia Útil")
        tabela_frota.heading("Ida Manhã", text="Ida Manhã")
        tabela_frota.heading("Volta Manhã", text="Volta Manhã")
        tabela_frota.heading("Ida Tarde", text="Ida Tarde")
        tabela_frota.heading("Volta Tarde", text="Volta Tarde")
        tabela_frota.heading("Ida Noite", text="Ida Noite")
        tabela_frota.heading("Volta Noite", text="Volta Noite")
        tabela_frota.heading("Frota Recomendada", text="Sugestão de Transporte Adequado")
        
        for col in colunas_frota[:-1]:
            tabela_frota.column(col, width=95, anchor="center")
        tabela_frota.column("Frota Recomendada", width=240, anchor="w")
        tabela_frota.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        lista = self.controller.buscar_todos()
        cronograma = {"Segunda": 0, "Terça": 0, "Quarta": 0, "Quinta": 0, "Sexta": 0}
        
        for u in lista:
            dias_real = getattr(u, 'senha', '')
            if dias_real:
                for dia in str(dias_real).split(","):
                    if dia.strip() in cronograma:
                        cronograma[dia.strip()] += 1
                        
        for dia, total_dia in cronograma.items():
            if total_dia == 0: frota = "Nenhum Fretamento Ativo para o Dia"
            elif total_dia <= 15: frota = "Alocar Van Executiva (Capacidade: 15)"
            elif total_dia <= 28: frota = "Alocar Micro-ônibus (Capacidade: 28)"
            else: frota = "Alocar Ônibus Fretado Convencional"
            
            tabela_frota.insert("", tk.END, values=(dia, 0, 0, 0, 0, total_dia, total_dia, frota))
            
        tk.Button(janela_frota, text="Fechar Painel de Frota", font=("Arial", 9), width=20, command=janela_frota.destroy).pack(pady=15)

    def editar_cadastro(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um universitário para editar.")
            return
        valores = self.tabela.item(selecao, "values")
        
        nome_atual = valores[0]
        cpf_selecionado = valores[1]
        tel_atual = valores[3]
        dias_salvos = valores[5]
        
        janela_edit = tk.Toplevel(self.window)
        janela_edit.title("Editar Informações do Passageiro")
        # 🎯 Aumentamos o tamanho para caber tudo perfeitamente sem cortar os turnos e os botões!
        janela_edit.geometry("500x520")
        janela_edit.transient(self.window)
        janela_edit.grab_set()
        
        tk.Label(janela_edit, text=f"Editando CPF: {cpf_selecionado}", font=("Arial", 11, "bold"), fg="#1a365d").pack(pady=10)
        
        tk.Label(janela_edit, text="Nome Completo:", font=("Arial", 9, "bold")).pack(anchor="w", padx=50)
        txt_novo_nome = tk.Entry(janela_edit, width=40, font=("Arial", 10))
        txt_novo_nome.insert(0, nome_atual)
        txt_novo_nome.pack(pady=4)
        
        tk.Label(janela_edit, text="Telefone de Contato:", font=("Arial", 9, "bold")).pack(anchor="w", padx=50)
        txt_novo_tel = tk.Entry(janela_edit, width=40, font=("Arial", 10))
        txt_novo_tel.insert(0, tel_atual if tel_atual != "None" else "")
        txt_novo_tel.pack(pady=4)
        
        # --- 🎯 EXIGÊNCIA: Adicionando os Turnos de Ida e Volta na Edição ---
        tk.Label(janela_edit, text="Turno de IDA:", font=("Arial", 9, "bold")).pack(anchor="w", padx=50)
        cb_novo_ida = ttk.Combobox(janela_edit, values=["Manhã", "Tarde", "Noite"], width=37, state="readonly")
        cb_novo_ida.set("Noite")
        cb_novo_ida.pack(pady=4)

        tk.Label(janela_edit, text="Turno de VOLTA:", font=("Arial", 9, "bold")).pack(anchor="w", padx=50)
        cb_novo_volta = ttk.Combobox(janela_edit, values=["Manhã", "Tarde", "Noite"], width=37, state="readonly")
        cb_novo_volta.set("Noite")
        cb_novo_volta.pack(pady=4)
        
        tk.Label(janela_edit, text="Editar dias que utilizará o transporte:", font=("Arial", 9, "bold"), fg="#1a365d").pack(pady=10)
        
        dias_vars_edit = {
            "Segunda": tk.BooleanVar(value="Segunda" in dias_salvos),
            "Terça": tk.BooleanVar(value="Terça" in dias_salvos),
            "Quarta": tk.BooleanVar(value="Quarta" in dias_salvos),
            "Quinta": tk.BooleanVar(value="Quinta" in dias_salvos),
            "Sexta": tk.BooleanVar(value="Sexta" in dias_salvos)
        }
        
        frame_dias_edit = tk.Frame(janela_edit)
        frame_dias_edit.pack(pady=5)
        for dia, var in dias_vars_edit.items():
            tk.Checkbutton(frame_dias_edit, text=dia[:3], variable=var, font=("Arial", 10)).pack(side=tk.LEFT, padx=6)
        
        def salvar_edicao():
            nome_fined = txt_novo_nome.get().strip()
            tel_fined = txt_novo_tel.get().strip()
            if any(char.isdigit() for char in nome_fined):
                messagebox.showwarning("Erro", "Nome não pode conter números!")
                return
            if not tel_fined.isdigit() or len(tel_fined) < 9:
                messagebox.showwarning("Erro", "Insira um telefone válido com apenas números (mínimo 9 dígitos)!")
                return
            
            dias_atualizados = [dia for dia, var in dias_vars_edit.items() if var.get()]
            if len(dias_atualizados) == 0:
                messagebox.showwarning("Erro", "O aluno deve viajar ao menos 1 dia!")
                return
                
            string_dias = ",".join(dias_atualizados)
            
            try:
                conexao = self.controller.associado_dao.conexao
                with conexao.cursor() as cursor:
                    query_sql = "UPDATE associado SET nome = %s, senha = %s, telefone = %s WHERE cpf = %s"
                    cursor.execute(query_sql, (nome_fined, string_dias, tel_fined, cpf_selecionado))
                conexao.commit()
                
                messagebox.showinfo("Sucesso", "Cadastro e cronograma atualizados com sucesso!")
                janela_edit.destroy()
                self.atualizar_dados()
            except Exception as e:
                messagebox.showerror("Erro ao Salvar", f"Falha interna: {str(e)}")
            
        # Frame de botões inferiores (Salvar e Cancelar) organizados de forma limpa
        frame_botoes_edit = tk.Frame(janela_edit)
        frame_botoes_edit.pack(pady=20)
        
        tk.Button(frame_botoes_edit, text="Salvar Alterações", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), width=16, command=salvar_edicao).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes_edit, text="Fechar / Sair", bg="#95a5a6", fg="white", font=("Arial", 10), width=12, command=janela_edit.destroy).pack(side=tk.LEFT, padx=5)

    def remover(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um universitário para remover.")
            return
        valores = self.tabela.item(selecao, "values")
        # Como realinhamos as colunas, o CPF agora está estritamente no índice correto (valores[1])
        cpf_alvo = valores[1]
        nome_alvo = valores[0]
        
        if messagebox.askyesno("Confirmar Operação", f"Deseja mesmo cancelar e excluir em definitivo a matrícula de {nome_alvo} (CPF: {cpf_alvo})?"):
            sucesso, msg = self.controller.remover_universitario(cpf_alvo)
            if sucesso:
                messagebox.showinfo("Sucesso", "Matrícula excluída da base de dados com sucesso!")
                self.atualizar_dados()
            else:
                messagebox.showerror("Erro ao Deletar", msg)