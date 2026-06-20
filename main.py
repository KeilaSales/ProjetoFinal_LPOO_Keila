import tkinter as tk
from controler.associado_controller import AssociadoController
from view.inscricao_usuario_view import InscricaoUsuarioView
from view.gerenciamento_fretamento_view import GerenciamentoFretamentoView
# Mantenha os seus imports normais e adicione esta linha abaixo deles:
from view.gerenciamento_associado_view import GerenciamentoAssociadoView

class AplicacaoPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Transporte Estudantil")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        self.controller = AssociadoController()
        
        barra_menu = tk.Menu(self.root)
        self.root.config(menu=barra_menu)
        


        menu_inscricao = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Inscrição", menu=menu_inscricao)
        menu_inscricao.add_command(label="Realizar Nova Inscrição", command=self.abrir_portal_estudante)

        menu_admin = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Administrador", menu=menu_admin)
        menu_admin.add_command(label="👥 Gerenciar Universitários (Editar/Remover)", command=self.abrir_painel_associados)
        menu_admin.add_command(label="🚌 Logística de Frota (Fretamento)", command=self.abrir_painel_diretoria)
        # Texto de Boas-Vindas da Janela Inicial
        tk.Label(self.root, text="Bem-vindo ao Sistema de Transporte!", font=("Arial", 16, "bold"), fg="#1a365d").pack(pady=40)
        tk.Label(self.root, text="Use a barra de menus acima para navegar:", font=("Arial", 12)).pack(pady=10)
        tk.Label(self.root, text="Menu Inscrição -> Realizar Nova Inscrição\nMenu Administrador -> Painel de Controle (Diretoria)", font=("Arial", 11, "italic"), fg="#4a5568").pack(pady=10)
        

        
    def abrir_portal_estudante(self):
        # Aciona o pop-up rebatizado do aluno
        InscricaoUsuarioView(self.root, self.controller)
    
    
    def abrir_painel_diretoria(self):
        # Chama direto a View da Diretoria. A View se encarrega de pedir a senha!
        GerenciamentoFretamentoView(self.root, self.controller)
    
    def abrir_painel_associados(self):
        GerenciamentoAssociadoView(self.root, self.controller)


if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicacaoPrincipal(raiz)
    raiz.mainloop()