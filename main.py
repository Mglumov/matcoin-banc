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

def save_game(bal, matcoin, matcoin_price, bitcoin, bitcoin_price):
    """сохранить прогресс игры"""
    
    data = {
        'balance': bal,
        'matcoin': matcoin,
        'matcoin_price': matcoin_price,
        'bitcoin': bitcoin,
        'bitcoin_price': bitcoin_price
    }
    
    with open('save.pkl', 'wb') as file:
        pickle.dump(data, file)
        
    print("Сохранение успешно!")

def load_game():
    """загрузить прогресс игры"""
    
    try:
        with open('save.pkl', 'rb') as f:
            data = pickle.load(f)
        
        bitcoin = data.get('bitcoin', 0)
        bitcoin_price = data.get('bitcoin_price', random.randint(9000, 11000))
            
        return data['balance'], data['matcoin'], data['matcoin_price'], bitcoin, bitcoin_price
    
    except FileNotFoundError:
        return "notfound"
    except Exception:
        return None


def old_cost_change(matcoin_price): #! УСТАРЕВШАЯ ФУНКЦИЯ, DO NOT USE
    way = bool(random.getrandbits(1))
    
    if way:
        cost = random.randint(0, 190)
        return cost
    else:
        cost = random.randint(-190, 0)
        if cost < 0:
            return 0
        return cost 

def cost_change(price, is_bitcoin=False):
    if is_bitcoin:
        volatility = random.uniform(-0.03, 0.03)
        
        if random.random() < 0.03:
            volatility = random.uniform(-0.15, 0.15)
    else:
        volatility = random.uniform(-0.05, 0.05)  # базовое событие (от -5% до +5%)
        
        if random.random() < 0.05:  # случайное событие (5% шанс)
            volatility = random.uniform(-0.30, 0.30)  # от -30% до +30%

    change = int(price * volatility)
    new_price = price + change
    
    if new_price < 1:  # ограничение до 1
        new_price = 1
    
    return new_price

def admin(bal, matcoin, matcoin_price, bitcoin, bitcoin_price):
    clear()
    print("Добро пожаловать в админ панель\n")
    
    print(f"Ваш баланс: {bal}$")
    print(f"Ваши маткоины: {matcoin}")
    print(f"Курс маткоина: 1 → {matcoin_price}$")
    print(f"Ваши биткоины: {bitcoin}")
    print(f"Курс биткоина: 0.1 → {bitcoin_price}$")
    
    print("\nДоступные функции:") 
    print("1. Установить значение баланса")
    print("2. Установить стоимость маткоина")
    print("3. Установить стоимость биткоина")
        
    print("\nЧто вы хотите сделать?")    
    userinput = input("> ")
    
    if userinput == "1":
        userinput = input("Введите значение: ")
        try:
            userinput = int(userinput)
            bal = userinput
            return bal, matcoin, matcoin_price, bitcoin, bitcoin_price
        except:
            print("Ошибка при попытке преобразования типа данных")
            input()
            pass
            
    elif userinput == "2":
        userinput = input("Введите значение: ")
        try: 
            userinput = int(userinput)
            matcoin_price = userinput 
            return bal, matcoin, matcoin_price, bitcoin, bitcoin_price
        except:
            print("Ошибка при попытке преобразования типа данных")
            input()
            pass
    
    elif userinput == "3":
        userinput = input("Введите значение: ")
        try: 
            userinput = int(userinput)
            bitcoin_price = userinput 
            return bal, matcoin, matcoin_price, bitcoin, bitcoin_price
        except:
            print("Ошибка при попытке преобразования типа данных")
            input()
            pass
        
    else:
        print(f"Функция {userinput} не найдена")   
        input()
        return bal, matcoin, matcoin_price, bitcoin, bitcoin_price
 
 
def buy(bal, matcoin, matcoin_price, bitcoin, bitcoin_price):
    clear()
    print(f"Ваш баланс: {bal}$")
    print("Доступные валюты:\n")
    
    print(f"1. Маткоин ({matcoin_price}$ → 1)")
    print(f"2. Биткоин ({bitcoin_price}$ → 0.1)")
    print("0. Выход")
    
    print("\nКакую валюту вы вы хотите приобрести?")
    userinput = input("> ")
    
    if userinput == "1":
        if bal < matcoin_price:
            print("У вас недостаточно денег для совершения покупки")
            input()
            return bal, matcoin, bitcoin
        else:
            bal -= matcoin_price
            matcoin += 1
            return bal, matcoin, bitcoin
    
    elif userinput == "2":
        if bal < bitcoin_price:
            print("У вас недостаточно денег для совершения покупки")
            input()
            return bal, matcoin, bitcoin
        else:
            bal -= bitcoin_price
            bitcoin += 0.1
            bitcoin = round(bitcoin, 1)
            return bal, matcoin, bitcoin
    
    elif userinput == "0":       
        return bal, matcoin, bitcoin
    else:
        print(f"Валюта с номером {userinput} не найдена")    
        input()
        return bal, matcoin, bitcoin

