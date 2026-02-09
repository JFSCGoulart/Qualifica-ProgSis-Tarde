#conectando aos outros codigos
import sqlite3
from Models.verRanking import ranking, ranking_geral
from Models.ListarCursos import acessar_atividades, adicionar_feito, listar_cursos, fazerAtividades, listar_cursos_progresso, registrar_resposta, registrar_resposta_errada
from Models.resetarProgresso import resetar_progresso
from Models.verProgresso import progresso_diario, progresso_por_curso, progresso_total


#conectando o banco de dados
from Connection.conexao import cursor, conexao

#exibi o menu de opções para o aluno
def Menu_cursos():
    while True:
        #exibindo o menu na tela
         print("\nMenu Alunos")
         print("1 - Ver Seus Cursos")
         print("2 - Ver Progresso Diario")
         print("3 - Ver Progresso por Curso")
         print("4 - Ver Progresso Total")
         print("5 - Ver ranking")
         print("6 - Resetar Progresso")
         print("0 - Sair")

        #Variavel para guardar a escolha do aluno
         escolha = input("Escolha uma opção: ")

        #Condicional para a escolha do aluno
         if escolha == '1':
            listar_cursos(id_usuario = 1)
         elif escolha == '2':
            progresso_diario(id_usuario = 1)
         elif escolha == '3':
            progresso_por_curso(id_usuario = 1)
         elif escolha == '4':
            progresso_total(id_usuario = 1)
         elif escolha == '5':
            ranking(id_usuario = 1)
         elif escolha == '6':
            resetar_progresso(id_usuario = 1)
         elif escolha == '0':
            print("Saindo.")
            break
         else:
            print("Opção inválida. Tente novamente.")

Menu_cursos() 
conexao.close()        
        
     
    