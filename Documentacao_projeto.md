# Documentação do Projeto - Sistema de Transporte Estudantil

**Disciplina:** Análise e Projeto de Sistemas (APS) & Linguagem de Programação Orientada a Objetos (LPOO)  
**Aluno:** Keila de Sales Gonçalves

---

## 1. Descrição e Delimitação do Escopo

### Cenário do Sistema e Propósito
O Sistema de Transporte Estudantil tem como propósito gerenciar o fluxo de inscrições, alocação de frota e controle financeiro de estudantes universitários que se deslocam diariamente de Lagoa Vermelha para os polos universitários de Passo Fundo. Atualmente, a associação lida com uma média de 140 associados pulverizados em diferentes turnos (tarde e noite), necessitando de uma ferramenta automatizada para extinguir o controle por planilhas manuais.

### Problema Resolvido
O sistema resolve o problema de dimensionamento de frota e precificação justa. Antes do encerramento do prazo de inscrição, a diretoria não possuía dados exatos de quantos alunos utilizavam o transporte por dia da semana e por turno específico (considerando que há estudantes que vão à tarde e retornam no turno da noite). O sistema consolida esses dados e sugere a frota necessária (vans, micro-ônibus ou ônibus), além de calcular a mensalidade de forma progressiva (premiando com diárias mais baratas os alunos frequentes e aplicando as taxas corretas de Matrícula e Rematrícula).

### Público-Alvo e Níveis de Acesso
1. **Estudante Associado:** Realiza autocadastro, solicita inscrição informando turnos de ida/volta e dias da semana, e consulta suas mensalidades.
2. **Diretoria (Tesoureiro):** Acessa o painel financeiro, relatórios de arrecadação e conferência de custos.
3. **Administrador (Diretor/Vice):** Possui controle total para alterar cadastros após o fechamento dos prazos e reconfigurar valores do sistema na Tela de Monitoramento.

### Escalabilidade do Escopo
*Nota de Projeto:* Embora o sistema seja inicialmente homologado para a rota Lagoa Vermelha x Passo Fundo, a arquitetura de banco de dados e as classes de domínio foram projetadas para suportar múltiplas cidades e novos trajetos no futuro apenas alimentando as tabelas correspondentes, sem necessidade de alteração no código-fonte.

---

## 2. Fase de Análise (Requisitos e Regras)

### 2.1 Requisitos Funcionais (RF)

O sistema deve atender, no mínimo, aos seguintes requisitos de negócio:

* **RF001 - Autenticação por Perfil:** O sistema deve permitir o login diferenciado para Estudantes, Diretoria e Administradores.
* **RF002 - Cadastro de Associados (CRUD):** O sistema deve permitir a inclusão, alteração, consulta e exclusão de estudantes associados, identificando se são "Novos" ou "Antigos".
* **RF003 - Cadastro de Rotas (CRUD):** O sistema deve permitir o gerenciamento de rotas, incluindo o nome do trajeto e a cidade de destino.
* **RF004 - Solicitação de Inscrição:** O sistema deve permitir ao associado vincular-se a uma rota escolhendo de 1 a 5 dias da semana, o turno de ida e o turno de volta.
* **RF005 - Bloqueio de Inscrição por Prazo:** O sistema deve impedir que associados alterem ou façam novas inscrições após a data limite estipulada pela diretoria.
* **RF006 - Alteração Administrativa Exclusiva:** O sistema deve permitir que apenas o perfil de Administrador altere os dias da semana ou cancele cadastros após o encerramento do prazo de inscrições.
* **RF007 - Cálculo de Mensalidade Automatizado (Pattern Strategy):** O sistema deve calcular o valor da mensalidade aplicando o preço correspondente aos dias da semana escolhidos e injetar a taxa de matrícula (R$ 200) ou rematrícula (R$ 80) conforme o tipo do associado.
* **RF008 - Monitoramento e Otimização de Frota:** O sistema deve exibir para a diretoria a soma total de alunos por dia da semana e turno, recomendando a combinação ideal de veículos (Van para até 15 alunos, Micro-ônibus para até 30, e Ônibus para até 45).
* **RF009 - Relatório de Arrecadação:** O sistema deve fornecer ao perfil de Tesoureiro um demonstrativo financeiro com a previsão de receita mensal baseada nas inscrições ativas.
* **RF010 - Histórico Financeiro do Aluno:** O sistema deve exibir para o associado logado os seus débitos vigentes, discriminando a mensalidade base e a taxa de adesão semestral.

### 2.2 Requisitos Não Funcionais (RNF)

Os requisitos não funcionais definem as restrições técnicas, qualidades e características de infraestrutura do sistema:

* **RNF001 - Linguagem de Programação:** O sistema deve ser desenvolvido obrigatoriamente utilizando a linguagem Python.
* **RNF002 - Sistema Gerenciador de Banco de Dados (SGBD):** A persistência dos dados deve ser realizada em um banco de dados relacional PostgreSQL.
* **RNF003 - Interface Gráfica (GUI):** A interface com o usuário deve ser construída utilizando a biblioteca Tkinter, garantindo padronização visual nativa e facilidade de uso pela diretoria.
* **RNF004 - Padrão de Arquitetura:** O código fonte do sistema deve ser estruturado utilizando a separação de responsabilidades em módulos/pacotes com as iniciais maiúsculas (Model, View, Controller e DAO).
* **RNF005 - Operação Local:** O sistema deve funcionar de forma totalmente local/offline, armazenando e consultando os dados diretamente no servidor PostgreSQL configurado, sem depender de conexão com a internet externa para sua execução diária.

### 2.3 Regras de Negócio (RN)

As regras de negócio descrevem as políticas operacionais da Associação (ALU) aplicadas ao software:

* **RN001 - Política de Desconto Progressivo e Adesão:** O cálculo da mensalidade base deve aplicar taxas fixas decrescentes de acordo com a frequência de dias escolhidos (1 dia: R$ 280,00; 2 dias: R$ 240,00; 3 dias: R$ 200,00; 4 dias: R$ 180,00; 5 dias: R$ 160,00). Adicionalmente, no primeiro mês do semestre correspondente ao contrato, associados categorizados como "NOVO" sofrem acréscimo de R$ 200,00 (Matrícula) e associados "ANTIGO" sofrem acréscimo de R$ 80,00 (Rematrícula).
* **RN002 - Parametrização para Dimensionamento de Frota:** A lógica de recomendação automática de veículos na **Tela de Monitoramento** deve obedecer rigorosamente à capacidade limite dos modais cadastrados:
  * Até 15 alunos alocados no turno específico: Sugerir **Van**.
  * De 16 a 30 alunos alocados no turno específico: Sugerir **Micro-ônibus**.
  * De 31 a 45 alunos alocados no turno específico: Sugerir **Ônibus** (Capacidade 45).
  * Acima de 45 alunos: Combinar os veículos de forma incremental e somatória (Exemplo: 60 alunos = 1 Ônibus + 1 Van).