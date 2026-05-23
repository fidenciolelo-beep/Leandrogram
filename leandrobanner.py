import pyfiglet
from colorama import Fore, Style, init
import os

init()

os.system('clear')

banner = pyfiglet.figlet_format("LeandroHacker", font="doom")

linhas = banner.split('\n')
cores = [Fore.MAGENTA, Fore.RED, Fore.YELLOW, Fore.RED, Fore.MAGENTA, Fore.CYAN]

for i, linha in enumerate(linhas):
    cor = cores[i % len(cores)]
    print(cor + Style.BRIGHT + linha)

print()
print(Fore.MAGENTA + Style.BRIGHT + "✦" + Fore.RED + "▓▓▓▓" + Fore.YELLOW + "▓▓▓▓" + Fore.MAGENTA + "▓▓▓▓" + Fore.CYAN + "▓▓▓▓" + Fore.MAGENTA + "✦")
print()
print(Fore.CYAN + Style.BRIGHT + "  ◈  Bem-vindo de volta, Leandro!  ◈")
print(Fore.MAGENTA + "  ✦ " + Fore.YELLOW + "O sistema está sob seu controle..." + Fore.MAGENTA + " ✦")
print()
print(Style.RESET_ALL)
