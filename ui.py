import os
import platform

def clear():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def call_to_action_clear():
    input("\nPressione Enter para continuar...")
    clear()

def menu_title(title):
    print(f"\n{80 * "#"}")
    print(title)
    print(80 * "#")
