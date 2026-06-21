# Sistema de Transporte Estudantil 

**Componente Curricular:** Linguagem de Programação Orientada a Objetos (LPOO)  
**Acadêmica:** Keila de Sales Gonçalves  
**Linguagem:** Python 3.13 | **SGBD:** PostgreSQL  

---

## Descrição Detalhada do Projeto
Este projeto consiste no desenvolvimento de um **Sistema de Gestão de Transporte Universitário**, projetado especificamente para solucionar os desafios logísticos e financeiros enfrentados diariamente no transporte intermunicipal de estudantes. 

O sistema foi inteiramente **inspirado na ALU (Associação Lagoense de Universitários)**, que organiza o deslocamento diário de centenas de acadêmicos que residem em Lagoa Vermelha e estudam nos polos universitários da cidade de Passo Fundo (como UPF, IFSul, Atitus, entre outras).

### O Problema Resolvido
Até então, o controle de quais alunos viajavam em quais dias era feito por planilhas manuais e suscetíveis a erros, dificultando o dimensionamento correto dos veículos antes do fechamento das inscrições. 

Este software unifica as duas pontas da associação:
1. **O Portal do Estudante:** Onde o universitário realiza sua inscrição informando seus dados cadastrais, a instituição de ensino, os dias exatos da semana em que utilizará o transporte e os turnos independentes de ida e de volta (já que muitos viajam à tarde e retornam à noite).
2. **O Painel Administrativo (Diretoria):** Uma área restrita voltada à gestão onde é possível auditar a lista de passageiros, realizar alterações cadastrais fora do prazo, cancelar matrículas e acompanhar a inteligência logística do sistema.

---

## Manual de Instruções e Navegação (Como Executar)

### Pré-requisitos Técnicos
Antes de iniciar, certifique-se de ter o **PostgreSQL** instalado e crie um banco de dados chamado `lpoo_projeto_keila`. Também é necessário instalar o driver de conexão do banco de dados no terminal do seu Python:
```bash
pip install psycopg2

---


