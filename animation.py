#from tqdm import tqdm
import time
import os
import shutil
from colorama import Fore, Style
columns, rows = shutil.get_terminal_size()
print(Fore.BLACK + "-" * columns + Style.RESET_ALL)
for _ in range(rows-2):
    print(Fore.ORANGE + "|" + " " * (columns-2) + "|" + Style.RESET_ALL)
print(Fore.BLACK + "-" * columns + Style.RESET_ALL)
# for i in tqdm(range(100), desc="Animating", ascii=True):
#     time.sleep(0.05)

print(Fore.RED + "This is red text" + Style.RESET_ALL)

