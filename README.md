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

### Guia de Navegação pelas Abas

1. Menu Inscrição -> Realizar Nova Inscrição: Esta é a porta de entrada do estudante associado. Ao abrir o formulário, o aluno preenche seus dados (Nome, CPF, Telefone, Matrícula), escolhe a instituição de ensino, marca seus turnos de funcionamento e seleciona em quais dias úteis (de Segunda a Sexta) usará o transporte. Ao confirmar, o sistema gera na tela um Recibo de Inscrição detalhado com os valores calculados pelo padrão Strategy.

2. Menu Administrador -> Gerenciar Universitários (Área Administrativa): Para acessar esta área restrita da diretoria, o sistema exige uma credencial de segurança. A senha configurada para entrar é "diretoria123" .

3. Barra de Pesquisa e Listagem Dinâmica: Dentro do painel administrativo, a diretoria visualiza a tabela geral de associados. No topo, há a funcionalidade de Lista de Pesquisa. Conforme o administrador digita as letras do nome de um estudante, a tabela se atualiza, filtrando e localizando o registro de forma instantânea.

4. Análise de Sugestão de Frota por Turno: No rodapé do gerenciamento de associados, encontra-se o botão Ver Frota (Logística por Turno). Ele abre a tela estatística da diretoria, que exibe o total bruto de passageiros divididos por cada dia da semana e segmentados em 6 colunas (Ida Manhã, Volta Manhã, Ida Tarde, Volta Tarde, Ida Noite, Volta Noite).

- Como funciona o botão Analisar: O administrador clica em cima de qualquer linha da semana (ex: Quinta-feira) e clica no botão Analisar Transporte para o Dia. O sistema abre um pop-up focado sugerindo o veículo ideal baseado na ocupação daquele turno específico (ex: indicando uma Van se houver até 15 alunos na manhã, Micro-ônibus se houver até 28 na tarde, ou Ônibus Convencional para a noite).

## Modelagem Arquitetural

O projeto foi estruturado utilizando a separação rigorosa de responsabilidades do padrão MVC (Model, View, Controller), dividida em módulos independentes (model/, dao/, controler/, view/).

A documentação completa dos Casos de Uso, com os fluxos do sistema mapeados, está descrita no arquivo: Documentacao_projeto.md.

## Padrões de Projeto Implementados

1. Data Access Object (DAO): Centralização de todas as queries de persistência SQL (AssociadoDAO, RotaDAO, InscricaoDAO) herdando os métodos abstratos obrigatórios de GenericDAO.py.

2. Strategy: Isolamento comportamental no módulo CalculoMensalidade.py para calcular de forma limpa o desconto progressivo baseado nos dias úteis da semana de cada aluno e injetar as taxas corretas de Matrícula (para alunos NOVOS) ou Rematrícula (para alunos ANTIGOS).


## Declaração de Uso de Inteligência Artificial (IA)

Em conformidade com as regras pedagógicas do projeto, declara-se o uso assistido de ferramentas de IA generativa para fins de refatoração e suporte técnico:

1. Google Gemini (Modelo Gemini 1.5 Pro): Atuou como assistente na camada de interface gráfica (view/), auxiliando na estruturação de componentes de layout do Tkinter, na configuração de eventos dinâmicos por digitação (<KeyRelease>) para a barra de pesquisa por nome e no ajuste de foco e posicionamento de janelas filhas e pop-ups (Toplevel).

2. OpenAI ChatGPT: Atuou como suporte de engenharia de dados na camada de persistência (dao/), auxiliando na revisão de estruturas de conexão Estática com a classe DatabaseConfig, tratamento normativo de transações e controle de segurança de rollback em falhas com a biblioteca psycopg2.
