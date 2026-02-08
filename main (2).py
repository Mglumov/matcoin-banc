import os
import random
import sys
import platform
import pickle
import hashlib
import time

class ColorSystem:
    def __init__(self):
        self.support_colors = self._check_color_support()
    
    def _check_color_support(self):
        if platform.system() == 'Windows':
            if sys.platform == 'win32':
                os.system('color')
                return True
        
        if 'TERM' in os.environ and os.environ['TERM'] != 'dumb':
            return True
        
        return sys.stdout.isatty()
    
    def _colorize(self, text, color_code):
        if not self.support_colors:
            return text
        return f"\033[{color_code}m{text}\033[0m"
    
    def red(self, text):
        return self._colorize(text, "91")
    
    def green(self, text):
        return self._colorize(text, "92")
    
    def yellow(self, text):
        return self._colorize(text, "93")
    
    def blue(self, text):
        return self._colorize(text, "94")
    
    def grey(self, text):
        return self._colorize(text, "90")
    
    def bold(self, text):
        return self._colorize(text, "1")
    
    def success(self, text):
        return self.green(f"[✓] {text}")
    
    def error(self, text):
        return self.red(f"[X] {text}")
    
    def warning(self, text):
        return self.yellow(f"[!] {text}")
    
    def info(self, text):
        return self.blue(f"[i] {text}")

colors = ColorSystem()

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

def about():
    clear()
    print("MatcoinBank Simulator\n")
    
    print("Добро пожаловать в игру в жанре симулятора инвестирования и криптовалюты")
    print("В этой игре вы можете инвестировать в различные валюты и получать прибыль (но это не гарантированно)")
    print("А также можно попробавть себя в роли майнера и добыть монеты")
    print("(учитывайте что некоторые вещи в игре могут отличаться от реальности)")
    
    print("\nРазработчики: ")
    print("1. SuperDragon777")
    print("2. SukunaRemen13")
    print("3. Mglumov")
    
    print("\nРепозиторий на гитхабе:\nhttps://github.com/mglumov/matcoin-banc")
    
    input("\nНажмите Enter чтобы продолжить...")

def admin(bal, matcoin, matcoin_price, bitcoin, bitcoin_price):
    clear()
    print("Добро пожаловать в админ панель\n")
    
    print(f"Ваш баланс: {bal}$")
    print(f"Ваши маткоины: {matcoin}")
    print(f"Курс маткоина: 1 → {matcoin_price}$")
    print(f"Ваши биткоины: {bitcoin}")
    print(f"Курс биткоина: 1 → {bitcoin_price * 10}$")
    print(f"Курс биткоина: 0.1 → {bitcoin_price}$")
    
    print("\nДоступные функции:") 
    print("1. Установить значение баланса")
    print("2. Установить значение баланса маткоина")
    print("3. Установить значение баланса биткоина ")
    print("4. Установить стоимость маткоина")
    print("5. Установить стоимость биткоина")
     

        
    print("\nЧто вы хотите сделать?")    
    userinput = input("> ")
    
    if userinput == "1":
        userinput = input("Введите значение: ")
        try:
            userinput = int(userinput)
            bal = userinput
            return bal, matcoin, matcoin_price, bitcoin, bitcoin_price
        except:
            print(colors.error("Ошибка при попытке преобразования типа данных"))
            input()
            pass
            
    elif userinput == "4":
        userinput = input("Введите значение: ")
        try: 
            userinput = int(userinput)
            matcoin_price = userinput 
            return bal, matcoin, matcoin_price, bitcoin, bitcoin_price
        except:
            print(colors.error("Ошибка при попытке преобразования типа данных"))
            input()
            pass
    
    elif userinput == "5":
        userinput = input("Введите значение: ")
        try: 
            userinput = int(userinput)
            bitcoin_price = userinput 
            return bal, matcoin, matcoin_price, bitcoin, bitcoin_price
        except:
            print(colors.error("Ошибка при попытке преобразования типа данных"))
            input()
            pass
        
    elif userinput == "2":
        userinput = input("Введите значение: ")
        try:
            userinput = int(userinput)
            matcoin = userinput
            return bal, matcoin, matcoin_price, bitcoin, bitcoin_price
        except:
            print(colors.error("Ошибка при попытке преобразования типа данных"))
            input()
            pass    

    elif userinput == "3":
        userinput = input("Введите значение: ")
        try:
            userinput = float(userinput)
            bitcoin = userinput
            return bal, matcoin, matcoin_price, bitcoin, bitcoin_price
        except:
            print(colors.error("Ошибка при попытке преобразования типа данных"))
            input()
            pass    
        
    else:
        print(f"Функция {userinput} не найдена")   
        input()
        return bal, matcoin, matcoin_price, bitcoin, bitcoin_price
    