def sell(bal, matcoin, matcoin_price, bitcoin, bitcoin_price):
    clear()
    print(f"Ваш баланс: {bal}$")
    print(f"Ваши маткоины: {matcoin}")
    print(f"Ваши биткоины: {bitcoin}\n")
    print("Доступные валюты:\n")
    
    print(f"1. Маткоин (1 → {matcoin_price}$)")
    print(f"2. Биткоин (0.1 → {bitcoin_price}$)")
    print("0. Выход")
    
    print("\nКакую валюту вы вы хотите продать?")
    userinput = input("> ")
    
    if userinput == "1":
        if matcoin <= 0:
            print("У вас нет маткоинов для продажи")
            input()
            return bal, matcoin, bitcoin
        else:
            bal += matcoin_price
            matcoin -= 1
            return bal, matcoin, bitcoin
    
    elif userinput == "2":
        if bitcoin < 0.1:
            print("У вас нет биткоинов для продажи")
            input()
            return bal, matcoin, bitcoin
        else:
            bal += bitcoin_price
            bitcoin -= 0.1
            bitcoin = round(bitcoin, 1)
            return bal, matcoin, bitcoin
    
    elif userinput == "0":       
        return bal, matcoin, bitcoin
    else:
        print(f"Валюта с номером {userinput} не найдена")    
        input()
        return bal, matcoin, bitcoin
    
def main():
    save = load_game()
    
    if save == "notfound":
        print("Сохранение не найдено. Начинаем новую игру...")
        bal = 100
        matcoin = 0
        matcoin_price = random.randint(45, 67)
        bitcoin = 0
        bitcoin_price = random.randint(9000, 11000)
        input("Нажмите Enter для продолжения...")
        
    elif save is None:
        print("Ошибка при загрузке сохранения. Начинаем новую игру...")
        bal = 100
        matcoin = 0
        matcoin_price = random.randint(45, 67)
        bitcoin = 0
        bitcoin_price = random.randint(9000, 11000)
        input("Нажмите Enter для продолжения...")
    else:
        print("Сохранение успешно загружено!")
        bal = save[0]
        matcoin = save[1]
        matcoin_price = save[2]
        bitcoin = save[3]
        bitcoin_price = save[4]
        input("Нажмите Enter для продолжения...")
    
    previous_matcoin_price = matcoin_price
    previous_bitcoin_price = bitcoin_price
    
    while True:
        clear()
        print(f"Ваш баланс: {bal}$")
        print(f"Ваши маткоины: {matcoin}")
        print(f"Ваши биткоины: {bitcoin}")
        
        price_diff = matcoin_price - previous_matcoin_price
        if price_diff > 0:
            print(f"\nКурс маткоина: 1 → {matcoin_price}$ 📈 (+{price_diff}$)")
        elif price_diff < 0:
            print(f"\nКурс маткоина: 1 → {matcoin_price}$ 📉 ({price_diff}$)")
        else:
            print(f"\nКурс маткоина: 1 → {matcoin_price}$ ━")
        
        bitcoin_diff = bitcoin_price - previous_bitcoin_price
        if bitcoin_diff > 0:
            print(f"Курс биткоина: 0.1 → {bitcoin_price}$ 📈 (+{bitcoin_diff}$)")
        elif bitcoin_diff < 0:
            print(f"Курс биткоина: 0.1 → {bitcoin_price}$ 📉 ({bitcoin_diff}$)")
        else:
            print(f"Курс биткоина: 0.1 → {bitcoin_price}$ ━")
        
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
            are_you_sure = input("Вы уверены что хотите выйти из игры? (сохранение нужно делать вручную!)\n> ")
            
            if are_you_sure.lower() in ("y", "yes", "д", "да"):
                print("\nПока!")
                sys.exit(0)
            else:
                continue
            
        elif userinput == "3":
            data = buy(bal, matcoin, matcoin_price, bitcoin, bitcoin_price)
            bal = data[0]
            matcoin = data[1]
            bitcoin = data[2]
        elif userinput == "4":
            data = sell(bal, matcoin, matcoin_price, bitcoin, bitcoin_price)
            bal = data[0]
            matcoin = data[1]
            bitcoin = data[2]
        elif userinput == "5":
            save_game(bal, matcoin, matcoin_price, bitcoin, bitcoin_price)
            input("Нажмите Enter для продолжения...")
        elif userinput == "6":
            save = load_game()
            
            if save is None:
                print("Произошла ошибка при загрузке сохранения")
                input()
                continue
            elif save == "notfound":
                print("Сохранение не было найдено")
                input()
                continue
            else:
                pass
            
            bal = save[0]
            matcoin = save[1]
            matcoin_price = save[2]
            bitcoin = save[3]
            bitcoin_price = save[4]
        elif hashinput == "36539da04d2b567146fa71125e983be3":
            bal, matcoin, matcoin_price, bitcoin, bitcoin_price = admin(bal, matcoin, matcoin_price, bitcoin, bitcoin_price)    
        elif userinput == "1":
            pass
        else:
            pass
        
        if not hashinput == "36539da04d2b567146fa71125e983be3":
            previous_matcoin_price = matcoin_price
            previous_bitcoin_price = bitcoin_price
            matcoin_price = cost_change(matcoin_price, is_bitcoin=False)
            bitcoin_price = cost_change(bitcoin_price, is_bitcoin=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПока!")
        sys.exit(0)
    except Exception as e:
        print(f"Ошибка: {e}")