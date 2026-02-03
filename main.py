import os
import random

bal = 100
matcoin = 0

while True:
    os.system("clear")
    print(f"Ваш баланс: {bal}")
    print(f"Ваши маткоины: {matcoin}")
    
    print("\nЧто вы хотите сделать?")
    print("1. Ничего")
    
    userinput = input("> ")