def mine_btc(bitcoin): # TODO: сделать короче чтобы можно было проиграть и получить минус битка (учитывать что биткоины не могут быть отрицательными)
    clear()
    print("Майним биток...\n")
    
    total_time = random.uniform(2.0, 5.0) # время от 2 до 5 сек
    
    mined_amount = random.uniform(0.005, 0.02) # биток от 0.005 до 0.02
    mined_amount = round(mined_amount, 3)
    
    steps = 100

    outcome = random.random() # определение исход майнинга
    
    if outcome < 0.10: # полный провал (10%)
        fail_at = random.randint(20, 60)
        fail_type = "full"
        fail_message = random.choice([
            ("❌ КРИТИЧЕСКАЯ ОШИБКА!", "🔥 Видеокарта сгорела!", "💸 Биткоины не получены"),
            ("❌ ПОТЕРЯ СОЕДИНЕНИЯ!", "📡 Пул майнинга недоступен", "💸 Биткоины не получены"),
            ("❌ АТАКА 51%!", "⚠️  Сеть скомпрометирована", "💸 Биткоины не получены"),
            ("❌ ОТКЛЮЧЕНИЕ ЭЛЕКТРИЧЕСТВА!", "⚡ Нет питания", "💸 Биткоины не получены"),
        ])
    elif outcome < 0.25: # неудача (25%)
        fail_at = random.randint(50, 90)
        fail_type = "partial"
        fail_message = random.choice([
            ("⚠️  ПЕРЕГРЕВ ОБОРУДОВАНИЯ!", "🌡️  Температура критическая", "частично"),
            ("⚠️  НЕСТАБИЛЬНОЕ СОЕДИНЕНИЕ!", "📶 Слабый сигнал", "частично"),
            ("⚠️  ОШИБКА ВЫЧИСЛЕНИЯ!", "⚠️  Неверный хэш блока", "частично"),
            ("⚠️  НЕДОСТАТОЧНО МОЩНОСТИ!", "🔋 Низкий заряд батареи", "частично"),
        ])
    else: # успех
        fail_at = None
        fail_type = None
        fail_message = None
    
    for i in range(steps + 1):
        if fail_at is not None and i >= fail_at:
            filled = int(30 * i / steps)
            bar = '▓' * filled + '░' * (30 - filled)
            print(f'\rПрогресс: [{bar}] {i}%', end='', flush=True)
            time.sleep(0.5)
            
            if fail_type == "full":
                print(f"\n\n{fail_message[0]}")
                print(fail_message[1])
                print(fail_message[2])
                input("\nНажмите Enter для продолжения...")
                return bitcoin
            
            elif fail_type == "partial":
                partial_amount = mined_amount * (i / 100) * random.uniform(0.3, 0.6)
                partial_amount = round(partial_amount, 3)
                bitcoin += partial_amount
                bitcoin = round(bitcoin, 3)
                
                print(f"\n\n{fail_message[0]}")
                print(fail_message[1])
                print(f"Получено: +{partial_amount} BTC ({fail_message[2]})")
                print(f"Всего биткоинов: {bitcoin} BTC")
                input("\nНажмите Enter для продолжения...")
                return bitcoin
        
        filled = int(30 * i / steps)
        bar = '▓' * filled + '░' * (30 - filled)
        percent = i
        elapsed = (i / steps) * total_time
        
        print(f'\rПрогресс: [{bar}] {percent}% | {elapsed:.1f}s / {total_time:.1f}s', end='', flush=True)
        time.sleep(total_time / steps)
    
    bitcoin += mined_amount
    bitcoin = round(bitcoin, 3)
    
    print("\n\nМайнинг успешно завершен!")
    print(f"Получено: +{mined_amount} BTC")
    print(f"Всего биткоинов: {bitcoin} BTC")
    input("\nНажмите Enter для продолжения...")
    
    return bitcoin

