
# CAMADA VIEW: Painel Completo de Controle e Edição da Diretoria (Tkinter)
import tkinter as tk
from tkinter import messagebox, ttk
from model.Associado import Associado  
from view.gerenciamento_fretamento_view import GerenciamentoFretamentoView

class GerenciamentoAssociadoView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        #Exige autenticação antes de renderizar qualquer dado
        self.solicitar_acesso_admin()

    def solicitar_acesso_admin(self):
        #Cria uma janela flutuante independente sobre a tela principal
        self.janela_login = tk.Toplevel(self.root)
        self.janela_login.title("Autenticação - Portaria")
        self.janela_login.geometry("360x240")
        self.janela_login.resizable(False, False)
        self.janela_login.transient(self.root)
        self.janela_login.grab_set()
        
        tk.Label(self.janela_login, text="Gerenciamento de Universitários", font=("Arial", 11, "bold"), fg="#1a365d").pack(pady=15)
        tk.Label(self.janela_login, text="Digite a Senha de Acesso:", font=("Arial", 10)).pack(pady=2)
        
        #O atributo show="*" esconde os caracteres digitados no campo
        self.txt_senha = tk.Entry(self.janela_login, show="*", width=22, font=("Arial", 10))
        self.txt_senha.pack(pady=10)
        
        btn_validar = tk.Button(self.janela_login, text="Entrar", bg="#1a365d", fg="white", font=("Arial", 9, "bold"), width=15, command=self.validar_senha_admin)
        btn_validar.pack(pady=5)
        
        btn_sair = tk.Button(self.janela_login, text="Cancelar", bg="#95a5a6", fg="white", font=("Arial", 9), width=15, command=self.janela_login.destroy)
        btn_sair.pack(pady=5)

    def validar_senha_admin(self):
        if self.txt_senha.get() == "diretoria123":
            self.janela_login.destroy() #Fecha a caixinha de login
            self.inicializar_tela_associados() #Abre a tela de gerenciamento de associados
        else:
            messagebox.showerror("Acesso Negado", "Senha administrativa incorreta!")

    def inicializar_tela_associados(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Painel Administrativo de Associados")
        self.window.geometry("1000x520")
        self.window.resizable(False, False)
        self.window.transient(self.root)
        self.window.lift()
        
        tk.Label(self.window, text="Universitários Cadastrados na Associação", font=("Arial", 14, "bold"), fg="#1a365d").pack(pady=10)
        
        frame_busca = tk.Frame(self.window)
        frame_busca.pack(pady=5, fill=tk.X, padx=20)
        
        tk.Label(frame_busca, text="🔍 Pesquisar por Nome:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.txt_busca = tk.Entry(frame_busca, font=("Arial", 10), width=35)
        self.txt_busca.pack(side=tk.LEFT, padx=5)
        
        #Busca em cada caracter digitado
        def filtrar_por_nome(event):
            termo = self.txt_busca.get().lower().strip() 
            # Limpa as linhas da tabela antes de listar o resultado filtrado
            for row in self.tabela.get_children():
                self.tabela.delete(row)
            try:
                lista = self.controller.buscar_todos()
                for u in lista:
                # Compara o termo digitado com o nome do objeto da Model
                    if termo in u.nome.lower():
                        qtd_dias = len(str(u.dias_semana).split(",")) if u.dias_semana else 1
                        valor_base = 120.00 if str(u.tipo_associado).upper() == "ANTIGO" else 150.00
                        mensalidade_final = valor_base * qtd_dias
                        self.tabela.insert("", tk.END, values=(u.nome, u.cpf, u.matricula, u.telefone, u.tipo_associado, u.dias_semana, f"R$ {mensalidade_final:.2f}"))
            except Exception as e:
                print(f"Erro ao filtrar: {e}")

        #Vincula o evento de soltar uma tecla (<KeyRelease>) à função de filtragem
        self.txt_busca.bind("<KeyRelease>", filtrar_por_nome)

        #Montagem da estrutura de colunas e cabeçalhos da tabela principal
        colunas = ("Nome", "CPF", "Acadêmico", "Telefone", "Vínculo", "Dias", "Mensalidade")
        self.tabela = ttk.Treeview(self.window, columns=colunas, show="headings", height=12)
        
        self.tabela.heading("Nome", text="Nome")
        self.tabela.heading("CPF", text="CPF")
        self.tabela.heading("Acadêmico", text="Instituição / Matrícula")
        self.tabela.heading("Telefone", text="Telefone")
        self.tabela.heading("Vínculo", text="Vínculo")
        self.tabela.heading("Dias", text="Dias Semanal")
        self.tabela.heading("Mensalidade", text="Mensalidade")
        
        self.tabela.column("Nome", width=160)
        self.tabela.column("CPF", width=100, anchor="center")
        self.tabela.column("Acadêmico", width=220)
        self.tabela.column("Telefone", width=110, anchor="center")
        self.tabela.column("Vínculo", width=80, anchor="center")
        self.tabela.column("Dias", width=150, anchor="w")
        self.tabela.column("Mensalidade", width=100, anchor="center")
        self.tabela.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        frame_botoes = tk.Frame(self.window)
        frame_botoes.pack(pady=15)
        
        #Botões de baixo 
        tk.Button(frame_botoes, text="Ver Frota (Logística por Turno)", font=("Arial", 9, "bold"), bg="#34495e", fg="white", width=26, command=self.abrir_fretamento_direto).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Editar Cadastro", font=("Arial", 9, "bold"), bg="#f39c12", fg="white", width=16, command=self.editar_cadastro).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Cancelar Matrícula", font=("Arial", 9, "bold"), bg="#e74c3c", fg="white", width=16, command=self.remover).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Fechar", font=("Arial", 9), width=12, command=self.window.destroy).pack(side=tk.LEFT, padx=5)
        
        # Puxa os dados iniciais do banco
        self.atualizar_dados()

    def atualizar_dados(self):
        #Popula a tabela com os registros ativos 
        for row in self.tabela.get_children(): 
            self.tabela.delete(row)
        
        try:
            lista = self.controller.buscar_todos()
            if lista:
                for u in lista: 
                    # Calcula o valor estimado para exibição administrativa baseado na quantia de dias
                    qtd_dias = len(str(u.dias_semana).split(",")) if u.dias_semana else 1
                    valor_base = 120.00 if str(u.tipo_associado).upper() == "ANTIGO" else 150.00
                    mensalidade_final = valor_base * qtd_dias
                    self.tabela.insert("", tk.END, values=(u.nome, u.cpf, u.matricula, u.telefone, u.tipo_associado, u.dias_semana, f"R$ {mensalidade_final:.2f}"))
        except Exception as e:
            print(f"Erro ao preencher a tabela: {e}")

    def abrir_fretamento_direto(self):
        GerenciamentoFretamentoView(self.window, self.controller)

    def editar_cadastro(self):
        #Abre o formulário flutuante interno para alteração cadastral
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um universitário para editar.")
            return
        valores = self.tabela.item(selecao, "values")

        # Captura os dados da linha clicada para preencher os campos originais na tela de edição
        nome_atual = valores[0]
        cpf_selecionado = valores[1]
        tel_atual = valores[3]
        dias_salvos = valores[5]
        
        # Varre a lista de objetos para extrair os turnos salvos daquele CPF específico
        lista_completa = self.controller.buscar_todos()
        turno_ida_atual = "Noite"
        turno_volta_atual = "Noite"
        for obj in lista_completa:
            if obj.cpf == cpf_selecionado:
                turno_ida_atual = obj.turno_ida
                turno_volta_atual = obj.turno_volta
                break
        
        # Cria a janela de alteração de dados
        janela_edit = tk.Toplevel(self.window)
        janela_edit.title("Editar Passageiro")
        janela_edit.geometry("520x560")
        janela_edit.transient(self.window)
        janela_edit.grab_set()
        
        #Cria um painel com barra de rolagem vertical dinâmica
        canvas = tk.Canvas(janela_edit, highlightthickness=0)
        scrollbar = ttk.Scrollbar(janela_edit, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        def configurar_rolagem(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            
        scrollable_frame.bind("<Configure>", configurar_rolagem)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=480)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(scrollable_frame, text=f"Editando CPF: {cpf_selecionado}", font=("Arial", 11, "bold"), fg="#1a365d").pack(pady=10)
        
        tk.Label(scrollable_frame, text="Nome Completo:", font=("Arial", 9, "bold")).pack(anchor="w", padx=50)
        txt_novo_nome = tk.Entry(scrollable_frame, width=40, font=("Arial", 10))
        txt_novo_nome.insert(0, nome_atual) # Preenche o campo com o valor existente
        txt_novo_nome.pack(pady=4)
        
        tk.Label(scrollable_frame, text="Telefone de Contato:", font=("Arial", 9, "bold")).pack(anchor="w", padx=50)
        txt_novo_tel = tk.Entry(scrollable_frame, width=40, font=("Arial", 10))
        txt_novo_tel.insert(0, tel_atual if tel_atual != "None" else "")
        txt_novo_tel.pack(pady=4)
        
        tk.Label(scrollable_frame, text="Turno de IDA:", font=("Arial", 9, "bold")).pack(anchor="w", padx=50)
        cb_novo_ida = ttk.Combobox(scrollable_frame, values=["Manhã", "Tarde", "Noite"], width=37, state="readonly")
        cb_novo_ida.set(turno_ida_atual)
        cb_novo_ida.pack(pady=4)

        tk.Label(scrollable_frame, text="Turno de VOLTA:", font=("Arial", 9, "bold")).pack(anchor="w", padx=50)
        cb_novo_volta = ttk.Combobox(scrollable_frame, values=["Manhã", "Tarde", "Noite"], width=37, state="readonly")
        cb_novo_volta.set(turno_volta_atual)
        cb_novo_volta.pack(pady=4)
        
        tk.Label(scrollable_frame, text="Editar dias semanais:", font=("Arial", 9, "bold"), fg="#1a365d").pack(pady=10)
        
        #Inicializam marcadas (True) se o dia já estava no texto recuperado do banco
        dias_vars_edit = {
            "Segunda": tk.BooleanVar(value="Segunda" in dias_salvos),
            "Terça": tk.BooleanVar(value="Terça" in dias_salvos),
            "Quarta": tk.BooleanVar(value="Quarta" in dias_salvos),
            "Quinta": tk.BooleanVar(value="Quinta" in dias_salvos),
            "Sexta": tk.BooleanVar(value="Sexta" in dias_salvos)
        }
        
        frame_dias_edit = tk.Frame(scrollable_frame)
        frame_dias_edit.pack(pady=5)
        for dia, var in dias_vars_edit.items():
            tk.Checkbutton(frame_dias_edit, text=dia[:3], variable=var, font=("Arial", 10)).pack(side=tk.LEFT, padx=6)
            
        def salvar_edicao():
            #Coleta as informações e acina a camanda controladora 
            nome_fined = txt_novo_nome.get().strip()
            telefone_bruto = txt_novo_tel.get().strip()
             
            # Higieniza o telefone tirando parênteses, hifens e espaços antes de validar
            tel_fined = telefone_bruto.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
            
            # Agora a validação funciona perfeitamente com os números limpos!
            if not tel_fined.isdigit() or len(tel_fined) < 9:
                messagebox.showwarning("Erro", "Insira um telefone válido com apenas números!")
                return

            if any(char.isdigit() for char in nome_fined):
                messagebox.showwarning("Erro", "Nome não pode conter números!")
                return
            if not tel_fined.isdigit() or len(tel_fined) < 9:
                messagebox.showwarning("Erro", "Insira um telefone válido com apenas números!")
                return
            
            dias_atualizados = [dia for dia, var in dias_vars_edit.items() if var.get()]
            if len(dias_atualizados) == 0:
                messagebox.showwarning("Erro", "O aluno deve viajar ao menos 1 dia!")
                return
            string_dias = ",".join(dias_atualizados)
            
            # Instancia o objeto com os dados modificados
            associado_modificado = Associado(
                nome=nome_fined,
                cpf=cpf_selecionado,
                matricula=valores[2],
                telefone=tel_fined,
                tipo_associado=valores[4],
                dias_semana=string_dias
            )
            associado_modificado.turno_ida = cb_novo_ida.get()
            associado_modificado.turno_volta = cb_novo_volta.get()
            
            #Invoca diretamente a operação de atualização do DAO
            sucesso, msg = self.controller.associado_dao.atualizar(associado_modificado)
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Cadastro e logística atualizados com sucesso!")
                janela_edit.destroy()
                self.atualizar_dados() # Recarrega a tabela principal em tempo real
            else:
                messagebox.showerror("Erro ao Salvar", f"Falha no banco de dados: {msg}")

        frame_botoes_edit = tk.Frame(scrollable_frame)
        frame_botoes_edit.pack(pady=25)
        
        tk.Button(frame_botoes_edit, text="Salvar Alterações", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), width=16, command=salvar_edicao).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes_edit, text="Fechar / Sair", bg="#95a5a6", fg="white", font=("Arial", 10), width=12, command=janela_edit.destroy).pack(side=tk.LEFT, padx=5)

        janela_edit.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def remover(self):
        #Cancela o refistro no banco de dados atraves do CPF
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um registro.")
            return
        valores = self.tabela.item(selecao, "values")
        if messagebox.askyesno("Confirmar", f"Deseja realmente cancelar a matrícula de {valores[0]}?"):
            sucesso, msg = self.controller.remover_universitario(valores[1])
            if sucesso:
                messagebox.showinfo("Sucesso", "Excluído!")
                self.atualizar_dados() #Atualiza dados na tela 
            else:
                messagebox.showerror("Erro", msg)