import sqlite3
conexao=sqlite3.connect('objetos.db')
cursor=conexao.cursor()
from datetime import date
from Models.funcoes_tarefas import adicionar_questao, excluir_atividade, ver_questoes, ver_tudo
import os

#Função para adicionar cursos!

def adicionar_curso():
    titulo_curso = input("digite o titulo do curso")
    horario = input("digite o horario do curso")

    cursor.execute("""
        INSERT INTO cursos (nome, horario)
        VALUES (?, ?)
    """, (titulo_curso, horario))

    print(f"o curso de {titulo_curso} foi adicionado com sucesso.")
    conexao.commit()
    

#Função usada para ver os cursos cadastrados, (utilizada na função de excluir cursos!)

def ver_curso():
    cursor.execute("SELECT * FROM cursos")
    resultado = cursor.fetchall()

    if not resultado:
        print("Não existe nenhum curso cadastrado.")
        return
    else:
        for lista in resultado:
            print(f"ID do curso: {lista[0]}\n"
                  f"Nome do curso: {lista[1]}\n"
                  f"Horário: {lista[2]}\n")


#Função utilizada para ver matérias do professor atráves do ID do professor!

def ver_materia():
    cursor.execute("SELECT * FROM cursos")
    resultado = cursor.fetchall()

    if not resultado:
        print("Não existe nenhum curso cadastrado.")
    else:
        for lista in resultado:
            print(f"ID: {lista[0]}  Curso: {lista[1]}")

        opcao = input("Deseja acessar o conteúdo do curso?(s/n): ").lower()
        if opcao == "s":
            ver_tudo()
            
                
#Função utilizade para excluir o curso e tudo o que corresponde ao curso, (está função apaga as questões também)  
         
def excluir_curso():
    ver_curso()

    id_curso = int(input("digite o id do curso que você deseja excluir: "))

    cursor.execute("SELECT 1 FROM cursos WHERE id_curso = ?", (id_curso,))
    procura = cursor.fetchone()

    if procura is None:
        print("O curso não existe")
        return
    else:
        pergunta = input("Você realmente deseja apagar o curso e as questões?(s/n): ").lower()

        if pergunta == "s":
            cursor.execute("DELETE FROM atividades WHERE id_curso = ?", (id_curso,))
            cursor.execute("DELETE FROM cursos WHERE id_curso = ?", (id_curso,))
            conexao.commit()

            print("O curso foi excluido com sucesso.")
            
               
#Função para sair!
                             
def sair():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    conexao.close()



    



    
    
    
    
    
