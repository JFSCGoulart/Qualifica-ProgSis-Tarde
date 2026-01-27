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
