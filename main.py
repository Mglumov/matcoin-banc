import os
import random
import sys
import platform
import pickle
import hashlib

def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def save_game(bal, matcoin, matcoin_price):
    """сохранить прогресс игры"""
    
    data = {
        'balance': bal,
        'matcoin': matcoin,
        'matcoin_price': matcoin_price
    }
    
    with open('save.pkl', 'wb') as file:
        pickle.dump(data, file)
        
    print("Сохранение успешно!")

def load_game():
    """загрузить прогресс игры"""
    
    try:
        with open('save.pkl', 'rb') as f:
            data = pickle.load(f)
            
        return data['balance'], data['matcoin'], data['matcoin_price']
    
    except FileNotFoundError:
        return "notfound"
    except Exception:
        return None


def cost_change(matcoin_price):
    way = bool(random.getrandbits(1))
    
    if way:
        cost = random.randint(0, 190)
        return cost
    else:
        cost = random.randint(-190, 0)
        if cost < 0:
            return 0
        return cost 

def admin(bal, matcoin, matcoin_price):
    clear()
    print("Добро пожаловать в админ панель\n")
    
    print(f"Ваш баланс: {bal}$")
    print(f"Ваши маткоины: {matcoin}")
    print(f"Курс маткоина: 1 → {matcoin_price}$")
    
    print("\nДоступные функции:") 
    print("1. Установить значение баланса")
    print("2. Установить стоимость маткоина")
        
    print("\nЧто вы хотите сделать?")    
    userinput = input("> ")
    
    if userinput == "1":
        userinput = input("Введите значение: ")
        try:
            userinput = int(userinput)
            bal = userinput
            return bal, matcoin, matcoin_price
        except:
            print("Ошибка при попытке преобразования типа данных")
            input()
            pass
            
    elif userinput == "2" : 
        userinput = input("Введите значение: ")
        try: 
            userinput = int(userinput)
            matcoin_price = userinput 
            return bal, matcoin , matcoin_price
        except:
            print("Ошибка при попытке преобразования типа данных")
            input()
            pass
        
    else:
        print(f"Функция {userinput} не найдена")   
        input()
        return bal, matcoin, matcoin_price 
 
 
def buy(bal, matcoin, matcoin_price):
    clear()
    print(f"Ваш баланс: {bal}$")
    print("Доступные валюты:\n")
    
    print(f"1. Маткоин ({matcoin_price}$ → 1)")
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

def sell(bal, matcoin, matcoin_price):
    clear()
    print(f"Ваш баланс: {bal}$")
    print(f"Ваши маткоины: {matcoin}\n")
    print("Доступные валюты:\n")
    
    print(f"1. Маткоин (1 → {matcoin_price}$)")
    print("0. Выход")
    
    print("\nКакую валюту вы вы хотите продать?")
    userinput = input("> ")
    
    if userinput == "1":
        if matcoin <= 0:
            print("У вас нет маткоинов для продажи")
            input()
            return bal, matcoin
        else:
            bal += matcoin_price
            matcoin -= 1
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
        print(f"\nКурс маткоина: 1 → {matcoin_price}$")
        
        print("\nЧто вы хотите сделать?")
        print("1. Ничего")
        print("2. Выйти")
        print("3. Приобрести")
        print("4. Продать")
        print("5. Сохранить прогресс")
        print("6. Загрузить прогресс")
        
        userinput = input("> ")
        hashinput = hashlib.md5(userinput.encode()).hexdigest()

        if userinput == "2":
            are_you_sure = input("Вы уверены что хотите выйти из игры? (сохранение нужно делать вручную!)\n> ")
            
            if are_you_sure.lower() in ("y", "yes", "д", "да"):
                print("\nПока!")
                sys.exit(0)
            else:
                continue
            
        elif userinput == "3":
            data = buy(bal, matcoin, matcoin_price)
            bal = data[0]
            matcoin = data[1]
        elif userinput == "4":
            data = sell(bal, matcoin, matcoin_price)
            bal = data[0]
            matcoin = data[1]
        elif userinput == "5":
            save_game(bal, matcoin, matcoin_price)
        elif userinput == "6":
            save = load_game()
            
            if save is None:
                print("Произоршла ошибка при загрузке сохранения")
                input()
                continue
            elif save == "notfound":
                print("Сохранение не было найдено")
                input()
                continue
            else:
                pass
            
            bal = save[0]
            matcoin = save[1]
            matcoin_price = save[2]
        elif hashinput == "36539da04d2b567146fa71125e983be3":
            bal, matcoin, matcoin_price = admin(bal, matcoin, matcoin_price)    
        elif userinput == "1":
            pass
        else:
            pass
        
        if not hashinput == "36539da04d2b567146fa71125e983be3":
            matcoin_price = cost_change(matcoin_price)    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПока!")
        sys.exit(0)
    except Exception as e:
        print(f"Ошибка: {e}")
