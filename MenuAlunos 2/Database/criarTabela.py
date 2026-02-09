import sqlite3

conexao = sqlite3.connect('Database/cursos.db')
cursor = conexao.cursor()

# cursor.execute("""
#       CREATE TABLE progresso (
#       id INTEGER PRIMARY KEY AUTOINCREMENT,
#       id_aluno INTEGER UNIQUE,
#       estrelas INTEGER DEFAULT 0
#  )
#          """)

# cursor.execute('''CREATE TABLE IF NOT EXISTS cursos(
#                id INTEGER PRIMARY KEY AUTOINCREMENT,
#                nome VARCHAR(100)
#                )
               
#                ''')

# cursor.execute('''CREATE TABLE IF NOT EXISTS matriculas(
#                id_aluno INTEGER NOT NULL,
#                id_curso INTEGER NOT NULL,
#                FOREIGN KEY (id_curso) REFERENCES cursos(id)
#                )
               
#                ''')

# cursor.execute("""
#   CREATE TABLE IF NOT EXISTS atividades (
#       id INTEGER PRIMARY KEY AUTOINCREMENT,
#       enunciado TEXT NOT NULL,
#       opcao_a TEXT NOT NULL,
#       opcao_b TEXT NOT NULL,
#       opcao_c TEXT NOT NULL,
#       opcao_d TEXT NOT NULL,
#       gabarito TEXT NOT NULL,
#       dica TEXT NOT NULL,
#       id_curso INTEGER NOT NULL,
#       FOREIGN KEY (id_curso) REFERENCES cursos(id)      
#  )""")

# cursor.execute("""
#       CREATE TABLE progressoAtividade (
#       id INTEGER PRIMARY KEY AUTOINCREMENT,
#       id_aluno INTEGER UNIQUE,
#       id_curso INTEGER UNIQUE,
#       Quant_feita INTEGER,
#       Quant_acertada INTEGER,
#       Quant_errou INTEGER , 
#       FOREIGN KEY (id_curso) REFERENCES curso(id),               
#       FOREIGN KEY (id_aluno) REFERENCES matriculas(id_aluno)              
#  )
#          """)


cursor.execute('''
 CREATE TABLE IF NOT EXISTS usuarios (
     id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
     nome VARCHAR(100),
     email VARCHAR(150),
     cpf INTEGER,
     senha VARCHAR(25),
     tipo INTEGER
 )
 ''')

cursor.execute('''
 CREATE TABLE IF NOT EXISTS cursos (
     id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
     nome VARCHAR(150),
     horario INTEGER
 )
 ''')

cursor.execute('''
 CREATE TABLE IF NOT EXISTS atividades (
     id_atividades INTEGER PRIMARY KEY AUTOINCREMENT,
     questao TEXT,
     A VARCHAR,
     B VARCHAR,
     C VARCHAR,
     D VARCHAR,
     dica VARCHAR,
     gabarito INTEGER,
     id_curso INTEGER,
     FOREIGN KEY (id_curso) REFERENCES cursos (id_curso)
 )
 ''')

cursor.execute('''
 CREATE TABLE IF NOT EXISTS usuario_curso (
     id_usuario INTEGER,
     id_curso INTEGER,
     PRIMARY KEY (id_usuario, id_curso),
     FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario),
     FOREIGN KEY (id_curso) REFERENCES cursos (id_curso)
 )
 ''')

cursor.execute('''
 CREATE TABLE IF NOT EXISTS usuario_atividade (
     id_usuario INTEGER,
     id_atividade INTEGER,
     data DATE,
     acerto BOOLEAN,
     status BOOLEAN,
     FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario),
     FOREIGN KEY (id_atividade) REFERENCES atividades (id_atividades)
 )
 ''')


conexao.commit()
print("Adicionado com sucesso!")
conexao.close()