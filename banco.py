import sqlite3
from datetime import date

def criar_tabela():
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS "usuarios" (
        "id_usuario" INTEGER NOT NULL UNIQUE,
        "nome" VARCHAR(100) NOT NULL,
        "email" VARCHAR(150) NOT NULL UNIQUE,
        "cpf" INTEGER NOT NULL UNIQUE,
        "senha" VARCHAR(25) NOT NULL,
        "tipo" INTEGER NOT NULL,
        PRIMARY KEY("id_usuario")
    );

    CREATE TABLE IF NOT EXISTS "cursos" (
        "id_curso" INTEGER NOT NULL UNIQUE,
        "nome" VARCHAR(150) NOT NULL,
        "horario" INTEGER NOT NULL,
        PRIMARY KEY("id_curso")
    );

    CREATE TABLE IF NOT EXISTS "usuario_curso" (
        "id_usuario" INTEGER NOT NULL,
        "id_curso" INTEGER NOT NULL,
        FOREIGN KEY ("id_usuario") REFERENCES "usuarios"("id_usuario")
        ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY ("id_curso") REFERENCES "cursos"("id_curso")
        ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "atividades" (
        "id_atividade" INTEGER NOT NULL UNIQUE,
        "questao" TEXT NOT NULL,
        "A" VARCHAR NOT NULL,
        "B" VARCHAR NOT NULL,
        "C" VARCHAR NOT NULL,
        "D" VARCHAR NOT NULL,
		"dica" VARCHAR NOT NULL,
        "gabarito" VARCHAR(1) NOT NULL,
        "id_curso" INTEGER NOT NULL,
        PRIMARY KEY("id_atividade"),
        FOREIGN KEY ("id_curso") REFERENCES "cursos"("id_curso")
        ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "usuario_atividade" (
        "id_usuario" INTEGER NOT NULL,
        "id_atividade" INTEGER NOT NULL,
        "data" DATE NOT NULL DEFAULT CURRENT_DATE,
        "acerto" BOOLEAN NOT NULL DEFAULT 0,
		"status" BOOLEAN NOT NULL DEFAULT 0,
        FOREIGN KEY ("id_usuario") REFERENCES "usuarios"("id_usuario")
        ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY ("id_atividade") REFERENCES "atividades"("id_atividade")
        ON UPDATE NO ACTION ON DELETE NO ACTION
    );

	INSERT OR IGNORE INTO usuarios (nome,email,cpf,senha,tipo)
    VALUES ('Admin','coordenacao@escola.br',12345678900,'Adm@8900',2);

    """)

    conexao.commit()
    conexao.close()

def cpf_existe(cpf):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	cursor.execute("SELECT 1 FROM usuarios WHERE cpf = ?", (cpf,))
	check_cpf = cursor.fetchone()
	conexao.close()
	return check_cpf is not None

def email_existe(email):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	cursor.execute("SELECT 1 FROM usuarios WHERE email = ?", (email,))
	check_email = cursor.fetchone()
	conexao.close()
	return check_email is not None

def cadastrar_usuario():
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	print("\nPara cadastrar um usuário preencha as informações a seguir: ")
	nome_completo = input("\nDigite o nome completo do(a) usuário(a): ")
	email = input("\nDigite o e-mail do(a) usuário(a): ")
	cpf = input("\nDigite o CPF do(a) usuário(a): (Apenas números) ")
	if not cpf.isdigit() or len(cpf)!=11:
		return print(f"CPF incorreto. Certifique-se de usar apenas 11 números.")
	if cpf_existe(cpf):
		conexao.close()
		return print(f"\nO CPF inserido já está cadastrado.")
	if email_existe(email):
		conexao.close()
		return print(f"\nO e-mail inserido já está cadastrado.")

	senha = (nome_completo[:3])+"@"+(str(cpf)[-4:])
	tipo = input("\nQual o tipo de usuário: \n1- Aluno \n2- Professor \n3- Coordenador ")
	if tipo.isdigit() and len(tipo)==1:
		opcao = int(tipo)-1
		if opcao == 0:
			print(f"\nQual curso, ou cursos, o aluno está matriculado? ")
			lista_cursos()
			escolha = input("\nDigite o número do curso em que o aluno está matriculado: ")
			if escolha.isdigit() and curso_existe(escolha):
				cursor.execute("INSERT INTO usuarios (nome,email,cpf,senha,tipo) VALUES (?,?,?,?,?)", (nome_completo,email,cpf,senha,opcao))
				cursor.execute("INSERT INTO usuario_curso (id_usuario,id_curso) VALUES ((SELECT id_usuario FROM usuarios WHERE cpf = ?),(?));", (cpf,escolha))
				conexao.commit()
				conexao.close()
				return print(f"\nUsuário(a) {nome_completo} cadastrado(a) com sucesso.")
			else:
				return print(f"\nApenas números entre os da lista são escolhas possíveis.")
		elif opcao <=2:
			cursor.execute("INSERT INTO usuarios (nome,email,cpf,senha,tipo) VALUES (?,?,?,?,?)", (nome_completo,email,cpf,senha,opcao))
			conexao.commit()
			conexao.close()
			return print(f"\nUsuário(a) {nome_completo} cadastrado(a) com sucesso.")
		else:
			return print(f"\nO número digitado não referencia nenhum dos tipos possíveis ")
	else:
		return print(f"\nApenas números entre 1 a 3 são escolhas possíveis.")

def adicionar_curso(cpf):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	print("\nPara adicionar um curso preencha as informações a seguir: ")
	nome = input(f"\nDigite o nome do curso a ser adicionado: ")
	horario = (input("\nQual o horário do curso: \n1-Matutino \n2-Vespertino \n3-Noturno "))
	if horario.isdigit() and len(horario)==1:
		opcao = int(horario)-1
		if opcao <= 2:
			cursor.execute("INSERT INTO cursos (nome,horario) VALUES (?,?)", (nome,opcao))
			cursor.execute("INSERT INTO usuario_curso (id_usuario,id_curso) VALUES ((SELECT id_usuario FROM usuarios WHERE cpf = ?),(SELECT id_curso FROM cursos WHERE nome = ?));", (cpf,nome))
			conexao.commit()
			conexao.close()
			return print(f"\nCurso {nome} adicionado a lista com sucesso.")
		else:
			return print(f"\nO número digitado não referencia nenhum dos horários possíveis")
	else:
		return print("Apenas números entre 1 a 3 são escolhas possíveis.")

def lista_cursos():
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	cursor.execute('''
    SELECT c.id_curso,
		   c.nome,
	       c.horario,
		   SUBSTR(u.nome, 1, INSTR(SUBSTR(u.nome, INSTR(u.nome, ' ') + 1), ' ') + INSTR(u.nome, ' ') - 1)
    FROM cursos c
    INNER JOIN usuario_curso uc ON c.id_curso = uc.id_curso
    INNER JOIN usuarios u ON uc.id_usuario = u.id_usuario
    WHERE u.tipo = 1;
	''')
	resultados = cursor.fetchall()
	for linha in resultados:
		match linha[2]:
			case 0:
				print(f"\n{linha[0]}. Curso: {linha[1]} | Horário: Matutino | Professor: {linha[3]}")
			case 1:
				print(f"\n{linha[0]}. Curso: {linha[1]} | Horário: Vespertino | Professor: {linha[3]}")
			case 2:
				print(f"\n{linha[0]}. Curso: {linha[1]} | Horário: Noturno | Professor: {linha[3]}")

	conexao.close()

def curso_existe(curso):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	cursor.execute("SELECT 1 FROM cursos WHERE id_curso = ?", (curso,))
	check_curso = cursor.fetchone()
	conexao.close()
	return check_curso is not None

def adicionar_atividade(curso):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	print("\nPara adicionar uma atividade múltipla escolha preencha as informações a seguir: ")
	questao = input(f"\nDigite o texto da questão: ")
	a = input(f"\nPreencha as informações da alternativa A: ")
	b = input(f"\nPreencha as informações da alternativa B: ")
	c = input(f"\nPreencha as informações da alternativa C: ")
	d = input(f"\nPreencha as informações da alternativa D: ")
	dica = input(f"\nDigite uma dica para a atividade: ")
	gabarito = input(f"\nQual a respota da atividade? \nA \nB \nC \nD ").lower().strip()
	if len(gabarito)==1:
		lista = ['a','b','c','d']
		if gabarito in lista:
			cursor.execute("INSERT INTO atividades (questao,A,B,C,D,dica,gabarito,id_curso) VALUES (?,?,?,?,?,?,?,?)", (questao,a,b,c,d,dica,gabarito,curso))
			conexao.commit()
			conexao.close()
			return print(f"\nAtividade adicionada a lista com sucesso.")
		else:
			return print(f"\nA letra digitada não referencia nenhuma das alternativas possíveis")
	else:
		return print("Apenas letras de A a D são escolhas possíveis.")

def ranking_parcial(curso):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	print("\nRanking dos 3 melhores alunos do curso: ")
	cursor.execute('''
	SELECT u.nome,
    	   COUNT (CASE WHEN ua.acerto = 1 THEN 1 end)
    FROM usuarios u
  	LEFT JOIN usuario_atividade ua ON u.id_usuario = ua.id_usuario
  	LEFT JOIN usuario_curso uc ON u.id_usuario = uc.id_usuario
    WHERE u.tipo = 0 AND uc.id_curso = ?
    GROUP by u.nome
    ORDER BY COUNT (ua.acerto) DESC
    Limit 3;
	''', (curso,))
	resultados = cursor.fetchall()
	for item in resultados:
		lugar = 1
		print(f"\n{lugar}º - {item[0]} \n{item[1]} Estrelas")
		lugar+=1
	conexao.close()

def ranking_total(curso):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	print("\nRanking de todos os alunos do curso: ")
	cursor.execute('''
	SELECT u.nome,
    	   COUNT (CASE WHEN ua.acerto = 1 THEN 1 end),
           COUNT (CASE WHEN ua.status = 1 THEN 1 end)
    FROM usuarios u
  	LEFT JOIN usuario_atividade ua ON u.id_usuario = ua.id_usuario
  	LEFT JOIN usuario_curso uc ON u.id_usuario = uc.id_usuario
    WHERE u.tipo = 0 AND uc.id_curso = ?
    GROUP by u.nome
    ORDER BY COUNT (ua.acerto) DESC;
	''', (curso,))
	resultados = cursor.fetchall()
	for item in resultados:
		lugar = 1
		print(f"\n{lugar}º - {item[0]} \n{item[1]} Estrelas | {item[2]} Atividades feitas")
		lugar+=1
	conexao.close()

def listar_atividades(curso):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	print("\nLista de todas as atividades do curso: ")
	atividades = []
	cursor.execute('''
	SELECT c.nome,
    	   a.id_atividade,
           SUBSTR(a.questao,1,50)
    FROM atividades a
    INNER JOIN cursos c ON a.id_curso = c.id_curso
    WHERE c.id_curso = ?;
	''', (curso,))
	resultados = cursor.fetchall()
	for item in resultados:
		atividades.append(item[1])
		lugar=1
		print(f"\n{item[0]} \nAtividade {lugar}: {item[2]}...")
		lugar+=1
	conexao.close()
	return atividades

def mostrar_atividade(atividade):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	cursor.execute('''
    SELECT a.questao,
    	   a.a,
           a.b,
           a.c,
           a.d
    FROM atividades a
    WHERE a.id_atividade = ?;
	''', (atividade,))
	resultados = cursor.fetchall()
	for item in resultados:
		print(f"\nAtividade \n{item[0]} \n\na){item[1]} \n\nb){item[2]} \n\nc){item[3]} \n\nd){item[4]}")
	conexao.close()

def pedir_dica(atividade):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	cursor.execute('''
    SELECT a.dica
    FROM atividades a
    WHERE a.id_atividade = ?;
''', (atividade,))
	resultado = cursor.fetchone()
	for item in resultado:
		print(f"\nDica: {item}")
	conexao.close()

def realizar_atividade(cpf,atividade,resposta):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	if atividade_feita(cpf,atividade):
		return repetir_atividade(cpf,atividade,resposta)
	cursor.execute('''
    SELECT a.gabarito
    FROM atividades a
    WHERE a.id_atividade = ?;
				''',(atividade,))
	gabarito = cursor.fetchone()
	if resposta in gabarito:
		cursor.execute(''' INSERT INTO usuario_atividade (id_usuario,id_atividade,acerto,status)
VALUES ((SELECT id_usuario FROM usuarios WHERE cpf = ?),?,?,?)''', (cpf,atividade,1,1))
		conexao.commit()
		conexao.close()
		return print(f"\n Resposta Correta. Parabéns.")
	else:
		cursor.execute(''' INSERT INTO usuario_atividade (id_usuario,id_atividade,acerto,status)
VALUES ((SELECT id_usuario FROM usuarios WHERE cpf = ?),?,?,?,?)''', (cpf,atividade,0,1))
		conexao.commit()
		conexao.close()
		return print(f"\nResposta Incorreta. Sinto Muito.")

def atividade_feita(cpf,atividade):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	cursor.execute('''
	SELECT 1 FROM usuario_atividade ua
    INNER JOIN usuarios u ON ua.id_usuario = u.id_usuario
    WHERE ua.id_usuario =(CASE WHEN u.cpf = ? THEN u.id_usuario END) AND ua.id_atividade = ?;
	''', (cpf,atividade,))
	check_cpf = cursor.fetchone()
	conexao.close()
	return check_cpf is not None

def repetir_atividade(cpf,atividade,resposta):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	cursor.execute('''
    UPDATE usuario_atividade
    SET status = 1
    FROM usuarios
    WHERE usuario_atividade.id_atividade = ? AND usuario_atividade.id_usuario=(CASE WHEN usuarios.cpf = ? THEN usuarios.id_usuario END);
	''',(atividade,cpf,))
	
	cursor.execute('''
	SELECT a.gabarito
    FROM atividades a
    WHERE a.id_atividade = ?;
	''', (atividade,))
	gabarito = cursor.fetchone()
	if resposta in gabarito:
		conexao.close()
		return print(f"\nResposta Correta. Parabéns.")
	else:
		conexao.close()
		return print(f"\nResposta Incorreta. Sinto Muito.")