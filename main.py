# ARQUIVO PRINCIPAL: Ponto de entrada e Orquestrador do Sistema
import tkinter as tk
from controler.associado_controller import AssociadoController
from view.inscricao_usuario_view import InscricaoUsuarioView
from view.gerenciamento_fretamento_view import GerenciamentoFretamentoView
from view.gerenciamento_associado_view import GerenciamentoAssociadoView

class AplicacaoPrincipal:
    def __init__(self, root):
        # Janela MASTER principal criada pelo loop do Tkinter
        self.root = root
        self.root.title("Sistema de Transporte Estudantil")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        # INSTANCIAÇÃO GLOBAL: Cria o único controlador que será compartilhado por todas as telas
        self.controller = AssociadoController()
        # COMPONENTE DE MENU: Constrói a barra superior de navegação em cascata
        barra_menu = tk.Menu(self.root)
        self.root.config(menu=barra_menu)
        

        #Incrição
        menu_inscricao = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Inscrição", menu=menu_inscricao)
        menu_inscricao.add_command(label="Realizar Nova Inscrição", command=self.abrir_portal_estudante)

        #Administração
        menu_admin = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Administrador", menu=menu_admin)
        menu_admin.add_command(label="👥 Gerenciar Universitários (Editar/Remover)", command=self.abrir_painel_associados)
        # Texto de Boas-Vindas da Janela Inicial
        tk.Label(self.root, text="Bem-vindo ao Sistema de Transporte!", font=("Arial", 16, "bold"), fg="#1a365d").pack(pady=40)
        tk.Label(self.root, text="Use a barra de menus acima para navegar:", font=("Arial", 12)).pack(pady=10)
        tk.Label(self.root, text="Inscrição -> Realizar Nova Inscrição\nAdministrador -> Gerenciar Universitários/Frota (Diretoria)", font=("Arial", 11, "italic"), fg="#4a5568").pack(pady=10)
        

        
    def abrir_portal_estudante(self):
        # Inicializa e exibe o formulário de cadastro do aluno
        # Passa a raiz (janela master) e o controlador instanciado como dependências
        InscricaoUsuarioView(self.root, self.controller)
    
    
    def abrir_painel_diretoria(self):
        #Inicializa o painel analítico básico de logística de frotas 
        GerenciamentoFretamentoView(self.root, self.controller)
    
    def abrir_painel_associados(self):
        # Abre a central administrativa de associados (que gerencia login, busca e edição)
        GerenciamentoAssociadoView(self.root, self.controller)


if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicacaoPrincipal(raiz)
    raiz.mainloop()