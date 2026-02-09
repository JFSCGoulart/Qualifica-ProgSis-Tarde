import sqlite3
conexao=sqlite3.connect('objetos.db')
cursor=conexao.cursor()
from datetime import date
from funcoes_tarefas import *
import os

#Função para adicionar cursos!

def adicionar_curso():
    titulo_curso = input("digite o titulo do curso")
    descricao_curso = input("digite a descrição do curso")
    professor_id = input("digite o seu id")
    data_upload = date.today()
    cursor.execute("INSERT INTO conteudo (titulo, descricao, professor_id, data_upload) VALUES(?,?,?,?)",
                        (titulo_curso, descricao_curso, 
                            professor_id, data_upload))
    print(f"o curso de {titulo_curso} foi adicionado com sucesso.")
    conexao.commit()
    

#Função usada para ver os cursos cadastrados, (utilizada na função de excluir cursos!)

def ver_curso():
    id_professor = int(input("digite seu id"))
    cursor.execute("SELECT 1 FROM conteudo WHERE professor_id = ?", (id_professor,))
    resultado = cursor.fetchone()
    if resultado is None:
        print("Não existe nenhum curso seu cadastrado.")
        return
    else:
            cursor.execute("SELECT * FROM conteudo WHERE professor_id = ?", (id_professor,))
            resultado = cursor.fetchall()
            for lista in resultado:
                print(f"ID do curso: {lista[0]}\n"
                    f"Título do curso: {lista[1]}\n"
                    f"Descrição do curso: {lista[2]}\n"
                    f"ID do professor: {lista[3]}\n"
                    f"Data de upload: {lista[4]}\n")

            
#Função utilizada para ver matérias do professor atráves do ID do professor!

def ver_materia():
        professor_id = int(input("digite o ID do professor: "))
        
        cursor.execute("SELECT titulo FROM conteudo WHERE professor_id = ?", (professor_id,))
        resultado = cursor.fetchone()
        if resultado is None:
            print("Não existe nenhum curso cadastrado no seu ID.")
        else:
            cursor.execute("SELECT * FROM conteudo WHERE professor_id = ?", (professor_id,))
            resultado = cursor.fetchall()
            for lista in resultado:
                print(f"ID: {lista[0]}  titulo: {lista[1]}")
            opcao = input("Deseja acessar o conteúdo do curso?(s/n): ").lower()
            if opcao == "s":
                ver_tudo()
            
                
#Função utilizade para excluir o curso e tudo o que corresponde ao curso, (está função apaga as questões também)  
         
def excluir_curso():
    ver_curso()
    id_curso = int(input("digite o id do curso que você deseja excluir"))
    cursor.execute("SELECT 1 FROM conteudo WHERE id = ?", (id_curso,))
    procura = cursor.fetchone()
    if procura is None:
            print("O curso não existe")
            return
    else:
        pergunta = input("Você realmente deseja apagar o conteudo e as questões?(s/n)").lower()
        if pergunta == "s":
            cursor.execute("DELETE FROM conteudo WHERE id = ?", (id_curso,))
            cursor.execute("DELETE FROM questao WHERE id_conteudo = ?", (id_curso,))
            conexao.commit()
            print(f"O curso foi excluido com sucesso.")
            
               
#Função para sair!
                             
def sair():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
        conexao.close()


    



    
    
    
    
    
