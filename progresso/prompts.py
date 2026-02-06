from ui import call_to_action_clear
from getpass import getpass

def perguntar(prompt: str, secret = False, redraw = None):
    while True:
        value = getpass(prompt) if secret else input(prompt)
        value = value.strip()

        if value == "<":
            return None
        if value == "":
            print("\nNão pode ficar vazio. Digite novamente ou '<' pra voltar.")
            call_to_action_clear()
            if redraw:
                redraw()
            continue

        return value
