# CLASSE ABSTRATA / INTERFACE: Define o contrato de banco de dados
from abc import ABC, abstractmethod

# Serve apenas como molde e não pode ser instanciada diretamente
class GenericDAO(ABC):
    @abstractmethod 
    def salvar(self, objeto):
        pass
    
    @abstractmethod
    def listar_todos(self):
        pass
    
    @abstractmethod
    def remover(self, id_objeto):
        pass
    
    @abstractmethod
    def atualizar(self, objeto):
        pass