from progresso.menu_principal import rodar_menu_principal
from banco import conexao

if __name__ == "__main__":
    try:
        rodar_menu_principal()
    finally:
        conexao.close()

