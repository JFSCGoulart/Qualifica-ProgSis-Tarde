import sqlite3
conexao=sqlite3.connect('objetos.db')
cursor=conexao.cursor()

#tabela de cada curso
cursor.execute('''
    CREATE TABLE IF NOT EXISTS conteudo(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo VARCHAR(100) NOT NULL,
        descricao VARCHAR(10000),
        professor_id INTEGER NOT NULL,
        data_upload DATE NOT NULL)
               ''')

#tabela de cada questao(com a pergunta, alternativas, resposta e dica)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS questao(
        numero_questao INTEGER NOT NULL,
        id_conteudo INTEGER NOT NULL,
        enunciado VARCHAR NOT NULL,
        alternativa_a VARCHAR(500) NOT NULL,
        alternativa_b VARCHAR(500) NOT NULL,
        alternativa_c VARCHAR(500) NOT NULL,
        alternativa_d VARCHAR(500) NOT NULL,
        alternativa_certa VARCHAR(5) NOT NULL,
        dica VARCHAR(200) NOT NULL,
        FOREIGN KEY (id_conteudo) REFERENCES conteudo(id)
)
''')


