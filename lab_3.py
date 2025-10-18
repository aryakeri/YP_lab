"""Implementations for Lab 3 assignments."""

from datetime import date, datetime
from decimal import Decimal, getcontext
from fractions import Fraction

# Настройка точности для задач Decimal.
getcontext().prec = 28

# 1. List comprehension (простое преобразование)
squares = [number**2 for number in range(1, 11)]

# 2. List comprehension (фильтрация)
even_numbers = [number for number in range(1, 20) if number % 2 == 0]

# 3. List comprehension (работа со строками)
words = ["python", "Java", "c++", "Rust", "go"]
uppercase_long_words = [word.upper() for word in words if len(word) > 3]


class Countdown:
    """Итератор, возвращающий последовательность чисел от n до 1."""

    def __init__(self, n: int):
        if n <= 0:
            raise ValueError("n must be a positive integer")
        self.current = n

    def __iter__(self):
        return self

    def __next__(self):
        if self.current == 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


def fibonacci(n: int):
    """Генератор, возвращающий первые n чисел Фибоначчи."""
    if n < 0:
        raise ValueError("n must be a non-negative integer")

    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def calculate_deposit(principal: Decimal, annual_rate_percent: Decimal, years: int):
    """Возвращает итоговую сумму и прибыль по вкладу с ежемесячной капитализацией."""
    if principal <= 0:
        raise ValueError("Начальная сумма должна быть положительной")
    if annual_rate_percent < 0:
        raise ValueError("Процентная ставка не может быть отрицательной")
    if years <= 0:
        raise ValueError("Срок вклада должен быть положительным целым числом")

    monthly_rate = annual_rate_percent / Decimal(12 * 100)
    months = years * 12
    compound_factor = (Decimal("1") + monthly_rate) ** months
    final_amount = (principal * compound_factor).quantize(Decimal("0.01"))
    profit = (final_amount - principal).quantize(Decimal("0.01"))
    return final_amount, profit


def format_datetime_ru(value: datetime) -> str:
    """Возвращает строку с датой и временем в требуемом формате."""
    month_names = {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря",
    }
    return (
        f"Сегодня {value.day} {month_names[value.month]} {value.year} года, "
        f"время: {value.hour}:{value.minute:02d}"
    )


if __name__ == "__main__":
    print("Squares:", squares)
    print("Even numbers:", even_numbers)
    print("Uppercase words:", uppercase_long_words)

    print("Countdown from 5:")
    for number in Countdown(5):
        print(number, end=" ")
    print()

    print("Fibonacci first 5 numbers:")
    for number in fibonacci(5):
        print(number, end=" ")
    print()

    initial_deposit = Decimal("100000.00")
    annual_rate = Decimal("7.5")
    deposit_years = 3
    final_sum, profit = calculate_deposit(initial_deposit, annual_rate, deposit_years)
    print(f"Deposit result: итоговая сумма {final_sum} руб., прибыль {profit} руб.")

    fraction_a = Fraction(3, 4)
    fraction_b = Fraction(5, 6)
    print("Fractions addition:", fraction_a + fraction_b)
    print("Fractions subtraction:", fraction_a - fraction_b)
    print("Fractions multiplication:", fraction_a * fraction_b)
    print("Fractions division:", fraction_a / fraction_b)

    current_datetime = datetime.now()
    print("Current date and time:", current_datetime)
    print("Current date:", current_datetime.date())
    print("Current time:", current_datetime.time())

    birth_date = date(2005, 1, 18)
    today = date.today()
    days_lived = (today - birth_date).days
    next_birthday_year = today.year
    if (today.month, today.day) >= (birth_date.month, birth_date.day):
        next_birthday_year += 1
    next_birthday = date(next_birthday_year, birth_date.month, birth_date.day)
    days_until_next_birthday = (next_birthday - today).days
    print(f"Days since birth: {days_lived}")
    print(f"Days until next birthday: {days_until_next_birthday}")

    print("Formatted datetime:", format_datetime_ru(current_datetime))
