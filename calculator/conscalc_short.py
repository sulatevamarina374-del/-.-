import random
import re

MIN, MAX = -30, 30
UNIVERSE = set(range(MIN, MAX + 1))
SETS = [None] * 3


def read(prompt, low=None, high=None):
    while True:
        try:
            value = int(input(prompt))
            if (low is None or value >= low) and (high is None or value <= high):
                return value
            print(f"Введите число от {low} до {high}.")
        except ValueError:
            print("Введите целое число.")
        except EOFError:
            raise SystemExit


def show(values):
    if values is None:
        print("не задано")
    elif values:
        print("{" + ", ".join(map(str, sorted(values))) + "}")
    else:
        print("∅")


def new_set():
    method = read("1 - вручную, 2 - случайно, 3 - по условиям: ", 1, 3)

    if method == 1:
        result = set()
        count = read("Количество элементов: ", 0, len(UNIVERSE))
        while len(result) < count:
            value = read("Элемент: ")
            if MIN <= value <= MAX and value not in result:
                result.add(value)
            else:
                print("Число должно быть от -30 до 30 и не повторяться.")
        return result

    if method == 2:
        count = read("Количество элементов: ", 0, len(UNIVERSE))
        return set(random.sample(range(MIN, MAX + 1), count))

    return by_conditions()


def by_conditions():
    print("1 +, 2 -, 3 чётные, 4 нечётные, 5 кратные, 6 диапазон, 0 готово")
    checks = {}

    while True:
        choice = read("Условие: ", 0, 6)
        if choice == 0:
            break
        if choice == 1:
            checks[1] = lambda x: x > 0
        elif choice == 2:
            checks[2] = lambda x: x < 0
        elif choice == 3:
            checks[3] = lambda x: x % 2 == 0
        elif choice == 4:
            checks[4] = lambda x: x % 2 != 0
        elif choice == 5:
            divisor = read("Делитель: ")
            while divisor == 0:
                divisor = read("Делитель не может быть 0: ")
            checks[5] = lambda x, d=divisor: x % d == 0
        elif choice == 6:
            left = read("Левая граница: ")
            right = read("Правая граница: ")
            if left > right:
                left, right = right, left
            checks[6] = lambda x, a=left, b=right: a <= x <= b

    return {x for x in UNIVERSE if all(check(x) for check in checks.values())}


def choose_set(prompt):
    number = read(prompt, 1, 3) - 1
    if SETS[number] is None:
        print("Это множество ещё не задано.")
        return None
    return number


def operate():
    operation = read("1 объединение, 2 пересечение, 3 разность, 4 дополнение: ", 1, 4)
    first = choose_set("Первое множество: ")
    if first is None:
        return

    if operation == 4:
        result = UNIVERSE - SETS[first]
    else:
        second = choose_set("Второе множество: ")
        if second is None:
            return
        if operation == 1:
            result = SETS[first] | SETS[second]
        elif operation == 2:
            result = SETS[first] & SETS[second]
        else:
            result = SETS[first] - SETS[second]

    print("Результат:", end=" ")
    show(result)


def calculate(text):
    text = re.sub(r"\s+", "", text)
    if not re.fullmatch(r"!?[123](?:[+*-]!?[123])*", text):
        return None

    tokens = re.findall(r"!?[123]|[+*-]", text)

    def get_set(token):
        value = SETS[int(token[-1]) - 1]
        if value is None:
            return None
        return UNIVERSE - value if token.startswith("!") else set(value)

    result = get_set(tokens[0])
    if result is None:
        return None

    for operation, token in zip(tokens[1::2], tokens[2::2]):
        value = get_set(token)
        if value is None:
            return None
        if operation == "+":
            result |= value
        elif operation == "*":
            result &= value
        else:
            result -= value
    return result


def main():
    print("КАЛЬКУЛЯТОР МНОЖЕСТВ")
    print("Универсум: от -30 до 30")

    while True:
        print("\n1 задать  2 показать  3 операция  4 формула  0 выход")
        command = read("Команда: ", 0, 4)

        if command == 0:
            break
        if command == 1:
            number = read("Номер множества: ", 1, 3) - 1
            SETS[number] = new_set()
            print("Сохранено:", end=" ")
            show(SETS[number])
        elif command == 2:
            for number, value in enumerate(SETS, 1):
                print(f"Множество {number}:", end=" ")
                show(value)
        elif command == 3:
            operate()
        else:
            result = calculate(input("Формула, например !1+2*3: "))
            if result is None:
                print("Неправильная формула или множество не задано.")
            else:
                print("Результат:", end=" ")
                show(result)

    print("Работа завершена.")


if __name__ == "__main__":
    main()
