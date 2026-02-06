from gerenciador_usuarios.menu import rodar_menu
from banco import conexao

if __name__ == "__main__":
    try:
        rodar_menu()
    finally:
        conexao.close()
