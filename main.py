import os
import random
import sys
import platform

def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def buy(bal, matcoin, matcoin_price):
    clear()
    print(f"Ваш баланс: {bal}$")
    print("Доступные валюты:\n")
    
    print(f"1. Маткоин ({matcoin_price})")
    print("0. Выход")
    
    print("\nКакую валюту вы вы хотите приобрести?")
    userinput = input("> ")
    
    if userinput == "1":
        if bal <= matcoin_price:
            print("У вас недостаточно денег для совершения покупки")
            input()
            return bal, matcoin
        else:
            bal -= matcoin_price
            matcoin += 1
            return bal, matcoin
    elif userinput == "0":       
        return bal, matcoin
    else:
        print(f"Валюта с номером {userinput} не найдена")    
        input()
        return bal, matcoin

def main():
    bal = 100
    matcoin = 0
    matcoin_price = 0
    
    matcoin_price = random.randint(45, 67)

    while True:
        clear()
        print(f"Ваш баланс: {bal}$")
        print(f"Ваши маткоины: {matcoin}")
        print(f"\nКурс маткоина: 1 – {matcoin_price}")
        
        print("\nЧто вы хотите сделать?")
        print("1. Ничего")
        print("2. Выйти")
        print("3. Приобрести")
        
        userinput = input("> ")
        
        if userinput == "2":
            print("\nПока!")
            sys.exit(0)
        elif userinput == "3":
            data = buy(bal, matcoin, matcoin_price)
            bal = data[0]
            matcoin = data[1]

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПока!")
        sys.exit(0)
    except Exception as e:
        print(f"Ошибка: {e}")