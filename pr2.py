from functools import wraps

<<<<<<< HEAD

=======
>>>>>>> 4ab5704 (WIP)
# 1) Декоратор логирования
def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Вызов функции {func.__name__} с аргументами {args} и {kwargs}")
        result = func(*args, **kwargs)
        print(f"Функция {func.__name__} вернула {result}")
        return result
<<<<<<< HEAD

=======
>>>>>>> 4ab5704 (WIP)
    return wrapper


# Примерные функции под логирование
@logger
def add(a, b):
    return a + b

<<<<<<< HEAD

=======
>>>>>>> 4ab5704 (WIP)
@logger
def divide(a, b):
    if b == 0:
        return "Деление на ноль запрещено"
    return a / b

<<<<<<< HEAD

@logger
def greet(name):
    print(f"Привет, {name}!")
    # возвращает None
=======
@logger
def greet(name):
    print(f"Привет, {name}!")  # печать приветствия
    # возвращает None — это тоже покажет logger
>>>>>>> 4ab5704 (WIP)


# 2) Декоратор доступа
def require_role(allowed_roles):
    """
    allowed_roles: список ролей (например, ["admin", "manager"])
    Ожидается, что первая позиция в аргументах — это user-словарь с ключами 'name' и 'role'.
    """
<<<<<<< HEAD

=======
>>>>>>> 4ab5704 (WIP)
    def decorator(func):
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            role = user.get("role")
            if role in allowed_roles:
                return func(user, *args, **kwargs)
            else:
                print(f"Доступ запрещён пользователю {user.get('name')}")
                return None
<<<<<<< HEAD

        return wrapper

=======
        return wrapper
>>>>>>> 4ab5704 (WIP)
    return decorator


# Пример использования декоратора доступа
@require_role(["admin"])
@logger
def delete_database(user):
    print(f"База данных удалена пользователем {user['name']}")
    return "OK"

<<<<<<< HEAD

=======
>>>>>>> 4ab5704 (WIP)
@require_role(["admin", "manager"])
@logger
def view_stats(user):
    return f"Статистика доступна для {user['name']}"


# Тесты
if __name__ == "__main__":
    # ----- Тесты логгера -----
    add(2, 3)
    divide(10, 2)
    divide(5, 0)
    greet("Алексей")

<<<<<<< HEAD
    print("\n" + "-" * 50 + "\n")

    # ----- Тесты декоратора доступа -----
    admin = {"name": "Иван", "role": "admin"}
    manager = {"name": "Мария", "role": "manager"}
    guest = {"name": "Гость", "role": "guest"}

    # delete_database: только admin
    delete_database(admin)  # допустим
    delete_database(manager)  # запрещён
    delete_database(guest)  # запрещён
=======
    print("\n" + "-"*50 + "\n")

    # ----- Тесты декоратора доступа -----
    admin   = {"name": "Иван", "role": "admin"}
    manager = {"name": "Мария", "role": "manager"}
    guest   = {"name": "Гость", "role": "guest"}

    # delete_database: только admin
    delete_database(admin)    # допустим
    delete_database(manager)  # запрещён
    delete_database(guest)    # запрещён
>>>>>>> 4ab5704 (WIP)

    print()

    # view_stats: admin и manager
<<<<<<< HEAD
    view_stats(admin)  # допустим
    view_stats(manager)  # допустим
    view_stats(guest)  # запрещён
=======
    view_stats(admin)         # допустим
    view_stats(manager)       # допустим
    view_stats(guest)         # запрещён
>>>>>>> 4ab5704 (WIP)
