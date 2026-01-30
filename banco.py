import sqlite3

conexao = sqlite3.connect('banco.db')
cursor = conexao.cursor()
cursor.executescript('''
CREATE TABLE IF NOT EXISTS "usuarios" (
	"id_usuario" INTEGER PRIMARY KEY AUTOINCREMENT,
	"nome" VARCHAR(100) NOT NULL,
	"email" VARCHAR(150) NOT NULL UNIQUE,
	"cpf" INTEGER(11) NOT NULL UNIQUE,
	"senha" VARCHAR(25) NOT NULL,
	"tipo" INTEGER(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS "cursos" (
	"id_curso" PRIMARY KEY AUTOINCREMENT,
	"nome" VARCHAR(100) NOT NULL,
	"horario" INTEGER(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS "usuario_curso" (
	"id_usuario" INTEGER NOT NULL,
	"id_curso" INTEGER NOT NULL	FOREIGN KEY ("id_usuario") REFERENCES "usuarios"("id_usuario")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("id_curso") REFERENCES "cursos"("id_curso")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "atividades" (
	"id_atividade" INTEGER PRIMARY KEY AUTOINCREMENT,
	"questao" TEXT NOT NULL,
	"A" VARCHAR NOT NULL,
	"B" VARCHAR NOT NULL,
	"C" VARCHAR NOT NULL,
	"D" VARCHAR NOT NULL,
	"gabarito" VARCHAR(1) NOT NULL,
	"id_curso" INTEGER NOT NULL,
	FOREIGN KEY ("id_curso") REFERENCES "cursos"("id_curso")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "usuario_atividade" (
	"id_usuario" INTEGER NOT NULL,
	"id_atividade" INTEGER NOT NULL,
	"data" DATE NOT NULL,
	"status" BOOLEAN NOT NULL DEFAULT FALSE	FOREIGN KEY ("id_usuario") REFERENCES "usuarios"("id_usuario")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("id_atividade") REFERENCES "atividades"("id_atividade")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

''')

conexao.commit()
conexao.close()