def buy(bal, matcoin, matcoin_price, bitcoin, bitcoin_price):
    clear()
    print(f"Ваш баланс: {bal}$")
    print("Доступные валюты:\n")
    
    print(f"1. Маткоин ({matcoin_price}$ → 1)")
    print(f"2. Биткоин ({bitcoin_price * 10}$ → 1)")
    print("0. Выход")
    
    print("\nКакую валюту вы вы хотите приобрести?")
    userinput = input("> ")
    
    if userinput == "1":
        print(f"Сколько валюты вы хотите купить?")
        userinput = input("Введите количество: ")
        userinput = int(userinput)
        if bal < matcoin_price*userinput:
            print("Вам не хватает денег для покупки")
            return bal, matcoin, bitcoin
        else:
            bal -= matcoin_price * userinput
            matcoin += userinput
            return bal, matcoin, bitcoin    
        
    elif userinput == "2":
        print(f"Сколько валюты вы хотите купить?")
        userinput = input("Введите количество: ")
        userinput = float(userinput)
        if bal < bitcoin_price * 10 *userinput:
            print("Вам не хватает денег для покупки")
            return bal, matcoin, bitcoin
        else:
            bal -= bitcoin_price * 10 * userinput
            bitcoin += userinput
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
    print(f"2. Биткоин (1 → {bitcoin_price * 10}$)")
    print("0. Выход")
    
    print("\nКакую валюту вы вы хотите продать?")
    userinput = input("> ")
    
    if userinput == "1":
        print(f"Сколько валюты вы хотите продать?")
        userinput = input("Введите количество: ")
        userinput = int(userinput)
        if matcoin < userinput:
            print("Вам не хватает маткоинов для продажи")
        else:
            bal += matcoin_price
            matcoin -= userinput 
            return bal, matcoin, bitcoin
        
    elif userinput == "2":
        print(f"Сколько валюты вы хотите продать?")
        userinput = input("Введите количество: ")
        userinput = float(userinput)
        if bitcoin < userinput:
            print("Вам не хватает биткоинов для продажи")
            return bal, matcoin, bitcoin
        else:
            bal += bitcoin_price * 10 * userinput
            bitcoin -= userinput
            return bal, matcoin, bitcoin    
    
    elif userinput == "0":       
        return bal, matcoin, bitcoin
    else:
        print(f"Валюта с номером {userinput} не найдена")    
        input()
        return bal, matcoin, bitcoin
    
def main():
    clear()
    save = load_game()
    
    if save == "notfound":
        print(colors.info("Сохранение не найдено. Начинаем новую игру..."))
        bal = 100
        matcoin = 0
        matcoin_price = random.randint(45, 67)
        bitcoin = 0
        bitcoin_price = random.randint(9000, 11000)
        input("Нажмите Enter для продолжения...")
        
    elif save is None:
        print(colors.error("Ошибка при загрузке сохранения. Начинаем новую игру..."))
        bal = 100
        matcoin = 0
        matcoin_price = random.randint(45, 67)
        bitcoin = 0
        bitcoin_price = random.randint(9000, 11000)
        input("Нажмите Enter для продолжения...")
    else:
        print(colors.success("Сохранение успешно загружено!"))
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

        bitcoin_diff = bitcoin_price * 10 - previous_bitcoin_price * 10
        if bitcoin_diff > 0:
            print(f"Курс биткоина: 1 → {bitcoin_price * 10}$ 📈 (+{bitcoin_diff}$)")
        elif bitcoin_diff < 0:
            print(f"Курс биткоина: 1 → {bitcoin_price * 10}$ 📉 ({bitcoin_diff}$)")
        else:
            print(f"Курс биткоина: 1 → {bitcoin_price * 10}$ ━")        
        
        bitcoin_diff = bitcoin_price - previous_bitcoin_price
        if bitcoin_diff > 0:
            print(f"Курс биткоина: 0.1 → {bitcoin_price}$ 📈 (+{bitcoin_diff}$)")
        elif bitcoin_diff < 0:
            print(f"Курс биткоина: 0.1 → {bitcoin_price}$ 📉 ({bitcoin_diff}$)")
        else:
            print(f"Курс биткоина: 0.1 → {bitcoin_price}$ ━")

         
        
        print("\nЧто вы хотите сделать?")
        print("1. Об игре")
        print("2. Выйти")
        print("3. Приобрести")
        print("4. Продать")
        print("5. Сохранить прогресс")
        print("6. Загрузить прогресс")
        print("7. Майнить биток")
        
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
                print(colors.error("Произошла ошибка при загрузке сохранения"))
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
        elif userinput == "7":
            bitcoin = mine_btc(bitcoin)
        elif userinput == "1":
            about()
        else:
            pass
        
        if not hashinput == "36539da04d2b567146fa71125e983be3":    #бро не пытайся брутфорсить,зачем тебе это?
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
        print(colors.error(f"Ошибка: {e}"))