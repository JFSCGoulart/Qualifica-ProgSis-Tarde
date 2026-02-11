# Gestão Escolar

Uma plataforma web desenvolvida em Python para gestão de cursos, acompanhamento de progresso acadêmico e correção de atividades.

## Funcionalidades
- **Portal do Aluno:** Visualização de progresso, notas, atividades e downloads.
- **Área do Professor:** Cadastro de atividadese e acompanhamento de desempenho.
- **Área do Coordenador:** Acompanhamento de progresso e desempenho.
- **Sistema de Login:** Acesso restrito por perfil (Aluno/Professor/Coordenador).
- **Histórico Dinâmico:** Gerenciamento de progresso em tempo real.

##  Tipos de Usuários

### Aluno

- Ver lista de cursos/módulos disponíveis
- Fazer atividades variadas
- Pedir dica antes de responder
- Ganhar 1 estrela por acerto
- Perder 1 vida por erro (começa com 3 vidas por curso)
- Ver seu progresso: estrelas, vidas, atividades feitas hoje
- Resetar seu próprio progresso
- Ver o ranking dos 3 melhores alunos


### Coordenador

- Ver ranking completo da turma (todos os alunos, com estrelas e acertos)
- Ver quantas atividades foram feitas hoje por todos
- Ver desempenho por curso (ex: “80% acertaram o módulo de Comunicação”)
- Não faz atividades nem edita conteúdo — só acompanha


### Professor

- Adicionar novo curso/módulo (ex: “Gestão de Tempo”)
- Adicionar nova atividade (escolhe o tipo, escreve pergunta, opções, resposta correta e dica)
- Ver a lista de cursos e atividades cadastradas
- Não vê estrelas nem ranking — só gerencia conteúdo

##  Tecnologias utilizadas
- Python 3
- SQlite3

### 📂 Descrição das Pastas e Arquivos

```text
Projeto final qualifica/
│
├── data/
│   └── banco de dados.db
│
├── src/
│ ├── main.py
│ │ 
│ ├── autenticacao/
│ │ └── usuarios.py
│ │
│ ├── core/
│ │  ├── atividades.py
│ │  └── progresso.py
│ │
│ └──database/
│   └── banco.py
├
│── docs/
├
└── README.md
```

Adaptado para desenvolvimento Web no **VS Code**:


- `data/`: Arquivos brutos, logs ou temporários.
  - `banco de dados.db`: arquivo de banco de dados do sistema.
- `src/`
  -`main.py`: menu principal, login e redirecionamento por tipo de usuário.
- `src/autenticacao/`: Autenticação.
  - `usuarios.py`: cadastro, verificação de tipo, login.
- `src/core/`: Inteligência do sistema .
  - `atividades.py`: tipos de atividade, correção, dicas.
  - `progresso.py`: vidas, estrelas, histórico, ranking.
- `src/database/`: responsável pela configuração e gerenciamento do banco de dados, incluindo conexão, inicialização, modelos de tabelas e consultas utilizadas pela aplicação.
  - `banco.py`: conexão, criação de tabelas, leitura do atividades_extra.txt.
- `doc/`: Documentos do projeto.

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/JFSCGoulart/Qualifica-ProgSis-Tarde

