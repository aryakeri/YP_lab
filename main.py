print('Hello, GitHub!')

# ===== ЦИКЛЫ =====

# 1) Таблица умножения 1..9 (табами)
for i in range(1, 10):
    row = []
    for j in range(1, 10):
        row.append(str(i * j))
    print('\t'.join(row))
print('-' * 40)

# 2) Сумма нечётных от 1 до 100
sum_odds = sum(range(1, 101, 2))
print("Сумма нечётных 1..100:", sum_odds)
print('-' * 40)

# 3) Делители числа n
n = int(input("Введите число n для делителей: "))
nn = abs(n)
divs = [d for d in range(1, nn + 1) if nn % d == 0]
print("Делители:", divs)
print('-' * 40)

# 4) Факториал числа
m = int(input("Введите число для факториала: "))
fact = 1
for i in range(2, max(0, m) + 1):
    fact *= i
print("Факториал:", fact)
print('-' * 40)

# 5) Последовательность Фибоначчи длиной k
k = int(input("Длина последовательности Фибоначчи k: "))
fib = []
a, b = 0, 1
for _ in range(max(0, k)):
    fib.append(a)
    a, b = b, a + b
print("Фибоначчи:", fib)
print('=' * 60)

# ===== Подготовка случайных чисел для следующих заданий =====
import random
numbers = [random.randint(-50, 50) for _ in range(10)]
print("Случайные numbers:", numbers)
print('=' * 60)

# ===== СПИСКИ =====

# 1) Только чётные элементы списка (из numbers)
evens = [x for x in numbers if x % 2 == 0]
print("Чётные в numbers:", evens)

# 2) Максимум и минимум в списке (из numbers)
print("min(numbers) =", min(numbers), "max(numbers) =", max(numbers))

# 3) Ввод 5 чисел, сортировка и вывод
user_list = []
print("Введите 5 чисел (по одному на строку):")
for _ in range(5):
    user_list.append(int(input()))
user_list.sort()
print("Отсортированный список:", user_list)

# 4) Удалить дубликаты без множеств (пройдёмся и соберём уникальные)
no_dups = []
for x in numbers:
    if x not in no_dups:
        no_dups.append(x)
print("numbers без дубликатов:", no_dups)

# 5) Поменять местами первый и последний элемент списка (копию сделаем)
swapped = numbers[:]  # копия
if len(swapped) >= 2:
    swapped[0], swapped[-1] = swapped[-1], swapped[0]
print("Поменяли 1-й и последний:", swapped)
print('=' * 60)

# ===== СЛОВАРИ =====

# 1) Словарь студентов и средний балл (простой пример)
students = {"Ivan": 4, "Anna": 5, "Petr": 3}
avg = sum(students.values()) / len(students)
print("Средний балл:", avg)

# 2) Подсчёт букв в строке
s = input("Введите строку для подсчёта букв: ")
letter_count = {}
for ch in s:
    letter_count[ch] = letter_count.get(ch, 0) + 1
print("Буква -> количество:", letter_count)

# 3) Квадраты для ключей 1..10
squares = {i: i * i for i in range(1, 11)}
print("1..10 -> квадрат:", squares)

# 4) Словарь из двух списков (короткий пример)
keys = ["a", "b", "c"]
vals = [10, 20, 30]
paired = dict(zip(keys, vals))
print("Словарь из списков:", paired)
print('=' * 60)

# ===== МНОЖЕСТВА =====

# 1) Два множества: пересечение и объединение
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}
print("Пересечение A ∩ B:", A & B)
print("Объединение A ∪ B:", A | B)

# 2) Уникальные слова из ввода
text = input("Введите текст для уникальных слов: ")
unique_words = set(text.lower().split())
print("Уникальные слова:", unique_words)

# 3) Общие элементы двух списков (пример)
L1 = [1, 2, 2, 3, 10]
L2 = [2, 3, 5, 10, 10]
commons = set(L1) & set(L2)
print("Общие элементы:", commons)

# 4) Проверка подмножества
C = {1, 2}
D = {0, 1, 2, 3}
print("C подмножество D?:", C.issubset(D))

# 5) Удалить из множества все элементы меньше заданного числа
S = {random.randint(-10, 10) for _ in range(10)}
t = int(input("Порог для удаления из множества (< порога удалить): "))
filtered = {x for x in S if x >= t}
print("Исходное множество:", S)
print("После фильтра (>= порога):", filtered)
print('=' * 60)

# ===== КОМБИНИРОВАННЫЕ ЗАДАНИЯ =====

# 1) Список из 20 случайных чисел и только уникальные
nums20 = [random.randint(0, 10) for _ in range(20)]
unique_vals = list(set(nums20))
print("20 чисел:", nums20)
print("Уникальные значения:", unique_vals)

# 2) Словарь: элемент -> количество повторений
counts = {}
for x in nums20:
    counts[x] = counts.get(x, 0) + 1
print("Подсчёт повторений:", counts)

# 3) Множество слов длиной > 5
words = ["python", "list", "dictionary", "set", "comprehension", "loop"]
long_words = {w for w in words if len(w) > 5}
print("Слова >5 символов:", long_words)

# 4) Ввести предложение и посчитать слова
sent = input("Введите предложение: ").lower()
word_counts = {}
for w in sent.split():
    word_counts[w] = word_counts.get(w, 0) + 1
print("Слово -> частота:", word_counts)

# 5) Список -> множество -> список (убрать дубли)
dup_list = [1, 2, 2, 3, 3, 3, 4]
unique_list = list(set(dup_list))
print("Без дублей:", unique_list)

# 6) Словарь "товар-цена": самый дорогой
goods = {"apple": 50, "banana": 30, "mango": 120, "orange": 60}
most_expensive = max(goods, key=goods.get)
print("Самый дорогой товар:", most_expensive, "за", goods[most_expensive])

# 7) Имена, что встречаются более 1 раза и какое чаще всего
names = ["Ivan", "Anna", "Ivan", "Petr", "Anna", "Ivan"]
name_counts = {}
for name in names:
    name_counts[name] = name_counts.get(name, 0) + 1
more_than_once = [n for n, c in name_counts.items() if c > 1]
most_common_name = max(name_counts, key=name_counts.get)
print("Имена >1 раза:", more_than_once)
print("Чаще всего:", most_common_name)

# 8) Строка -> словарь: символ -> индекс первого вхождения
s2 = input("Введите строку для индексов первых вхождений: ")
first_index = {}
for i, ch in enumerate(s2):
    if ch not in first_index:
        first_index[ch] = i
print("Символ -> первый индекс:", first_index)
